from flask import Blueprint, jsonify, request
from db import get_db_connection

movies_bp = Blueprint("movies", __name__, url_prefix="/api/movies")

@movies_bp.route("/", methods=["GET"])
def get_all_movies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movie")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": movies})

@movies_bp.route("/<int:movie_id>", methods=["GET"])
def get_movie_by_id(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movie WHERE Movie_Id = %s", (movie_id,))
    movie = cursor.fetchone()
    cursor.close()
    conn.close()

    if movie:
        return jsonify({"success": True, "data": movie})
    else:
        return jsonify({"success": False, "message": "Movie not found"}), 404

@movies_bp.route("/genre/<string:genre_name>", methods=["GET"])
def get_movies_by_genre(genre_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT m.* 
        FROM movie m
        JOIN movie_genre mg ON m.Movie_Id = mg.Movie_Id
        JOIN genre g ON mg.Genre_Id = g.Genre_Id
        WHERE g.Genre_Name = %s
    """
    cursor.execute(query, (genre_name,))
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": movies})
