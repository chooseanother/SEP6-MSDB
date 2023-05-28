import datetime
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Func, Avg

from msdb.models import Movie
from msdb.users.models import User

def movie_stats(request, movie_id: str):
    if request.method == "GET":
        movie = Movie.objects.get(id=movie_id)

        graph_data = dict()
        graph_data["rating_star_amount"] = list(movie.reviews.all().values('rating').annotate(count=Count('rating')).order_by('rating'))

        first_rating_date = movie.reviews.order_by('created_at').first().created_at.date()
        last_rating_date = movie.reviews.order_by('-created_at').first().created_at.date()
        count = (last_rating_date-first_rating_date).days + 1
        days = dict()
        days_cumulative = dict()
        for i in range(count):
            date = first_rating_date + datetime.timedelta(days=i)
            days[date.strftime("%d.%m.%Y")] = movie.reviews.all()\
                .filter(created_at__year=date.year, created_at__month=date.month, created_at__day=date.day).count()
            days_cumulative[date.strftime("%d.%m.%Y")] = movie.reviews.all()\
                .filter(created_at__range=(datetime.datetime.combine(first_rating_date, datetime.time.min),
                                datetime.datetime.combine(date, datetime.time.max))).count()
        graph_data["ratings_over_time"] = days
        graph_data["ratings_over_time_cumulative"] = days_cumulative

        movie_avg_ratings = Movie.objects.annotate(avg_rating=Avg('reviews__rating'))
        ratings_count = dict()
        for i in range(10, 51):
            rating = i/10
            ratings_count[rating] = movie_avg_ratings.filter(avg_rating__gte=rating-0.05, avg_rating__lt=rating+0.05).count()
        graph_data["all_movie_ratings_count"] = ratings_count



        return JsonResponse(graph_data, status=200)

    return JsonResponse({}, status=400)


def user_stats(request, user_id: int):
    if request.method == "GET":
        user = User.objects.get(id=user_id)

        graph_data = dict()
        ratings_count = dict()
        most_ratings = User.objects.all().annotate(reviews_count=Count('reviews')).order_by('-reviews_count').first().reviews.count()
        all_users = User.objects.all()
        for i in range(0, most_ratings+1):
            ratings_count[i] = all_users.annotate(reviews_count=Count('reviews')).filter(reviews_count=i).count()
        graph_data["all_user_ratings_count"] = ratings_count

        return JsonResponse(graph_data, status=200)

    return JsonResponse({}, status=400)

