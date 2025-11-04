from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os 
from routes.user_auth import user_bp
from routes.users import users_bp
from routes.profile import profile_bp
from routes.watchlist import watchlist_bp
from routes.movies import movies_bp
from routes.tvshows import tvshows_bp
from routes.subscriptions import subscriptions_bp
from routes.ratings import ratings_bp
from routes.viewing_history import viewing_history_bp
from routes.genres import genres_bp
from routes.home_page import home_page_bp
from routes.payments import payments_bp

app = Flask(__name__)
CORS(app)  

# Register all blueprints with URL prefixes
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(profile_bp, url_prefix="/api/profile") 
app.register_blueprint(watchlist_bp, url_prefix="/api/watchlist")
app.register_blueprint(movies_bp, url_prefix="/api/movies")
app.register_blueprint(tvshows_bp, url_prefix="/api/tvshows")
app.register_blueprint(subscriptions_bp, url_prefix="/api/subscriptions")
app.register_blueprint(ratings_bp, url_prefix="/api/ratings")
app.register_blueprint(viewing_history_bp, url_prefix="/api/viewing_history")
app.register_blueprint(genres_bp, url_prefix="/api/genres")
app.register_blueprint(home_page_bp, url_prefix="/api/home")
app.register_blueprint(payments_bp, url_prefix="/api/payments")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"success": True, "message": "Streamix API is running"})

if __name__ == '__main__':
    
    app.run(port=3001, debug=True)