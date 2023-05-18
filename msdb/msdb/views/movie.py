from django.shortcuts import render

from msdb.utils.movie_api import get_movie_from_api, MovieFromApi
from msdb.models import Movie

def movie(request, movie_id):
    #if movie id does not exist in our database, throw 404
    try:
        movie_datab = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return render(request, "404.html", dict(movie_id=movie_id))

    #if movie exists, try getting more information from api
    #if api throws an exception, we just display what we have
    movie_api = None
    try:
        movie_api = get_movie_from_api(movie_id)
    except Exception:
        pass

    context = dict(movie_api=movie_api, movie_datab=movie_datab)
    return render(request, "movies/movie.html", context)




