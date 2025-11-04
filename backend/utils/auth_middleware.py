from functools import wraps
from flask import request, jsonify
import jwt
import os

# Use the same secret as in user_auth.py
SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"success": False, "message": "Missing token"}), 401

        try:
            decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = decoded_data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token"}), 401

        # Pass the user id from token to the route
        return f(current_user, *args, **kwargs)

    return decorated
