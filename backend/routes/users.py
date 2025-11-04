from flask import Blueprint, request, jsonify
from db import fetch_one, execute_query
from utils.auth_middleware import token_required
import bcrypt

users_bp = Blueprint('users', __name__)


@users_bp.route('/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    """Get current user's profile information"""
    user = fetch_one("SELECT User_Id, Name, DOB, Country, Email FROM user WHERE User_Id = %s", (current_user,))
    if user:
        return jsonify({"success": True, "user": user})
    else:
        return jsonify({"success": False, "message": "User not found"}), 404


@users_bp.route('/update', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    """Update user profile information"""
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')
    country = data.get('country')

    updates = []
    params = []

    if name:
        updates.append("Name = %s")
        params.append(name)
    if dob:
        updates.append("DOB = %s")
        params.append(dob)
    if country:
        updates.append("Country = %s")
        params.append(country)

    if not updates:
        return jsonify({"success": False, "message": "No fields to update"}), 400

    params.append(current_user)
    query = f"UPDATE user SET {', '.join(updates)} WHERE User_Id = %s"
    execute_query(query, tuple(params))
    
    return jsonify({"success": True, "message": "User profile updated successfully"})


@users_bp.route('/change-password', methods=['PUT'])
@token_required
def change_password(current_user):
    """Change user password"""
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not (old_password and new_password):
        return jsonify({"success": False, "message": "Both old and new password required"}), 400

    # Verify old password
    user = fetch_one("SELECT Password FROM user WHERE User_Id = %s", (current_user,))
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    if not bcrypt.checkpw(old_password.encode("utf-8"), user["Password"].encode("utf-8")):
        return jsonify({"success": False, "message": "Old password is incorrect"}), 401

    # Hash new password
    hashed_pw = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    execute_query("UPDATE user SET Password = %s WHERE User_Id = %s", (hashed_pw, current_user))

    return jsonify({"success": True, "message": "Password changed successfully"})
