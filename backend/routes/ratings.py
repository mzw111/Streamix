from flask import Blueprint, request, jsonify
from db import execute_query, fetch_all, fetch_one
from utils.auth_middleware import token_required

ratings_bp = Blueprint('ratings', __name__)


@ratings_bp.route('/add', methods=['POST'])
@token_required
def add_rating(current_user):
    data = request.get_json()
    profile_id = data.get('profile_id')
    content_type = data.get('content_type')  # 'Movie' or 'TV_Show'
    content_id = data.get('content_id')
    rating = data.get('rating')              # int
    review_text = data.get('review_text', None)

    if not (profile_id and content_type and content_id and rating is not None):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Ensure profile belongs to the current user
    owner = fetch_one("SELECT Profile_Id FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
    if not owner:
        return jsonify({"success": False, "message": "Profile not found or not owned by user"}), 403

    query = """
        INSERT INTO rating_review (Profile_Id, Content_Type, Content_Id, Rating, Review_Text)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (profile_id, content_type, content_id, rating, review_text))
    # Trigger will update average_rating automatically
    return jsonify({"success": True, "message": "Rating submitted"})


@ratings_bp.route('/content/<string:content_type>/<int:content_id>', methods=['GET'])
def list_ratings_for_content(content_type, content_id):
    rows = fetch_all(
        "SELECT rr.*, p.Profile_Name FROM rating_review rr JOIN profile p ON rr.Profile_Id = p.Profile_Id WHERE rr.Content_Type = %s AND rr.Content_Id = %s ORDER BY rr.Review_Date DESC",
        (content_type, content_id),
    )
    return jsonify({"success": True, "ratings": rows})


@ratings_bp.route('/profile/<int:profile_id>', methods=['GET'])
@token_required
def list_profile_ratings(current_user, profile_id):
    # Ensure profile belongs to current user
    owner = fetch_one("SELECT Profile_Id FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
    if not owner:
        return jsonify({"success": False, "message": "Profile not found or not owned by user"}), 403

    rows = fetch_all("SELECT * FROM rating_review WHERE Profile_Id = %s ORDER BY Review_Date DESC", (profile_id,))
    return jsonify({"success": True, "ratings": rows})
