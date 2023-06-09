import datetime
from operator import itemgetter

from django.db import connection
from django.db.models import Avg, Count
from django.http import JsonResponse

from msdb.models import List, Movie
from msdb.users.models import User


def movie_stats(request, movie_id: str):
    if request.method == "GET":
        movie = Movie.objects.get(id=movie_id)

        graph_data = {}
        any_reviews = False

        rating_star_amount = {}
        for i in range(1, 6):
            rating_star_amount[i] = movie.reviews.filter(rating=i).count()
            if rating_star_amount[i] != 0:
                any_reviews = True
        if not any_reviews:
            rating_star_amount = {}
        graph_data["rating_star_amount"] = rating_star_amount

        days = {}
        days_cumulative = {}
        if any_reviews:
            # starting at one day before the first rating to start at 0
            first_rating_date = movie.reviews.order_by("created_at").first().created_at.date() - datetime.timedelta(
                days=1
            )
            last_rating_date = movie.reviews.order_by("-created_at").first().created_at.date()
            count = (last_rating_date - first_rating_date).days + 1
            for i in range(count):
                date = first_rating_date + datetime.timedelta(days=i)
                days[date.strftime("%d.%m.%Y")] = (
                    movie.reviews.all()
                    .filter(created_at__year=date.year, created_at__month=date.month, created_at__day=date.day)
                    .count()
                )
                days_cumulative[date.strftime("%d.%m.%Y")] = (
                    movie.reviews.all()
                    .filter(
                        created_at__range=(
                            datetime.datetime.combine(first_rating_date, datetime.time.min),
                            datetime.datetime.combine(date, datetime.time.max),
                        )
                    )
                    .count()
                )
        graph_data["ratings_over_time"] = days
        graph_data["ratings_over_time_cumulative"] = days_cumulative

        ratings_count = {}
        if any_reviews:
            movie_avg_ratings = Movie.objects.annotate(avg_rating=Avg("reviews__rating"))
            for i in range(10, 51):
                rating = i / 10
                ratings_count[rating] = movie_avg_ratings.filter(
                    avg_rating__gte=rating - 0.05, avg_rating__lt=rating + 0.05
                ).count()
        graph_data["all_movie_ratings_count"] = ratings_count

        return JsonResponse(graph_data, status=200)

    return JsonResponse({}, status=400)


def user_stats(request, user_id: int):
    if request.method == "GET":
        user = User.objects.get(id=user_id)

        graph_data = {}
        ratings_count = {}
        most_ratings = (
            User.objects.exclude(is_staff=True)
            .all()
            .annotate(reviews_count=Count("reviews"))
            .order_by("-reviews_count")
            .first()
            .reviews.count()
        )
        all_users = User.objects.exclude(is_staff=True).all()
        for i in range(0, most_ratings + 1):
            ratings_count[i] = all_users.annotate(reviews_count=Count("reviews")).filter(reviews_count=i).count()
        graph_data["all_user_ratings_count"] = ratings_count

        cursor = connection.cursor()
        raw_query = """select unnest(subquery_alias.genre) as distinct_genres, count(*) as genres_group_by_count
            from (select genre from msdb_movie) as subquery_alias group by distinct_genres;"""
        cursor.execute(raw_query)
        genres_count = [{"genre": row[0], "count": row[1]} for row in cursor]
        all_genres = []
        for genre_count in genres_count:
            all_genres.append(genre_count["genre"])

        user_genres_count = {}
        for genre in all_genres:
            user_genres_count[genre] = 0

        watched_movies = user.lists.get(list_type=List.ListChoices.WATCHED).movies.all()
        for movie in watched_movies:
            for genre in movie.genre:
                user_genres_count[genre] = user_genres_count[genre] + 1
        graph_data["user_genres_count"] = user_genres_count

        user_directors_count = {}
        for movie in watched_movies:
            if movie.director is None:
                continue
            for director in movie.director:
                if director in user_directors_count:
                    user_directors_count[director] = user_directors_count[director] + 1
                else:
                    user_directors_count[director] = 1
        # get top 10 directors sorted by number of movies
        user_directors_count = dict(sorted(user_directors_count.items(), key=itemgetter(1), reverse=True)[:10])
        graph_data["user_directors_count"] = user_directors_count

        user_actor_count = {}
        for movie in watched_movies:
            if movie.actors is None:
                continue
            for actor in movie.actors:
                if actor in user_actor_count:
                    user_actor_count[actor] = user_actor_count[actor] + 1
                else:
                    user_actor_count[actor] = 1
        # get top 10 actors sorted by number of movies
        user_actor_count = dict(sorted(user_actor_count.items(), key=itemgetter(1), reverse=True)[:10])
        graph_data["user_actor_count"] = user_actor_count

        return JsonResponse(graph_data, status=200)

    return JsonResponse({}, status=400)


def person_stats(request, person_name: str):
    if request.method == "GET":
        graph_data = {}

        director_nmb_movies_years = {}
        director_rating_movies_years = {}
        director_movies = Movie.objects.filter(director__icontains=person_name)
        if director_movies:
            first_year = int(director_movies.values("year").order_by("year").first()["year"])
            last_year = int(director_movies.values("year").order_by("-year").first()["year"])

            if director_movies.exclude(reviews__isnull=True).count() != 0:
                for year in range(first_year, last_year + 1):
                    director_nmb_movies_years[year] = director_movies.filter(year=year).count()
                    director_rating_movies_years[year] = (
                        director_movies.filter(year=year)
                        .annotate(avg_rating=Avg("reviews__rating"))
                        .aggregate(Avg("avg_rating"))
                    )
            else:
                for year in range(first_year, last_year + 1):
                    director_nmb_movies_years[year] = director_movies.filter(year=year).count()
        graph_data["director_nmb_movies_years"] = director_nmb_movies_years
        graph_data["director_rating_movies_years"] = director_rating_movies_years

        actor_nmb_movies_years = {}
        actor_rating_movies_years = {}
        actor_movies = Movie.objects.filter(actors__icontains=person_name)
        if actor_movies:
            first_year = int(actor_movies.values("year").order_by("year").first()["year"])
            last_year = int(actor_movies.values("year").order_by("-year").first()["year"])
            if actor_movies.exclude(reviews__isnull=True).count() != 0:
                for year in range(first_year, last_year + 1):
                    actor_nmb_movies_years[year] = actor_movies.filter(year=year).count()
                    actor_rating_movies_years[year] = (
                        actor_movies.filter(year=year)
                        .annotate(avg_rating=Avg("reviews__rating"))
                        .aggregate(Avg("avg_rating"))
                    )
            else:
                for year in range(first_year, last_year + 1):
                    actor_nmb_movies_years[year] = actor_movies.filter(year=year).count()
        graph_data["actor_nmb_movies_years"] = actor_nmb_movies_years
        graph_data["actor_rating_movies_years"] = actor_rating_movies_years

        return JsonResponse(graph_data, status=200)

    return JsonResponse({}, status=400)
