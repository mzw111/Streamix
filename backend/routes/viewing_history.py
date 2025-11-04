from flask import Blueprint, request, jsonify
from db import execute_query, fetch_all, fetch_one, call_procedure
from utils.auth_middleware import token_required

viewing_history_bp = Blueprint('viewing_history', __name__)


@viewing_history_bp.route('/log', methods=['POST'])
@token_required
def log_viewing(current_user):
    data = request.get_json()
    profile_id = data.get('profile_id')
    content_type = data.get('content_type')  # 'Movie' or 'TV_Show'
    content_id = data.get('content_id')
    watch_duration = data.get('watch_duration')  # in minutes

    if not (profile_id and content_type and content_id):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Ensure profile belongs to the current user
    owner = fetch_one("SELECT Profile_Id FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
    if not owner:
        return jsonify({"success": False, "message": "Profile not found or not owned by user"}), 403

    query = """
        INSERT INTO viewing_history (Profile_Id, Content_Type, Content_Id, Watch_Duration)
        VALUES (%s, %s, %s, %s)
    """
    execute_query(query, (profile_id, content_type, content_id, watch_duration))
    return jsonify({"success": True, "message": "Viewing logged"})


@viewing_history_bp.route('/profile/<int:profile_id>', methods=['GET'])
@token_required
def get_viewing_history(current_user, profile_id):
    # Ensure profile belongs to current user
    owner = fetch_one("SELECT Profile_Id FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
    if not owner:
        return jsonify({"success": False, "message": "Profile not found or not owned by user"}), 403

    # Use stored procedure to get watch history
    try:
        results = call_procedure('sp_GetWatchHistory', (profile_id,))
        return jsonify({"success": True, "history": results})
    except Exception as e:
        # Fallback to direct query if procedure doesn't exist
        query = """
            SELECT vh.*, 
                   CASE 
                       WHEN vh.Content_Type = 'Movie' THEN m.Title
                       WHEN vh.Content_Type = 'TV_Show' THEN t.Title
                   END AS Title
            FROM viewing_history vh
            LEFT JOIN movie m ON vh.Content_Type = 'Movie' AND vh.Content_Id = m.Movie_Id
            LEFT JOIN tv_show t ON vh.Content_Type = 'TV_Show' AND vh.Content_Id = t.Show_Id
            WHERE vh.Profile_Id = %s
        ORDER BY vh.Watch_Date DESC
    """
    rows = fetch_all(query, (profile_id,))
    return jsonify({"success": True, "viewing_history": rows})


@viewing_history_bp.route('/delete/<int:history_id>', methods=['DELETE'])
@token_required
def delete_viewing_entry(current_user, history_id):
    # Verify the history entry belongs to a profile owned by current user
    entry = fetch_one("""
        SELECT vh.History_Id 
        FROM viewing_history vh
        JOIN profile p ON vh.Profile_Id = p.Profile_Id
        WHERE vh.History_Id = %s AND p.User_Id = %s
    """, (history_id, current_user))
    
    if not entry:
        return jsonify({"success": False, "message": "History entry not found or not owned by user"}), 404

    execute_query("DELETE FROM viewing_history WHERE History_Id = %s", (history_id,))
    return jsonify({"success": True, "message": "History entry deleted"})
