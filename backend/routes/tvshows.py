from flask import Blueprint, jsonify
from db import fetch_all, fetch_one

tvshows_bp = Blueprint("tvshows", __name__)

# Map TV show titles to their actual TMDB poster URLs
TVSHOW_POSTERS = {
    "Breaking Bad": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg",
    "Game of Thrones": "https://image.tmdb.org/t/p/w500/1XS1oqL89opfnbLl8WnZY1O1uJx.jpg",
    "Stranger Things": "https://image.tmdb.org/t/p/w500/x2LSRK2Cm7MZhjluni1msVJ3wDF.jpg",
    "The Crown": "https://image.tmdb.org/t/p/w500/1M876KPjulVwppEpldhdc8V4o68.jpg",
    "The Mandalorian": "https://image.tmdb.org/t/p/w500/sWgBv7LV2PRoQgkxwlibdGXKz1S.jpg",
    "The Witcher": "https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg",
    "The Office": "https://image.tmdb.org/t/p/w500/qWnJzyZhyy74gjpSjIXWmuk0ifX.jpg",
    "Friends": "https://image.tmdb.org/t/p/w500/f496cm9enuEsZkSPzCwnTESEK5s.jpg",
    "Sherlock": "https://image.tmdb.org/t/p/w500/7WTsnHkbA0FaG6R9twfFde0I9hl.jpg",
    "The Boys": "https://image.tmdb.org/t/p/w500/stTEycfG9928HYGEISBFaG1ngjM.jpg",
    "Peaky Blinders": "https://image.tmdb.org/t/p/w500/vUUqzWa2LnHIVqkaKVlVGkVcZIW.jpg",
    "Dark": "https://image.tmdb.org/t/p/w500/3WR8kGGGmHVY0iE6RZZwskhk4GX.jpg",
    "The Last of Us": "https://image.tmdb.org/t/p/w500/uKvVjHNqB5VmOrdxqAt2F7J78ED.jpg",
    "Better Call Saul": "https://image.tmdb.org/t/p/w500/fC2HDm5t0kHl7mTm7jxMR31b7by.jpg",
    "Westworld": "https://image.tmdb.org/t/p/w500/8MfgyFHf7XEboZJPZXCIDqqiz6e.jpg"
}

def transform_tvshow(show):
    """Transform database TV show format to API format"""
    if not show:
        return None
    
    title = show.get("Title", "")
    poster_url = TVSHOW_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg")
    
    return {
        "tv_show_id": show.get("Show_Id"),
        "title": title,
        "description": show.get("Description"),
        "release_year": show.get("Release_Year"),
        "status": show.get("Status"),
        "age_rating": show.get("Age_Rating"),
        "average_rating": float(show.get("average_rating")) if show.get("average_rating") else 0,
        "total_seasons": 5,  # Default value
        "total_episodes": 50,  # Default value
        "poster_url": poster_url,
    }

@tvshows_bp.route("/", methods=["GET"])
def get_all_tvshows():
    shows = fetch_all("SELECT * FROM tv_show")
    transformed_shows = [transform_tvshow(s) for s in shows]
    return jsonify({"success": True, "tv_shows": transformed_shows})


@tvshows_bp.route("/<int:show_id>", methods=["GET"])
def get_tvshow_by_id(show_id):
    show = fetch_one("SELECT * FROM tv_show WHERE Show_Id = %s", (show_id,))
    if show:
        return jsonify({"success": True, "tv_show": transform_tvshow(show)})
    else:
        return jsonify({"success": False, "message": "TV Show not found"}), 404
    

@tvshows_bp.route("/genre/<string:genre_name>", methods=["GET"])
def get_tvshows_by_genre(genre_name):
    query = """
        SELECT t.* 
        FROM tv_show t
        JOIN tvshow_genre tg ON t.Show_Id = tg.Show_Id
        JOIN genre g ON tg.Genre_Id = g.Genre_Id
        WHERE g.Genre_Name = %s
    """
    shows = fetch_all(query, (genre_name,))
    transformed_shows = [transform_tvshow(s) for s in shows]
    return jsonify({"success": True, "tv_shows": transformed_shows})