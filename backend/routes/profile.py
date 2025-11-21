from flask import Blueprint, request, jsonify
from db import fetch_all, execute_query, fetch_one
from utils.auth_middleware import token_required

profile_bp = Blueprint('profiles', __name__)

def transform_profile(profile):
    """Transform database profile format to API format"""
    if not profile:
        return None
    return {
        "profile_id": profile.get("Profile_Id"),
        "user_id": profile.get("User_Id"),
        "name": profile.get("Profile_Name"),
        "picture": profile.get("Profile_Picture"),
        "language": profile.get("Language_Preference"),
        "age_restriction": profile.get("Age_Restriction")
    }


@profile_bp.route("/create", methods=["POST"])
@token_required
def create_profile(current_user):
    data = request.get_json()
    profile_name = data.get("name")
    profile_picture = data.get("picture", "default_avatar.png")
    language_pref = data.get("language", "English")
    age_restriction = data.get("age_restriction", "All")

    if not profile_name:
        return jsonify({"success": False, "message": "Profile name is required"}), 400

    try:
        query = """
            INSERT INTO profile (User_Id, Profile_Name, Profile_Picture, Language_Preference, Age_Restriction)
            VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (current_user, profile_name, profile_picture, language_pref, age_restriction))
        
        # Get the newly created profile by user_id and profile_name
        new_profile = fetch_one(
            "SELECT * FROM profile WHERE User_Id = %s AND Profile_Name = %s ORDER BY Profile_Id DESC LIMIT 1",
            (current_user, profile_name)
        )
        
        if not new_profile:
            return jsonify({"success": False, "message": "Profile created but could not retrieve"}), 500
        
        return jsonify({"success": True, "message": "Profile created successfully!", "profile": transform_profile(new_profile)})
    except Exception as e:
        error_msg = str(e)
        # Check if it's the trigger error
        if "Maximum profile limit" in error_msg:
            return jsonify({"success": False, "message": "Maximum profile limit (3) reached for this user."}), 400
        return jsonify({"success": False, "message": f"Failed to create profile: {error_msg}"}), 500


@profile_bp.route("/list", methods=["GET"])
@token_required
def list_profiles(current_user):
    profiles = fetch_all("SELECT * FROM profile WHERE User_Id = %s", (current_user,))
    return jsonify({"success": True, "profiles": [transform_profile(p) for p in profiles]})


@profile_bp.route("/delete/<int:profile_id>", methods=["DELETE"])
@token_required
def delete_profile(current_user, profile_id):
    # Verify the profile belongs to the current user
    profile = fetch_one("SELECT Profile_Id FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
    if not profile:
        return jsonify({"success": False, "message": "Profile not found or not owned by user"}), 404

    execute_query("DELETE FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
    return jsonify({"success": True, "message": "Profile deleted successfully!"})


__all__ = ["profile_bp"]

