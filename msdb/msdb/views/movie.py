from django.shortcuts import render
def movie(request, movie_id):
    #movie = Movie.objects.get(id=movie_id)
    movie = dict(title="Kill Bill Vol. 1", id="tt826471")
    context = dict(movie=movie)
    return render(request, "movies/movies.html", context)
