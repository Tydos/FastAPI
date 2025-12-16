from fastapi import FastAPI, Path, Query, HTTPException
from database import fetch_movies_list,search_movie

#load the environment variables in the main script instead of helper files, to avoid env issues
# import os
# from dotenv import load_dotenv
# load_dotenv()
# URI = os.getenv("URI")

#Start Uvicorn server with:
#uvicorn main:app --reload
app = FastAPI()

#Routes
@app.get("/")
def hello():
    return{"message":"hello world"}

@app.get("/test")
def test():
    return{"message":"FastAPI testing..."}

@app.get("/movies/{limit}")
def get_movies_by_limit(limit: int = Path(...,description="Number of movies to show")):
    movies = fetch_movies_list(limit)
    if movies == []:
        raise HTTPException(503,detail="No Movies Found")
    else:
        return movies

@app.get("/search/{movie_title}")
def search_movie_by_title(movie_title: str = Path(...,description="Enter name of the movie")):
    movies = search_movie(movie_title)
    return movies

