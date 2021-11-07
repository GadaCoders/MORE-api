from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pickle

from utils import fetch_movie_details

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
)

print("STARTING")

movie_data = pd.read_csv("./data/movie_data_final.csv")



@app.get("/")
def read_root():
    return {
        "MoRe": "Welcome to MoRe API", 
        "Try It Out": "Head onto /docs to try the api out"
        }

@app.get("/get-movies-from-title/{title}")
def get_movies_from_title(title: str):
    try:

        titles_ids = []
        for i in range(movie_data.shape[0]):
            movie = movie_data.iloc[i]
            if title.lower() in str(movie['title']).lower():
                titles_ids.append({'imdb_title_id': movie['imdb_title_id'],'title': movie['title']})
        
        return titles_ids

    except Exception as e:
        print(e)
        return e
    

@app.get("/recommend-movie/{imdb_title_id}")
def recommend_movies(imdb_title_id: str, limit: int = 10):

    try:
        
        if imdb_title_id not in movie_data['imdb_title_id'].values:
            raise HTTPException(status_code=404, detail="Entered movie is not found!")

        if limit >= 20:
            raise HTTPException(status_code=429, detail="You can request upto maximum 20 recommendations")

        movie_vectors = pickle.load(open("./data/final_movie_vec.pkl", 'rb'))

        index = movie_data[movie_data['imdb_title_id'] == imdb_title_id].index[0]

        selected_movie = movie_vectors[index]

        similarities = cosine_similarity(X=selected_movie.reshape(1,-1), Y=movie_vectors)

        similarities_sorted = sorted(list(enumerate(similarities[0])), reverse=True, key=lambda x: x[1])[1:limit+1]


        result = []
        for index, sim in similarities_sorted:
            movie = movie_data.iloc[index]

            id = movie['imdb_title_id']
            
            details = fetch_movie_details(id)


            if details:
                result.append(details) 

            break
        

        return {"result" : result}


    except HTTPException as e:

        if not e.status_code: 
            raise HTTPException(status_code=500, detail="Something went wrong!")
        else:
            raise e
    
    except Exception as e:
        print("Exception", e)
        raise HTTPException(status_code=500, detail="Something went wrong!")

    




