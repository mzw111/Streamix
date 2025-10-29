from flask import Blueprint, request, jsonify
from db import fetch_all, execute_query
import jwt

profile_bp = Blueprint('profiles', __name__)

SECRET_KEY = "supersecretkey123"  


def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data["user_id"]
    except:
        return None
    
@profile_bp.route("/create", methods=["POST"])
def create_profile():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Missing token"}), 401

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"success": False, "message": "Invalid or expired token"}), 401

    data = request.get_json()
    profile_name = data.get("name")
    profile_picture = data.get("picture", "default_avatar.png")
    language_pref = data.get("language", "English")
    age_restriction = data.get("age_restriction", "All")

    query = """
        INSERT INTO profile (User_Id, Profile_Name, Profile_Picture, Language_Preference, Age_Restriction)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (user_id, profile_name, profile_picture, language_pref, age_restriction))

    return jsonify({"success": True, "message": "Profile created successfully!"})


@profile_bp.route("/list", methods=["GET"])
def list_profiles():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Missing token"}), 401

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"success": False, "message": "Invalid or expired token"}), 401

    profiles = fetch_all("SELECT * FROM profile WHERE User_Id = %s", (user_id,))
    return jsonify({"success": True, "profiles": profiles})




@profile_bp.route("/delete/<int:profile_id>", methods=["DELETE"])
def delete_profile(profile_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Missing token"}), 401

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"success": False, "message": "Invalid or expired token"}), 401

    execute_query("DELETE FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, user_id))
    return jsonify({"success": True, "message": "Profile deleted successfully!"})


__all__ = ["profile_bp"]
