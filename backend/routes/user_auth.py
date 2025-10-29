
from flask import Blueprint, request, jsonify
from db import fetch_all, execute_query
import bcrypt
import jwt
import datetime

user_bp = Blueprint('user', __name__)


SECRET_KEY = "supersecretkey123"  



@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    dob = data.get("dob")
    country = data.get("country")

   
    existing_user = fetch_all("SELECT * FROM user WHERE Email = %s", (email,))
    if existing_user:
        return jsonify({"success": False, "message": "User already exists!"}), 400

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


    query = "INSERT INTO user (Name, DOB, Country, Email) VALUES (%s, %s, %s, %s)"
    execute_query(query, (name, dob, country, email))

  
    execute_query("UPDATE user SET Password = %s WHERE Email = %s", (hashed_pw, email))

    return jsonify({"success": True, "message": "User registered successfully!"})


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = fetch_all("SELECT * FROM user WHERE Email = %s", (email,))
    if not user:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

    user = user[0]


    if not bcrypt.checkpw(password.encode("utf-8"), user["Password"].encode("utf-8")):
        return jsonify({"success": False, "message": "Invalid email or password"}), 401


    token = jwt.encode(
        {
            "user_id": user["User_Id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "success": True,
        "message": "Login successful!",
        "token": token,
        "user": {
            "id": user["User_Id"],
            "name": user["Name"],
            "email": user["Email"]
        }
    })



@user_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"success": True, "message": "User logged out successfully!"})