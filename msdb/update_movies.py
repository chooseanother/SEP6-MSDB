from msdb.models import Movie
from msdb.utils.movie_api import MovieFromApi, get_movie_from_api

#API_KEY = "e6f34a57"
#URL = "http://www.omdbapi.com/" #?apikey=e6f34a57&i=tt3896198

MOVIE_ID = "tt3896198"

def main():

    api_movie = get_movie_from_api(MOVIE_ID)
    
    local_movie = Movie.objects.get(id=MOVIE_ID)

    print(api_movie)
    print(local_movie)

    if isinstance(api_movie, MovieFromApi):
        local_movie.genre = api_movie.genre
        local_movie.director = api_movie.director
        local_movie.actors = api_movie.actors
        local_movie.poster_url = api_movie.poster_link


if __name__ == "__main__":
    main()
