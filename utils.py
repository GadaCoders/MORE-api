import requests


def fetch_movie_details(imdb_title_id):
    URL = f'https://api.themoviedb.org/3/movie/{imdb_title_id}?api_key=86b01c870d192d9c90bfbfbc18d9d37a'

    POSTER_PATH = "https://image.tmdb.org/t/p/w500"
    
    movie_data  = requests.get(URL).json()

    if not movie_data:
        return None

    return {
        "imdb_title_id": imdb_title_id,
        "title": movie_data["title"] if movie_data["title"] != None else '',
        "original_title": movie_data["original_title"] if movie_data["original_title"] != None else '',
        "poster_path": POSTER_PATH + movie_data["poster_path"] if movie_data["poster_path"] != None else '',
        "backdrop_path": POSTER_PATH + movie_data["backdrop_path"] if movie_data["backdrop_path"] != None else '',
        "genres": movie_data["genres"] if movie_data["genres"] != None else '',
        "overview": movie_data["overview"] if movie_data["overview"] != None else '',
        "release_date": movie_data['release_date'] if movie_data["release_date"] != None else ''
    }