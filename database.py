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

def check_connection():
    try:
        client.admin.command('ismaster')
        print("MongoDB connection: Successful")
    except Exception as e:
        print("MongoDB connection: Failed", e)


def fetch_movies_list(limit=1):
    search_query = {}
    projection_query = {"_id": 0, "title": 1}
    cursor = movies_collection.find(search_query, projection_query).limit(limit)
    return [movie.get("title") for movie in cursor]

def search_movie(movie_title):
    search_query = {"title":movie_title}
    projection_query = {"_id": 0, "title": 1,"imdb.rating": 1}
    cursor = movies_collection.find(search_query,projection_query)
    movie_info = {}
    return [movie for movie in cursor]

if __name__ == "__main__":
    check_connection()
    # movies = search_movie("The Italian")
    # print(movies)
