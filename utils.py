import requests


def fetch_movie_details(imdb_title_id):
    URL = f'https://api.themoviedb.org/3/movie/{imdb_title_id}?api_key=86b01c870d192d9c90bfbfbc18d9d37a'

    POSTER_PATH = "https://image.tmdb.org/t/p/w500"
    
    tmdb_movie_data  = requests.get(URL).json()


    if tmdb_movie_data.get("success") == False:
        return None
    
    print(tmdb_movie_data)
    

    return {
        "imdb_title_id": imdb_title_id,
        "title": tmdb_movie_data["title"] if tmdb_movie_data["title"] != None else '',
        "original_title": tmdb_movie_data["original_title"] if tmdb_movie_data["original_title"] != None else '',
        "poster_path": POSTER_PATH + tmdb_movie_data["poster_path"] if tmdb_movie_data["poster_path"] != None else '',
        "backdrop_path": POSTER_PATH + tmdb_movie_data["backdrop_path"] if tmdb_movie_data["backdrop_path"] != None else '',
        "genres": tmdb_movie_data["genres"] if tmdb_movie_data["genres"] != None else '',
        "overview": tmdb_movie_data["overview"] if tmdb_movie_data["overview"] != None else '',
        "release_date": tmdb_movie_data['release_date'] if tmdb_movie_data["release_date"] != None else '',
        "tagline": tmdb_movie_data['tagline'] if tmdb_movie_data["tagline"] != None else '',
        "vote_average": tmdb_movie_data["vote_average"] if tmdb_movie_data["vote_average"] != None else ''
    }
