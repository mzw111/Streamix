# 🎬 Streamix - Streaming Platform

A full-stack streaming platform built with React, Flask, and MySQL featuring advanced database management with stored procedures, triggers, and functions.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Database Architecture](#-database-architecture)
- [Project Structure](#-project-structure)
- [Setup Instructions](#-setup-instructions)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Database Objects](#-database-objects)

## ✨ Features

### User Features
- **Authentication & Authorization**: JWT-based secure authentication
- **Multi-Profile Support**: Create and manage multiple user profiles
- **Content Library**: Browse 20+ movies and 15+ TV shows with unique posters
- **Watchlist**: Add/remove content to personal watchlist per profile
- **Viewing History**: Track and view complete watch history
- **Ratings & Reviews**: Rate content and trigger automatic average rating updates
- **Search & Filter**: Search content by title and filter by genre
- **Subscription Management**: Check subscription status and plan details

### Technical Features
- **Stored Procedures**: 5 custom procedures for watchlist, recommendations, payments, and history
- **Database Functions**: 2 functions for subscription status and watch time calculations
- **Database Triggers**: 3 triggers for automatic rating updates
- **Dark Theme UI**: Modern purple-themed responsive interface
- **Real-time Updates**: Automatic rating calculations on review submissions

## 🛠 Tech Stack

### Frontend
- **React** 19.2.0
- **React Router** 6.20.0
- **Axios** 1.6.2
- **CSS3** with custom dark purple theme

### Backend
- **Flask** 3.0.0
- **MySQL** 8.0+
- **JWT** (PyJWT)
- **Flask-CORS**
- **mysql-connector-python**

### Database
- **MySQL 8.0+**
- 12 tables with proper relationships
- 5 stored procedures
- 2 custom functions
- 3 triggers

## 🗄 Database Architecture

### Tables
1. **user** - User accounts
2. **profile** - User profiles (multiple per user)
3. **subscription** - Subscription plans and status
4. **movie** - Movie catalog (20 movies)
5. **tv_show** - TV show catalog (15 shows)
6. **genre** - Genre categories (17 genres)
7. **watchlist** - User's watchlist
8. **rating_review** - Ratings and reviews
9. **viewing_history** - Watch history tracking
10. **home_page** - Featured content
11. **payment** - Payment records
12. **movie_genre** & **tvshow_genre** - Many-to-many relationships

### Database Objects

#### Stored Procedures
- **sp_AddToWatchlist**: Add content to watchlist with duplicate prevention
- **sp_RemoveFromWatchlist**: Remove content from watchlist
- **sp_GetWatchHistory**: Retrieve complete viewing history
- **sp_GetRecommendations**: Get personalized recommendations
- **sp_ProcessPayment**: Process subscription payments

#### Functions
- **fn_GetSubscriptionStatus**: Check user subscription status (Active/Expired/Inactive)
- **fn_GetTotalWatchTime**: Calculate total watch time for a profile

#### Triggers
- **trg_UpdateMovieRating**: Update movie average rating on new review (INSERT)
- **trg_UpdateRatingOnUpdate**: Update rating when review is modified (UPDATE)
- **trg_UpdateAverageRating**: Recalculate average rating on review changes

## 📁 Project Structure

```
streamix/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── db.py                     # Database connection pool
│   ├── requirements.txt          # Python dependencies
│   ├── routes/
│   │   ├── movies.py            # Movie endpoints
│   │   ├── tvshows.py           # TV show endpoints
│   │   ├── user_auth.py         # Authentication
│   │   ├── profile.py           # Profile management
│   │   ├── watchlist.py         # Watchlist operations (uses procedures)
│   │   ├── subscriptions.py     # Subscription management (uses functions)
│   │   └── users.py             # User management
│   └── utils/
│       └── auth_middleware.py   # JWT middleware
├── frontend/
│   └── my-app/
│       ├── package.json
│       ├── public/
│       └── src/
│           ├── pages/           # 7 main pages
│           │   ├── Home.js
│           │   ├── Login.js
│           │   ├── Signup.js
│           │   ├── Profiles.js
│           │   ├── Movies.js
│           │   ├── TVShows.js
│           │   └── Watchlist.js
│           ├── components/      # 5 reusable components
│           │   ├── Navbar.js
│           │   ├── MovieCard.js
│           │   ├── SearchBar.js
│           │   ├── GenreFilter.js
│           │   └── ProfileCard.js
│           └── services/
│               └── api.js       # Axios API client
├── database_objects.sql         # All procedures, functions, triggers
├── DATABASE_FEATURES.md         # Detailed database documentation
└── TESTING_RESULTS.md          # Comprehensive test results

```

## 🚀 Setup Instructions

### Prerequisites
- **Node.js** 14+ and npm
- **Python** 3.8+
- **MySQL** 8.0+
- **Git**

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd streamix
```

### 2. Database Setup
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE streamingdb;
USE streamingdb;

# Import schema (run your schema file)
source path/to/your/schema.sql;

# Create database objects
source database_objects.sql;
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Update db.py with your MySQL credentials
# Edit db.py and set:
# host="localhost"
# user="root"
# password="your_password"
# database="streamingdb"

# Run Flask server
python app.py
# Server runs on http://127.0.0.1:3001
```

### 4. Frontend Setup
```bash
cd frontend/my-app

# Install dependencies
npm install

# Run development server
npm start
# Server runs on http://localhost:3000
```

### 5. Access Application
- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:3001/api
- Default test credentials:
  - Email: `user1@example.com`
  - Password: (check your database)

## 📡 API Documentation

### Authentication
```
POST /api/user/register    # Register new user
POST /api/user/login       # Login user (returns JWT)
GET  /api/user/info        # Get user info (requires JWT)
```

### Content
```
GET  /api/movies/          # Get all movies
GET  /api/movies/<id>      # Get movie by ID
GET  /api/tvshows/         # Get all TV shows
GET  /api/tvshows/<id>     # Get TV show by ID
GET  /api/home/            # Get featured content
```

### Profile
```
GET  /api/profile/list     # Get user's profiles
POST /api/profile/create   # Create new profile
GET  /api/profile/<id>     # Get profile details
```

### Watchlist (Uses Stored Procedures)
```
GET    /api/watchlist/all/<profile_id>           # Get watchlist
POST   /api/watchlist/add                        # Add to watchlist (calls sp_AddToWatchlist)
DELETE /api/watchlist/remove/<watchlist_id>      # Remove from watchlist (calls sp_RemoveFromWatchlist)
```

### Subscriptions (Uses Functions)
```
GET  /api/subscriptions/status     # Get subscription status (uses fn_GetSubscriptionStatus)
GET  /api/subscriptions/plans      # Get available plans
POST /api/subscriptions/subscribe  # Subscribe to plan
```

### Search & Filter
```
GET  /api/search?query=<text>           # Search movies/TV shows
GET  /api/movies/genre/<genre_name>     # Filter movies by genre
GET  /api/tvshows/genre/<genre_name>    # Filter TV shows by genre
```

## 🧪 Testing

### Database Objects Testing

All database objects have been thoroughly tested. See `TESTING_RESULTS.md` for detailed results.

#### Quick Test Commands

**Test Stored Procedure**:
```sql
-- Add to watchlist
CALL sp_AddToWatchlist(2, 'Movie', 4);
SELECT * FROM watchlist WHERE Profile_Id = 2;
```

**Test Function**:
```sql
-- Check subscription status
SELECT fn_GetSubscriptionStatus(1);
```

**Test Trigger**:
```sql
-- Insert rating (trigger auto-updates average)
INSERT INTO rating_review (User_Id, Movie_Id, Rating, Review_Text) 
VALUES (1, 26, 9.5, 'Great movie!');

SELECT average_rating FROM movie WHERE Movie_Id = 26;
```

#### Run Test Scripts
```bash
cd backend

# Test all database features
python test_all_database_features.py

# Test specific trigger
python test_rating_trigger.py

# Verify all objects exist
python verify_database_objects.py
```

### Frontend Testing
1. Navigate to http://localhost:3000
2. Register a new account or login
3. Create a profile
4. Browse movies/TV shows
5. Add items to watchlist
6. Rate content and verify average rating updates

## 🔧 Database Objects

For complete documentation of all stored procedures, functions, and triggers, see:
- **DATABASE_FEATURES.md** - Detailed feature documentation
- **TESTING_RESULTS.md** - Test results and SQL examples
- **database_objects.sql** - Complete SQL source code

### Key Database Objects

**Watchlist Management**:
- `sp_AddToWatchlist` - Prevents duplicates, auto-timestamps
- `sp_RemoveFromWatchlist` - Safe removal with validation

**Recommendations**:
- `sp_GetRecommendations` - Genre-based recommendations from watch history

**Subscription**:
- `fn_GetSubscriptionStatus` - Returns Active/Expired/Inactive
- `sp_ProcessPayment` - Complete payment processing workflow

**Rating System**:
- `trg_UpdateMovieRating` - Auto-calculates average on INSERT
- `trg_UpdateRatingOnUpdate` - Recalculates on UPDATE
- Uses DECIMAL(3,1) for 0.0-10.0 rating scale

## 📝 Notes

- All API endpoints require JWT token except `/register` and `/login`
- Database uses PascalCase column names (Movie_Id, Title, etc.)
- Backend transforms responses to snake_case for frontend
- Poster URLs use TMDB image CDN
- Dark purple theme: `#1a0033` background, `#9b59b6` accents

## 👥 Contributors

- Database Design & Schema
- Backend API Development
- Frontend React Implementation
- Database Objects & Triggers

## 📄 License

This project is for educational purposes.

---

**Built with ❤️ using React, Flask, and MySQL**