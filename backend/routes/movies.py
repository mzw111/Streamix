from flask import Blueprint, jsonify
from db import fetch_all, fetch_one

movies_bp = Blueprint("movies", __name__)


MOVIE_POSTERS = {
    "The Dark Knight": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "Mad Max: Fury Road": "https://image.tmdb.org/t/p/w500/hA2ple9q4qnwxp3hKVNhroipsir.jpg",
    "John Wick": "https://image.tmdb.org/t/p/w500/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg",
    "The Shawshank Redemption": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
    "Forrest Gump": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
    "The Green Mile": "https://image.tmdb.org/t/p/w500/velWPhVMQeQKcxggNEU8YmIo52R.jpg",
    "Inception": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    "The Matrix": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "Interstellar": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "Blade Runner 2049": "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
    "The Grand Budapest Hotel": "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg",
    "Superbad": "https://image.tmdb.org/t/p/w500/ek8e8txUyUwd2BNqj6lFEerJfbq.jpg",
    "Se7en": "https://image.tmdb.org/t/p/w500/6yoghtyTpznpBik8EngEmJskVUO.jpg",
    "Gone Girl": "https://image.tmdb.org/t/p/w500/lv5xShBIDboxe4WqAjcv8L9FALz.jpg",
    "Shutter Island": "https://image.tmdb.org/t/p/w500/4GDy0PHYX3VRXUtwK5ysFbg3kEx.jpg",
    "The Conjuring": "https://image.tmdb.org/t/p/w500/wVYREutTvI2tmxr6ujrHT704wGF.jpg",
    "A Quiet Place": "https://image.tmdb.org/t/p/w500/nAU74GmpUk7t5iklEp3bufwDq4n.jpg",
    "The Notebook": "https://image.tmdb.org/t/p/w500/rNzQyW4f8B8cQeg7Dgj3n6eT5k9.jpg",
    "La La Land": "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
    "The Godfather": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Pulp Fiction": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"
}

# Map movie titles to video URLs (for movies that have videos)
MOVIE_VIDEOS = {
    "The Dark Knight": "/videos/15097-261402819_small.mp4",
    "Inception": "/videos/26452-358778857_small.mp4"
}

def transform_movie(movie):
    """Transform database movie format to API format"""
    if not movie:
        return None
    
    title = movie.get("Title", "")
    poster_url = MOVIE_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg")
    video_url = MOVIE_VIDEOS.get(title)  # Will be None if no video available
    
    return {
        "movie_id": movie.get("Movie_Id"),
        "title": title,
        "description": movie.get("Description"),
        "release_year": movie.get("Release_Date").year if movie.get("Release_Date") else None,
        "duration": movie.get("Duration"),
        "age_rating": movie.get("Age_Rating"),
        "average_rating": float(movie.get("average_rating")) if movie.get("average_rating") else 0,
        "poster_url": poster_url,
        "video_url": video_url,
    }

@movies_bp.route("/", methods=["GET"])
def get_all_movies():
    movies = fetch_all("SELECT * FROM movie")
    transformed_movies = []
    
    for m in movies:
        movie = transform_movie(m)
        if movie:
            # Fetch genres for this movie
            genres = fetch_all("""
                SELECT g.Genre_Id, g.Genre_Name 
                FROM genre g
                JOIN movie_genre mg ON g.Genre_Id = mg.Genre_Id
                WHERE mg.Movie_Id = %s
            """, (movie['movie_id'],))
            movie['genres'] = [{'genre_id': g['Genre_Id'], 'name': g['Genre_Name']} for g in genres]
            transformed_movies.append(movie)
    
    return jsonify({"success": True, "movies": transformed_movies})

@movies_bp.route("/<int:movie_id>", methods=["GET"])
def get_movie_by_id(movie_id):
    movie = fetch_one("SELECT * FROM movie WHERE Movie_Id = %s", (movie_id,))
    if movie:
        transformed_movie = transform_movie(movie)
        # Fetch genres for this movie
        genres = fetch_all("""
            SELECT g.Genre_Id, g.Genre_Name 
            FROM genre g
            JOIN movie_genre mg ON g.Genre_Id = mg.Genre_Id
            WHERE mg.Movie_Id = %s
        """, (movie_id,))
        transformed_movie['genres'] = [{'genre_id': g['Genre_Id'], 'name': g['Genre_Name']} for g in genres]
        return jsonify({"success": True, "movie": transformed_movie})
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
