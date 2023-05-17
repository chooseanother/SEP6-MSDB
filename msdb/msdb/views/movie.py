from django.shortcuts import render

from msdb.utils.movie_api import get_movie_from_api, MovieFromApi

def movie(request, movie_id):
    movie = None
    try:
        movie = get_movie_from_api(movie_id)
    except Exception:
        pass

    if isinstance(movie, MovieFromApi):
        context = dict(movie=movie)
        return render(request, "movies/movie.html", context)
    else:
        return render(request, "404.html", dict(exception=movie))




