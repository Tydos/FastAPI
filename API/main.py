from fastapi import FastAPI, Path, Query, HTTPException
from database import check_connection,show_movies,search_movie,search_genre, upload_movie
from pydantic import BaseModel, Field
#Start Uvicorn server and check mongo status
#uvicorn main:app --reload
app = FastAPI()
check_connection()

#validated data
class Movieinfo(BaseModel):
    title: str = Field(...)
    plot: str = Field(...,max_length=50)
    runtime: int = Field(...,gt=0)
    year: int = Field(...,gt=1900,lt=2025)

# user inputs
my_movie = {
    "title": "Prasad2",
    "plot": "A long list of activities",
    "runtime": 24,
    "year": 2000
}

new_movie = Movieinfo(**my_movie)  # unpack dictionary into fields
# print(new_movie)
#Routes
@app.get("/")
def hello():
    return{"message":"hello world"}

@app.get("/test")
def test():
    return{"message":"FastAPI testing..."}

@app.get("/movies/{limit}")
def get_movies_by_limit(limit: int = Path(...,description="Number of movies to show")):
    movies = show_movies(limit)
    if movies == []:
        raise HTTPException(503,detail="No Movies Found")
    else:
        return movies

@app.get("/search")
def search(
    movie_title : str|None = Query(None, description="Movie title"),
    genre:  str|None = Query(None, description="Movie Genre"),
):
    #find movie by its title
    if movie_title:
        movies = search_movie(movie_title)

    #title not there, search by genre
    elif genre:
        movies = search_genre(genre)    

    #Incorrect argument
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either movie_title or genre"
        )

    #empty set
    if not movies:
        raise HTTPException(status_code=503, detail="No Movies Found")

    #success
    return movies

@app.post("/upload")
def upload(new_movie:Movieinfo):    
    #upload
    status = upload_movie(new_movie.dict())
    if status:
        return {"message":"uploaded {new_movie}"}
    else:
        return{"message":"Error"}

    