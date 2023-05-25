from django.shortcuts import render, redirect
from msdb.forms.review import ReviewForm
from msdb.utils.movie_api import get_movie_from_api, MovieFromApi
from msdb.models import Movie
from msdb.models import List
from msdb.models import Review

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
    review = None

    if request.user.is_authenticated:
        user = request.user
        favorites = user.lists.get(list_type=List.ListChoices.FAVORITES)
        is_favorites = movie_datab in favorites.movies.all()
        watched = user.lists.get(list_type=List.ListChoices.WATCHED)
        is_watched = movie_datab in watched.movies.all()
        watchlist = user.lists.get(list_type=List.ListChoices.WATCHLIST)
        is_watchlist = movie_datab in watchlist.movies.all()

        # check if user has reviewed this movie
        try:
            review = movie_datab.reviews.get(user=user)
        except Exception:
            review = None


    context = dict(movie_api=movie_api, movie_datab=movie_datab, user=user,
                is_favorites=is_favorites, is_watched=is_watched, is_watchlist=is_watchlist)

    # get all reviews for a movie and exclude the logged in users review if it exists
    reviews = movie_datab.reviews.exclude(user=user) if request.user.is_authenticated else movie_datab.reviews.all()
    context["reviews"] = reviews.order_by("-created_at")
    context["review"] = review
    if review:
        context["loop1"] = 3
        context["loop2"] = 2
    else:
        context["loop1"] = 4
        context["loop2"] = 3
    context["user"] = user
    context["PLACEHOLDER"] = "PLACEHOLDER"

    return render(request, "movies/movie.html", context)


def add_review(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            text = form.cleaned_data["text"]
            review = Review(movie=movie, user=request.user, rating=rating, text=text)
            if movie.reviews.filter(user=request.user).exists():
                return redirect("movie", movie_id=movie_id)
            review.save()
            # add the rated movie to a users watched list
            if request.user.is_authenticated:
                watched_list = request.user.lists.get(list_type=List.ListChoices.WATCHED)
                watched_list.movies.add(movie)

            return redirect("movie", movie_id=movie_id)
    else:
        form = ReviewForm()
    return render(request, "review/add_edit_review.html", dict(form=form, movie=movie))


def edit_review(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    review = movie.reviews.get(user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            text = form.cleaned_data["text"]
            review.rating = rating
            review.text = text
            review.save()
            return redirect("movie", movie_id=movie_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, "review/add_edit_review.html", dict(form=form, movie=movie))

