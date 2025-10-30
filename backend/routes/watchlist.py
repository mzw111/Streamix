from flask import Blueprint, request, jsonify
from db import execute_query, fetch_query
from utils.auth_middleware import token_required

watchlist_bp = Blueprint('watchlist', __name__)

@watchlist_bp.route("/add", methods=["POST"])
@token_required
def add_to_watchlist(current_user):
    data = request.get_json()
    profile_id = data.get("profile_id")
    content_type = data.get("content_type")
    content_id = data.get("content_id")

    if not (profile_id and content_type and content_id):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    query = """
        INSERT INTO watchlist (Profile_Id, Content_Type, Content_Id)
        VALUES (%s, %s, %s)
    """
    execute_query(query, (profile_id, content_type, content_id))
    return jsonify({"success": True, "message": "Added to watchlist"})


@watchlist_bp.route("/remove", methods=["DELETE"])
@token_required
def remove_from_watchlist(current_user):
    data = request.get_json()
    profile_id = data.get("profile_id")
    content_type = data.get("content_type")
    content_id = data.get("content_id")

    if not (profile_id and content_type and content_id):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    query = """
        DELETE FROM watchlist 
        WHERE Profile_Id = %s AND Content_Type = %s AND Content_Id = %s
    """
    execute_query(query, (profile_id, content_type, content_id))
    return jsonify({"success": True, "message": "Removed from watchlist"})


@watchlist_bp.route("/all/<int:profile_id>", methods=["GET"])
@token_required
def get_watchlist(current_user, profile_id):
    query = """
        SELECT w.Watchlist_Id, w.Content_Type, w.Content_Id, w.Date_Added,
               CASE 
                   WHEN w.Content_Type = 'Movie' THEN m.Title
                   WHEN w.Content_Type = 'TV_Show' THEN t.Title
               END AS Title
        FROM watchlist w
        LEFT JOIN movie m ON w.Content_Type = 'Movie' AND w.Content_Id = m.Movie_Id
        LEFT JOIN tv_show t ON w.Content_Type = 'TV_Show' AND w.Content_Id = t.Show_Id
        WHERE w.Profile_Id = %s
        ORDER BY w.Date_Added DESC
    """
    results = fetch_query(query, (profile_id,))
    return jsonify({"success": True, "watchlist": results})

