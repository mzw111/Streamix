from flask import Blueprint, jsonify
from db import fetch_all, fetch_one

movies_bp = Blueprint("movies", __name__)

# Map movie titles to their actual TMDB poster URLs
MOVIE_POSTERS = {
    "The Dark Knight": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "Inception": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    "The Shawshank Redemption": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
    "Pulp Fiction": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
    "The Godfather": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Interstellar": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "The Matrix": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "Forrest Gump": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
    "Gladiator": "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg",
    "The Lord of the Rings: The Return of the King": "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
    "Fight Club": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    "The Silence of the Lambs": "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg",
    "Saving Private Ryan": "https://image.tmdb.org/t/p/w500/uqx37QI3HySKFCQFJQlKaPeUzD2.jpg",
    "Schindler's List": "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
    "The Departed": "https://image.tmdb.org/t/p/w500/nT97ifVT2J1yMQmeq20Qblg61T.jpg",
    "Goodfellas": "https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
    "The Prestige": "https://image.tmdb.org/t/p/w500/tRNlZbgNCNOpLpbPEz5L8G8A0JN.jpg",
    "Whiplash": "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg",
    "Parasite": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    "The Green Mile": "https://image.tmdb.org/t/p/w500/velWPhVMQeQKcxggNEU8YmIo52R.jpg"
}

def transform_movie(movie):
    """Transform database movie format to API format"""
    if not movie:
        return None
    
    title = movie.get("Title", "")
    poster_url = MOVIE_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg")
    
    return {
        "movie_id": movie.get("Movie_Id"),
        "title": title,
        "description": movie.get("Description"),
        "release_year": movie.get("Release_Date").year if movie.get("Release_Date") else None,
        "duration": movie.get("Duration"),
        "age_rating": movie.get("Age_Rating"),
        "average_rating": float(movie.get("average_rating")) if movie.get("average_rating") else 0,
        "poster_url": poster_url,
    }

@movies_bp.route("/", methods=["GET"])
def get_all_movies():
    movies = fetch_all("SELECT * FROM movie")
    transformed_movies = [transform_movie(m) for m in movies]
    return jsonify({"success": True, "movies": transformed_movies})

@movies_bp.route("/<int:movie_id>", methods=["GET"])
def get_movie_by_id(movie_id):
    movie = fetch_one("SELECT * FROM movie WHERE Movie_Id = %s", (movie_id,))
    if movie:
        return jsonify({"success": True, "movie": transform_movie(movie)})
    else:
        return jsonify({"success": False, "message": "Movie not found"}), 404

@movies_bp.route("/genre/<string:genre_name>", methods=["GET"])
def get_movies_by_genre(genre_name):
    query = """
        SELECT m.* 
        FROM movie m
        JOIN movie_genre mg ON m.Movie_Id = mg.Movie_Id
        JOIN genre g ON mg.Genre_Id = g.Genre_Id
        WHERE g.Genre_Name = %s
    """
    movies = fetch_all(query, (genre_name,))
    transformed_movies = [transform_movie(m) for m in movies]
    return jsonify({"success": True, "movies": transformed_movies})
