from flask import Blueprint, jsonify
from db import fetch_all

home_page_bp = Blueprint('home_page', __name__)

# Poster mappings for movies and TV shows
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
}

TVSHOW_POSTERS = {
    "Breaking Bad": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg",
    "Game of Thrones": "https://image.tmdb.org/t/p/w500/1XS1oqL89opfnbLl8WnZY1O1uJx.jpg",
    "Stranger Things": "https://image.tmdb.org/t/p/w500/x2LSRK2Cm7MZhjluni1msVJ3wDF.jpg",
}

def transform_home_content(item):
    """Transform database format to API format with poster"""
    if not item:
        return None
    
    title = item.get("Title", "")
    content_type = item.get("Content_Type", "")
    
    # Get poster based on content type and title
    if content_type == "Movie":
        poster_url = MOVIE_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg")
    else:
        poster_url = TVSHOW_POSTERS.get(title, "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg")
    
    return {
        "content_id": item.get("Content_Id"),
        "content_type": content_type,
        "title": title,
        "description": item.get("Description"),
        "release_date": str(item.get("Release_Date")) if item.get("Release_Date") else None,
        "language": item.get("Language"),
        "age_rating": item.get("Age_Rating"),
        "rating": float(item.get("average_rating")) if item.get("average_rating") else 0,
        "poster_url": poster_url
    }


@home_page_bp.route('/', methods=['GET'])
def get_home_page_content():
    """
    Returns content from home_page table with titles from movie/tv_show tables
    """
    query = """
        SELECT hp.Content_Id, hp.Content_Type, hp.Release_Date, hp.Language, hp.Age_Rating,
               CASE 
                   WHEN hp.Content_Type = 'Movie' THEN m.Title
                   WHEN hp.Content_Type = 'TV_Show' THEN t.Title
               END AS Title,
               CASE 
                   WHEN hp.Content_Type = 'Movie' THEN m.Description
                   WHEN hp.Content_Type = 'TV_Show' THEN t.Description
               END AS Description,
               CASE 
                   WHEN hp.Content_Type = 'Movie' THEN m.average_rating
                   WHEN hp.Content_Type = 'TV_Show' THEN t.average_rating
               END AS average_rating
        FROM home_page hp
        LEFT JOIN movie m ON hp.Content_Type = 'Movie' AND hp.Content_Id = m.Movie_Id
        LEFT JOIN tv_show t ON hp.Content_Type = 'TV_Show' AND hp.Content_Id = t.Show_Id
        ORDER BY hp.Release_Date DESC
    """
    content = fetch_all(query)
    return jsonify({"success": True, "content": [transform_home_content(c) for c in content]})
