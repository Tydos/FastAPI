from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

#Connect to MongoDB using URI from environment variables
from dotenv import load_dotenv
load_dotenv()
URI = os.getenv("URI")
client = MongoClient(URI, server_api=ServerApi('1'))
database = client["sample_mflix"]
movies_collection = database["movies"]

#Check connection
def check_connection():
    try:
        client.admin.command('ismaster')
        print("MongoDB connection: Successful")
    except Exception as e:
        print("MongoDB connection: Failed", e)

#Show X number of movies
def show_movies(limit=1):
    search_query = {}
    projection_query = {"_id": 0, "title": 1}
    cursor = movies_collection.find(search_query, projection_query).limit(limit)
    return [movie.get("title") for movie in cursor]

def search_movie(movie_title: str) -> list[dict]:
    projection = {
        "_id": 0,
        "title": 1,
        "plot": 1,
        "runtime": 1,
        "year": 1,
        "genres": 1,
        "directors": 1,
        "cast": 1,
        "imdb": 1,
    }
    cursor = movies_collection.find({"title": movie_title}, projection)
    result = []
    for movie in cursor:
        result.append({
            "title": movie.get("title"),
            "plot": movie.get("plot"),
            "runtime": movie.get("runtime"),
            "year": movie.get("year"),
            "genres": movie.get("genres"),
            "directors": movie.get("directors"),
            "cast": movie.get("cast"),
            "imdb": movie.get("imdb")
        })
    return result

def search_genre(genre):
    search_query = {"genres":genre}
    projection = {
    "_id": 0,
    "title": 1,
    "plot": 1,
    "runtime": 1,
    "year": 1,
    "genres": 1,
    "directors": 1,
    "cast": 1,
    "imdb": 1,
    }
    cursor = movies_collection.find(search_query, projection).limit(5)
    results = []
    for movie in cursor:
        results.append({
            "title": movie.get("title"),
            "plot": movie.get("plot"),
            "runtime": movie.get("runtime"),
            "year": movie.get("year"),
            "genres": movie.get("genres"),
            "directors": movie.get("directors"),
            "cast": movie.get("cast"),
            "imdb": movie.get("imdb")
        })
    return results

def upload_movie(movie_data: dict):
    try:
        movies_collection.insert_one(movie_data)
        return True
    except Exception as e:
        print("Error uploading movie:", e)
        return False
    
    
#Tester code
if __name__ == "__main__":
    check_connection()
    movies = search_movie("It")
    print(movies)
