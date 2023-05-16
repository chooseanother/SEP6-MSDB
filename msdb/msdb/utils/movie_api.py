from dataclasses import dataclass
import requests
import json

@dataclass
class MovieFromApi:
    id: str
    title: str
    released: str
    runtime: str
    genre: list[str]
    director: list[str]
    actors: list[str]
    year: int
    rated: str
    plot: str
    poster_link: str
    imdb_rating: float

def get_movie_from_api(movie_id: str) -> MovieFromApi|str:
    url = "https://www.omdbapi.com/?apikey=371a659c&i=" + movie_id
    response = requests.get(url)
    if response.status_code != 200:
        return "Error in API connection."
    if "Error" in response.json():
        return response.json()["Error"]
    else:
        return movie_json_mapper(response.json())

def movie_json_mapper(json:dict) -> MovieFromApi:
    movie_from_api = MovieFromApi(
        id=json["imdbID"],
        title=json["Title"],
        released=json["Released"],
        runtime=json["Runtime"],
        genre=[x.strip() for x in json["Genre"].split(',')],
        director=[x.strip() for x in json["Director"].split(',')],
        actors=[x.strip() for x in json["Actors"].split(',')],
        year=json["Year"],
        rated=json["Rated"],
        plot=json["Plot"],
        poster_link=json["Poster"],
        imdb_rating=json["imdbRating"]
    )
    return movie_from_api
