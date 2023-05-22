from django.shortcuts import render
from msdb.utils.movie_api import get_movie_from_api, MovieFromApi
from msdb.models import Movie
from msdb.models import List

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
    
    user = None
    is_favorites = None
    is_watched = None
    is_watchlist = None

    if request.user.is_authenticated:
        user = request.user
        favorites = user.lists.get(list_type=List.ListChoices.FAVORITES)
        is_favorites = movie_datab in favorites.movies.all()
        watched = user.lists.get(list_type=List.ListChoices.WATCHED)
        is_watched = movie_datab in watched.movies.all()
        watchlist = user.lists.get(list_type=List.ListChoices.WATCHLIST)
        is_watchlist = movie_datab in watchlist.movies.all()

    context = dict(movie_api=movie_api, movie_datab=movie_datab, user=user,
                   is_favorites=is_favorites, is_watched=is_watched, is_watchlist=is_watchlist)
    
    if request.user.is_authenticated:
        user = request.user
        context["user"] = user
        # check if user has reviewed this movie
        try:
            review = movie_datab.reviews.get(user=user)
        except Exception:
            review = None
        context["review"] = review

    # get all reviews for a movie and exclude the logged in users review if it exists
    reviews = movie_datab.reviews.exclude(user=user) if request.user.is_authenticated else movie_datab.reviews.all()
    context["reviews"] = reviews

    return render(request, "movies/movie.html", context)
