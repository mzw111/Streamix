from flask import Blueprint, jsonify
from db import fetch_all

genres_bp = Blueprint('genres', __name__)


@genres_bp.route('/', methods=['GET'])
def get_all_genres():
    genres = fetch_all("SELECT * FROM genre ORDER BY Genre_Name")
    return jsonify({"success": True, "genres": genres})


@genres_bp.route('/<int:genre_id>', methods=['GET'])
def get_genre_by_id(genre_id):
    genre = fetch_all("SELECT * FROM genre WHERE Genre_Id = %s", (genre_id,))
    if genre:
        return jsonify({"success": True, "genre": genre[0]})
    else:
        return jsonify({"success": False, "message": "Genre not found"}), 404
