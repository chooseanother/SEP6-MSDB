from django.shortcuts import render, redirect

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
    if request.user.is_authenticated:
        user = request.user
        context["user"] = user
        # check if user has reviewed this movie
        try:
            review = movie_datab.reviews.get(user=user)
        except Exception:
            review = None
        context["review"] = review

        # handle review form
        form = ReviewForm(request.POST)
        context["form"] = form
        if request.method == "POST":
            if form.is_valid():
                rating = form.cleaned_data["rating"]
                text = form.cleaned_data["text"]
                review = Review(movie=movie_datab, user=user, rating=rating, text=text)
                review.save()
                return redirect("movie", movie_id=movie_id)


    # get all reviews for a movie and exclude the logged in users review if it exists
    reviews = movie_datab.reviews.exclude(user=user) if request.user.is_authenticated else movie_datab.reviews.all()
    context["reviews"] = reviews

    return render(request, "movies/movie.html", context)




