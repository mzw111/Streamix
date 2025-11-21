from flask import Blueprint, request, jsonify
from db import execute_query, fetch_all, fetch_one, call_procedure
from utils.auth_middleware import token_required

viewing_history_bp = Blueprint('viewing_history', __name__)

# Poster mappings
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

TVSHOW_POSTERS = {
    "Breaking Bad": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg",
    "Better Call Saul": "https://image.tmdb.org/t/p/w500/fC2HDm5t0kHl7mTm7jxMR31b7by.jpg",
    "The Crown": "https://image.tmdb.org/t/p/w500/1M876KPjulVwppEpldhdc8V4o68.jpg",
    "Stranger Things": "https://image.tmdb.org/t/p/w500/x2LSRK2Cm7MZhjluni1msVJ3wDF.jpg",
    "Black Mirror": "https://image.tmdb.org/t/p/w500/5UaYsGZOFhjFDwQix4jKEo3f8oN.jpg",
    "Game of Thrones": "https://image.tmdb.org/t/p/w500/1XS1oqL89opfnbLl8WnZY1O1uJx.jpg",
}


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
        # Add poster URLs to results
        for item in results:
            title = item.get('Title', '')
            content_type = item.get('Content_Type', '')
            if content_type == 'Movie':
                item['poster_url'] = MOVIE_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg")
            else:
                item['poster_url'] = TVSHOW_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg")
        return jsonify({"success": True, "history": results})
    except Exception as e:
        print(f"Stored procedure error: {e}, using fallback query")
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
        # Add poster URLs to results
        for item in rows:
            title = item.get('Title', '')
            content_type = item.get('Content_Type', '')
            if content_type == 'Movie':
                item['poster_url'] = MOVIE_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg")
            else:
                item['poster_url'] = TVSHOW_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg")
        return jsonify({"success": True, "history": rows})


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
