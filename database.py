from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

URI = os.getenv("URI")
client = MongoClient(URI, server_api=ServerApi('1'))

def setup_database():
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print("Connection failed:", e)
        raise

    database = client["sample_mflix"]
    return database["movies"]

def fetch_movies(limit=1):
    movies_collection = setup_database()
    cursor = movies_collection.find({}, {"_id": 0, "title": 1}).limit(limit)
    return [movie["title"] for movie in cursor if "title" in movie]

if __name__ == "__main__":
    print(fetch_movies())
