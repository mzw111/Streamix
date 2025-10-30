from flask import Blueprint, jsonify, request
from db import get_db_connection

tvshows_bp = Blueprint("tvshows", __name__, url_prefix="/api/tvshows")


@tvshows_bp.route("/", methods=["GET"])
def get_all_tvshows():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tv_show")
    shows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": shows})


@tvshows_bp.route("/<int:show_id>", methods=["GET"])
def get_tvshow_by_id(show_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tv_show WHERE Show_Id = %s", (show_id,))
    show = cursor.fetchone()
    cursor.close()
    conn.close()

    if show:
        return jsonify({"success": True, "data": show})
    else:
        return jsonify({"success": False, "message": "TV Show not found"}), 404
    

@tvshows_bp.route("/genre/<string:genre_name>", methods=["GET"])
def get_tvshows_by_genre(genre_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT t.* 
        FROM tv_show t
        JOIN tvshow_genre tg ON t.Show_Id = tg.Show_Id
        JOIN genre g ON tg.Genre_Id = g.Genre_Id
        WHERE g.Genre_Name = %s
    """
    cursor.execute(query, (genre_name,))
    shows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": shows})