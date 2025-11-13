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
        "profile_name": profile.get("Profile_Name"),
        "name": profile.get("Profile_Name"),
        "picture": profile.get("Profile_Picture"),
        "language": profile.get("Language_Preference"),
        "age_restriction": profile.get("Age_Restriction")
    }

@profile_bp.route("/create", methods=["POST"])
@token_required
def create_profile(current_user):
    try:
        data = request.get_json()
        profile_name = data.get("name")
        
        if not profile_name or not profile_name.strip():
            return jsonify({"success": False, "message": "Profile name is required"}), 400
        
        profile_picture = data.get("picture", "default_avatar.png")
        language_pref = data.get("language", "English")
        age_restriction = data.get("age_restriction", "All")
        
        # Check current profile count (enforce 3-profile limit)
        count_query = "SELECT COUNT(*) as count FROM profile WHERE User_Id = %s"
        count_result = fetch_one(count_query, (current_user,))
        
        if count_result and count_result.get('count', 0) >= 3:
            return jsonify({"success": False, "message": "Maximum profile limit (3) reached for this user"}), 400
        
        # Insert new profile
        insert_query = """
            INSERT INTO profile (User_Id, Profile_Name, Profile_Picture, Language_Preference, Age_Restriction)
            VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(insert_query, (current_user, profile_name.strip(), profile_picture, language_pref, age_restriction))
        
        # Get the newly created profile using the name and user_id (more reliable than LAST_INSERT_ID)
        new_profile = fetch_one(
            "SELECT * FROM profile WHERE User_Id = %s AND Profile_Name = %s ORDER BY Profile_Id DESC LIMIT 1",
            (current_user, profile_name.strip())
        )
        
        if not new_profile:
            return jsonify({"success": False, "message": "Profile created but failed to retrieve"}), 500
        
        return jsonify({
            "success": True, 
            "message": "Profile created successfully!", 
            "profile": transform_profile(new_profile)
        }), 201
        
    except Exception as e:
        print(f"Error creating profile: {str(e)}")
        return jsonify({"success": False, "message": f"Failed to create profile: {str(e)}"}), 500

@profile_bp.route("/list", methods=["GET"])
@token_required
def list_profiles(current_user):
    try:
        profiles = fetch_all("SELECT * FROM profile WHERE User_Id = %s ORDER BY Profile_Id ASC", (current_user,))
        return jsonify({
            "success": True, 
            "profiles": [transform_profile(p) for p in profiles if p]
        }), 200
    except Exception as e:
        print(f"Error listing profiles: {str(e)}")
        return jsonify({"success": False, "message": "Failed to load profiles"}), 500

@profile_bp.route("/delete/<int:profile_id>", methods=["DELETE"])
@token_required
def delete_profile(current_user, profile_id):
    try:
        # Verify the profile belongs to the current user
        profile = fetch_one("SELECT Profile_Id FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
        if not profile:
            return jsonify({"success": False, "message": "Profile not found or not owned by user"}), 404

        execute_query("DELETE FROM profile WHERE Profile_Id = %s AND User_Id = %s", (profile_id, current_user))
        return jsonify({"success": True, "message": "Profile deleted successfully!"}), 200
        
    except Exception as e:
        print(f"Error deleting profile: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete profile"}), 500

__all__ = ["profile_bp"]
