from django.shortcuts import render

from msdb.models import Movie
from msdb.utils.movie_api import get_movie_from_api, MovieFromApi


def movie(request, movie_id):
    try:
        #movie = Movie.objects.get(id=movie_id)
        movie = get_movie_from_api(movie_id)
    except Movie.DoesNotExist:
        return render(request, "404.html", dict(movie_id=movie_id))

    if isinstance(movie, MovieFromApi):
        context = dict(movie=movie)
        print(context)
        return render(request, "movies/movies.html", context)
    else:
        return render(request, "404.html", dict(exception=movie))




