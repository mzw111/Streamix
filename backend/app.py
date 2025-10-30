from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os 
from routes.user_auth import user_bp
from routes.profile import profile_bp
from routes.watchlist import watchlist_bp
from routes.movies import movies_bp
from routes.tvshows import tvshows_bp
app = Flask(__name__)
CORS(app)  

app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(profile_bp, url_prefix="/api/profile") 
app.register_blueprint(watchlist_bp, url_prefix="/api/watchlist")
app.register_blueprint(movies_bp, url_prefix="/api/movies")
app.register_blueprint(tvshows_bp, url_prefix="/api/tvshows")

if __name__ == '__main__':
    
    app.run(port=3001, debug=True)