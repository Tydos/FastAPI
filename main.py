from fastapi import FastAPI
from database import fetch_movies

#load the environment variables in the main script instead of helper files, to avoid env issues
import os
from dotenv import load_dotenv
load_dotenv()
URI = os.getenv("URI")

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

@app.get("/movies")
def get_movies():
    movies = fetch_movies()
    return{"movies":movies}
