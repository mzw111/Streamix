from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os 
from routes.user_auth import user_bp


app = Flask(__name__)
CORS(app)  

app.register_blueprint(user_bp, url_prefix="/api/user")

if __name__ == '__main__':
    
    app.run(port=3001, debug=True)