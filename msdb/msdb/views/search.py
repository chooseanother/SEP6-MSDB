from functools import reduce
import operator
from itertools import chain
from django.db.models import Q, Count, F, Avg
from django.shortcuts import render, redirect

from msdb.models import Movie
from msdb.users.models import User


def search(request):
    if request.method == "POST":
        search_string = request.POST.get("query")
        queries = search_string.split()

        # Find movies
        movies = search_movie(queries)

        # Find people
        people = search_people(queries, search_string)

        # Find users
        users = search_users(queries)

        context = dict(search_string=search_string, movies=movies, users=users, people=people)
        return render(request, "search/search.html", context)
    else:
        return redirect('home')


def search_movie(queries : list):
    movies_result = Movie.objects.filter(reduce(operator.and_, (Q(title__icontains=x) for x in queries))).annotate(avg_rating=Avg('reviews__rating')).order_by(F('avg_rating').desc(nulls_last=True))[:10]
    # if no movies are found, do the search with or operator instead
    if movies_result.count() == 0:
        movies_result = Movie.objects.filter(reduce(operator.or_, (Q(title__icontains=x) for x in queries))).annotate(avg_rating=Avg('reviews__rating')).order_by(F('avg_rating').desc(nulls_last=True))[:10]

    return movies_result


def search_users(queries: list):
    users = User.objects.filter(reduce(operator.and_, (Q(name__icontains=x) for x in queries)))\
                .annotate(num_reviews=Count('reviews')).order_by(F('num_reviews').desc(nulls_last=True))[:10]
    # if no users are found, do the search with or operator instead
    if users.count() == 0:
        users = User.objects.filter(is_staff=False).filter(reduce(operator.or_, (Q(name__icontains=x) for x in queries)))\
                    .annotate(num_reviews=Count('reviews')).order_by(F('num_reviews').desc(nulls_last=True))[:10]

    return users


def search_people(queries: list, search_string: str) -> list:
    # Find directors
    directors = search_directors(queries)

    # Find actors
    actors = search_actors(queries)

    people = list(set(directors + actors))

    # check if exact match is found
    exact = [person for person in people if person.lower() == search_string.lower()]

    if len(exact) > 0:
        people = exact

    people = [dict(name=person, director=person in directors, actor=person in actors) for person in people]

    return people


def search_directors(queries: list) -> list:
    directors = []
    directors_qset = Movie.objects.values('director').filter(director__isnull=False)\
        .filter(reduce(operator.and_, (Q(director__icontains=x) for x in queries))).values_list('director', flat=True)
    # if no directors are found, do the search with or operator instead
    if len(directors_qset) == 0:
        directors_qset = Movie.objects.values('director').filter(director__isnull=False)\
            .filter(reduce(operator.or_, (Q(director__icontains=x) for x in queries))).values_list('director', flat=True)
    # if no directors are found skip the filtering
    if len(directors_qset) != 0:
        d_flat_distinct = list(set(chain.from_iterable(directors_qset)))
        d_filtered = [person for person in d_flat_distinct if any(query.lower() in person.lower() for query in queries)]
        directors = d_filtered[:10]

    return directors


def search_actors(queries: list) -> list:
    actors = []
    actors_qset = Movie.objects.values('actors').filter(actors__isnull=False)\
        .filter(reduce(operator.and_, (Q(actors__icontains=x) for x in queries))).values_list('actors', flat=True)
    # if no actors are found, do the search with or operator instead
    if len(actors_qset) == 0:
        actors_qset = Movie.objects.values('actors').filter(actors__isnull=False)\
            .filter(reduce(operator.or_, (Q(actors__icontains=x) for x in queries))).values_list('actors', flat=True)
    # if no actors are found skip the filtering
    if len(actors_qset) != 0:
        a_flat_distinct = list(set(chain.from_iterable(actors_qset)))
        a_filtered = [person for person in a_flat_distinct if any(query.lower() in person.lower() for query in queries)]
        actors = a_filtered[:10]

    return actors
