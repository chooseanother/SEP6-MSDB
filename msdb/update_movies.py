from msdb.models import Movie
from msdb.utils.movie_api import MovieFromApi, get_movie_from_api


# script to update moveis with more information from api
def update_movies(number: int = 1000, offset: int = 0):
    # get movies that needs to be updated
    movies = Movie.objects.filter(genre__isnull=True)[offset * number : number * offset + number]

    updated = 0
    not_updated = 0

    for movie in movies:
        print(f"Updating movie {movie.id}")
        api_movie = get_movie_from_api(movie.id)

        if isinstance(api_movie, MovieFromApi):
            movie.genre = api_movie.genre
            movie.director = api_movie.director
            movie.actors = api_movie.actors
            movie.poster_url = api_movie.poster_link
            movie.save()
            updated += 1
            print(f"Movie {movie.id} updated. total {updated} of {number}")
        else:
            not_updated += 1
            print(f"Movie {movie.id} not updated. total {not_updated} of {number}")

    count = Movie.objects.filter(genre__isnull=True).count()

    print(f"{count} movies left. updated: {updated} not updated: {not_updated}")
