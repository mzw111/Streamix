from flask import Blueprint, request, jsonify
from db import execute_query, fetch_query, call_procedure, fetch_one
from utils.auth_middleware import token_required

watchlist_bp = Blueprint('watchlist', __name__)

# Poster mappings
MOVIE_POSTERS = {
    "The Dark Knight": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "Inception": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    "The Shawshank Redemption": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
    "Pulp Fiction": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
    "The Godfather": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Interstellar": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "The Matrix": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "Forrest Gump": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
}

TVSHOW_POSTERS = {
    "Breaking Bad": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg",
    "Game of Thrones": "https://image.tmdb.org/t/p/w500/1XS1oqL89opfnbLl8WnZY1O1uJx.jpg",
    "Stranger Things": "https://image.tmdb.org/t/p/w500/x2LSRK2Cm7MZhjluni1msVJ3wDF.jpg",
}

def transform_watchlist_item(item):
    """Transform database format to API format with poster"""
    if not item:
        return None
    
    title = item.get("Title", "")
    content_type = item.get("Content_Type", "")
    
    # Get poster based on content type
    if content_type == "Movie":
        poster_url = MOVIE_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg")
    else:
        poster_url = TVSHOW_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg")
    
    return {
        "watchlist_id": item.get("Watchlist_Id"),
        "content_type": content_type,
        "content_id": item.get("Content_Id"),
        "title": title,
        "date_added": str(item.get("Date_Added")) if item.get("Date_Added") else None,
        "poster_url": poster_url
    }

@watchlist_bp.route("/add", methods=["POST"])
@token_required
def add_to_watchlist(current_user):
    data = request.get_json()
    profile_id = data.get("profile_id")
    content_type = data.get("content_type")
    content_id = data.get("content_id")

    print(f"Watchlist add request - User: {current_user}, Data: {data}")
    print(f"profile_id: {profile_id} (type: {type(profile_id)})")
    print(f"content_type: {content_type} (type: {type(content_type)})")
    print(f"content_id: {content_id} (type: {type(content_id)})")

    if not (profile_id and content_type and content_id):
        print(f"Missing fields! profile_id={profile_id}, content_type={content_type}, content_id={content_id}")
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Ensure profile belongs to current user
    owner = fetch_one("SELECT Profile_Id FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
    if not owner:
        return jsonify({"success": False, "message": "Profile not found or not owned by user"}), 403

    # Use stored procedure to add to watchlist
    try:
        call_procedure('sp_AddToWatchlist', (int(profile_id), content_type, int(content_id)))
        return jsonify({"success": True, "message": "Added to watchlist via procedure"})
    except Exception as e:
        print(f"Error adding to watchlist: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


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
               END AS Title,
               CASE 
                   WHEN w.Content_Type = 'Movie' THEN m.Movie_Id
                   ELSE NULL
               END AS Movie_Id,
               CASE 
                   WHEN w.Content_Type = 'TV_Show' THEN t.Show_Id
                   ELSE NULL
               END AS Show_Id,
               CASE 
                   WHEN w.Content_Type = 'Movie' THEN m.average_rating
                   WHEN w.Content_Type = 'TV_Show' THEN t.average_rating
               END AS average_rating,
               CASE 
                   WHEN w.Content_Type = 'Movie' THEN m.Release_Date
                   ELSE NULL
               END AS Release_Date,
               CASE 
                   WHEN w.Content_Type = 'Movie' THEN m.Duration
                   ELSE NULL
               END AS Duration
        FROM watchlist w
        LEFT JOIN movie m ON w.Content_Type = 'Movie' AND w.Content_Id = m.Movie_Id
        LEFT JOIN tv_show t ON w.Content_Type = 'TV_Show' AND w.Content_Id = t.Show_Id
        WHERE w.Profile_Id = %s
        ORDER BY w.Date_Added DESC
    """
    results = fetch_query(query, (profile_id,))
    transformed = []
    for r in results:
        item = transform_watchlist_item(r)
        # Add movie_id or tv_show_id for frontend
        if r.get("Movie_Id"):
            item["movie_id"] = r.get("Movie_Id")
            item["average_rating"] = float(r.get("average_rating", 0)) if r.get("average_rating") else 0
            item["release_year"] = r.get("Release_Date").year if r.get("Release_Date") else None
            item["duration"] = r.get("Duration")
        elif r.get("Show_Id"):
            item["tv_show_id"] = r.get("Show_Id")
            item["average_rating"] = float(r.get("average_rating", 0)) if r.get("average_rating") else 0
        transformed.append(item)
    return jsonify({"success": True, "watchlist": transformed})

