from django.shortcuts import render, redirect
from bootstrap_modal_forms.generic import BSModalCreateView
from msdb.forms.review import ReviewForm

from msdb.utils.movie_api import get_movie_from_api, MovieFromApi
from msdb.models import Movie, Review

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
    user = None
    if request.user.is_authenticated:
        user = request.user
        # check if user has reviewed this movie
        try:
            review = movie_datab.reviews.get(user=user)
        except Exception:
            review = None
        context["review"] = review

    # get all reviews for a movie and exclude the logged in users review if it exists
    reviews = movie_datab.reviews.exclude(user=user) if request.user.is_authenticated else movie_datab.reviews.all()
    context["reviews"] = reviews
    context["user"] = user

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
            # TODO: add the rated movie to a users watched list
            
            return redirect("movie", movie_id=movie_id)
    else:
        form = ReviewForm()
    return render(request, "review/add_review.html", dict(form=form, movie=movie))


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
    return render(request, "review/edit_review.html", dict(form=form, movie=movie))
