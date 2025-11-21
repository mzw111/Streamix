# 🎬 Streamix - Streaming Platform

A full-stack Netflix-like streaming platform built with React, Flask, and MySQL featuring user authentication, profile management, video playback, watchlists, viewing history, ratings, and subscription management.


---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Objects](#database-objects)
- [Project Structure](#project-structure)

---

## 🎯 Project Overview

Streamix is a comprehensive streaming platform that allows users to:
- Browse and search movies and TV shows by genre
- Watch video content with integrated player
- Create multiple profiles per account (max 3, enforced by database trigger)
- Manage personal watchlists with stored procedures
- Track viewing history automatically on video playback
- Rate and review content with automatic average calculation
- Subscribe to different plans (Basic, Standard, Premium)
- View personalized home page with featured content

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  React Frontend │ ◄─────► │  Flask Backend  │ ◄─────► │  MySQL Database │
│  (Port 3002)    │  HTTP   │  (Port 3001)    │   SQL   │  (Port 3306)    │
│                 │  /API   │                 │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Component Flow

1. **Frontend (React)**: User interface with video player, routing, and state management
2. **Backend (Flask)**: REST API with JWT authentication and connection pooling (30 connections)
3. **Database (MySQL)**: Relational data with stored procedures, functions, and triggers

---

## ✨ Features

### User Management
- **Authentication**: Secure login/signup with JWT tokens and bcrypt password hashing
- **Profiles**: Multiple profiles per user (max 3, enforced by trigger)
- **Subscriptions**: Basic, Standard, and Premium plans with status tracking

### Content Features
- **Video Player**: Integrated video playback with progress tracking
- **Browse**: Movies and TV shows with genre filtering
- **Search**: Filter content by genre with dropdown
- **Watchlist**: Add/remove content using stored procedures
- **Ratings**: Rate and review movies/shows (triggers auto-update averages)
- **Viewing History**: Automatic tracking on video completion

### Database Features
- **Stored Procedures**: `sp_AddToWatchlist`, `sp_RemoveFromWatchlist`, `sp_GetWatchHistory`, `sp_GetRecommendations`, `sp_ProcessPayment`
- **Functions**: `fn_GetSubscriptionStatus`, `fn_GetTotalWatchTime`
- **Triggers**: `trg_CheckProfileLimit`, `trg_UpdateMovieRating`, `trg_UpdateRatingOnUpdate`
- **Connection Pooling**: 30 connections to prevent exhaustion

---

## 🛠️ Technology Stack

### Frontend
- **React** 19.2.0 - UI library
- **React Router** 7.0.2 - Navigation
- **Axios** 1.6.2 - HTTP client
- **React Icons** 5.4.0 - Icon components
- **HTML5 Video Player** - Native video playback
- **CSS3** - Custom styling

### Backend
- **Flask** 3.0.0 - Web framework
- **Flask-CORS** 5.0.0 - Cross-origin requests
- **MySQL Connector** 9.1.0 - Database driver with connection pooling
- **PyJWT** 2.9.0 - JWT authentication
- **Bcrypt** 4.2.1 - Password hashing

### Database
- **MySQL** 8.0+ - Relational database
- 12 tables with foreign key relationships
- 5 stored procedures
- 2 custom functions
- 3 triggers
- Connection pool size: 30

---

## 🗄️ Database Schema

### Core Tables

#### User Management
- **user**: User accounts (User_Id, Name, Email, Password, DOB, Country)
- **profile**: User profiles (Profile_Id, User_Id, Profile_Name, Language_Preference, Age_Restriction)
- **subscription**: User subscriptions (Subscription_Id, User_Id, Plan_Type, Start_Date, End_Date)
- **payment**: Payment records (Payment_Id, User_Id, Amount, Payment_Date, Payment_Method, Status)

#### Content
- **movie**: Movies (Movie_Id, Title, Description, Release_Date, Duration, Age_Rating, average_rating)
- **tv_show**: TV shows (Show_Id, Title, Description, Release_Year, Status, Age_Rating, average_rating)
- **genre**: Content genres (Genre_Id, Genre_Name, Description)
- **movie_genre**: Movie-genre relationships (many-to-many)
- **tvshow_genre**: TV show-genre relationships (many-to-many)
- **home_page**: Featured content (Content_Id, Content_Type, Release_Date, Language, Age_Rating)

#### User Interactions
- **watchlist**: User watchlists (Watchlist_Id, Profile_Id, Content_Type, Content_Id, Date_Added)
- **rating_review**: Ratings and reviews (Rating_Id, Profile_Id, Content_Type, Content_Id, Rating, Review_Text)
- **viewing_history**: Watch history (History_Id, Profile_Id, Content_Type, Content_Id, Watch_Duration, Watch_Date)

### Key Relationships
- User → Profile (1:N, max 3 enforced by trigger)
- User → Subscription (1:N)
- Profile → Watchlist (1:N)
- Profile → Rating (1:N)
- Profile → Viewing History (1:N)
- Movie/TV Show → Genre (N:M)

---

## 🚀 Setup & Installation

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.11+
- **MySQL** 8.0+

### 1. Clone Repository
```bash
git clone https://github.com/mzw111/Streamix.git
cd Streamix
```

### 2. Database Setup

#### Create Database
```sql
CREATE DATABASE streamingdb;
USE streamingdb;
```

#### Run Schema and Objects
```bash
cd backend
mysql -u root -p streamingdb < database_objects.sql
```

#### Populate Database
```bash
python populate_database_simple.py
```

This will populate:
- 5 users
- 15 genres
- 21 movies
- 20 TV shows
- 7 profiles
- 10 featured home page items

### 3. Backend Setup

Create `.env` file in `backend/` directory:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=streamingdb
JWT_SECRET=your_secret_key_here
```

#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Frontend Setup

#### Install Dependencies
```bash
cd frontend/my-app
npm install
```

---

## ▶️ Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
python app.py
```
Backend runs on: `http://localhost:3001`

### Start Frontend (Terminal 2)
```bash
cd frontend/my-app
npm start
```
Frontend runs on: `http://localhost:3002`

### Access Application
Open browser and navigate to: `http://localhost:3002`

---

## 📡 API Documentation

### Base URL
```
http://localhost:3001/api
```

### Authentication Endpoints

#### POST /user/signup
Register a new user
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "dob": "1990-05-15",
  "country": "USA"
}
```

#### POST /user/login
Login user
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```
Returns: `{ "token": "jwt_token", "user_id": 1 }`

### Profile Endpoints

#### GET /profile/list
Get all profiles for logged-in user
- **Auth**: Required (JWT token)

#### POST /profile/create
Create new profile (max 3 profiles enforced by trigger)
```json
{
  "profile_name": "John Main",
  "language_preference": "English",
  "age_restriction": "PG-13"
}
```

#### DELETE /profile/delete/:id
Delete a profile

### Content Endpoints

#### GET /movies/
Get all movies with genres
- **Query Params**: `genre` (optional)

#### GET /movies/:id
Get movie details with video URL

#### GET /tvshows/
Get all TV shows with genres
- **Query Params**: `genre` (optional)

#### GET /genres/
Get all genres

#### GET /home/
Get featured home page content

### Watchlist Endpoints (Uses Stored Procedures)

#### POST /watchlist/add
Add to watchlist (calls `sp_AddToWatchlist`)
```json
{
  "profile_id": 1,
  "content_type": "Movie",
  "content_id": 26
}
```

#### DELETE /watchlist/remove
Remove from watchlist (calls `sp_RemoveFromWatchlist`)

#### GET /watchlist/all/:profile_id
Get all watchlist items

### Viewing History Endpoints

#### POST /viewing_history/log
Log viewing history (called automatically on video end)
```json
{
  "profile_id": 1,
  "content_type": "Movie",
  "content_id": 26,
  "watch_duration": 120
}
```

#### GET /viewing_history/profile/:id
Get viewing history for profile (calls `sp_GetWatchHistory`)

#### DELETE /viewing_history/delete/:id
Delete history entry

### Rating Endpoints

#### POST /ratings/add
Add rating/review (triggers auto-update average rating)
```json
{
  "profile_id": 1,
  "content_type": "Movie",
  "content_id": 26,
  "rating": 4.5,
  "review_text": "Great movie!"
}
```

#### GET /ratings/profile/:id
Get all ratings by profile

### Subscription Endpoints

#### GET /subscriptions/plans
Get all subscription plans

#### POST /subscriptions/subscribe
Subscribe to a plan (calls `sp_ProcessPayment`)
```json
{
  "plan_type": "Premium",
  "payment_method": "Credit Card"
}
```

#### GET /subscriptions/status
Get user's subscription status (uses `fn_GetSubscriptionStatus`)

---

## 📁 Project Structure

```
Streamix/
├── backend/
│   ├── app.py                          # Main Flask application
│   ├── db.py                           # Database connection pool
│   ├── requirements.txt                # Python dependencies
│   ├── database_objects.sql            # Stored procedures, functions, triggers (includes profile limit trigger)
│   ├── populate_database_simple.py     # Database population script (applies trigger automatically)
│   ├── routes/
│   │   ├── user_auth.py               # Authentication routes
│   │   ├── profile.py                 # Profile management
│   │   ├── movies.py                  # Movie endpoints
│   │   ├── tvshows.py                 # TV show endpoints
│   │   ├── genres.py                  # Genre endpoints
│   │   ├── home_page.py               # Home page content
│   │   ├── watchlist.py               # Watchlist management
│   │   ├── viewing_history.py         # History tracking
│   │   ├── ratings.py                 # Ratings and reviews
│   │   └── subscriptions.py           # Subscription management
│   └── utils/
│       └── auth_middleware.py         # JWT authentication middleware
│
├── frontend/my-app/
│   ├── package.json                   # npm dependencies
│   ├── public/
│   │   ├── index.html                 # HTML template
│   │   └── videos/                    # Video files directory
│   │       ├── 15097-261402819_small.mp4  # The Dark Knight
│   │       └── 26452-358778857_small.mp4  # Inception
│   └── src/
│       ├── App.js                     # Main React component with routing
│       ├── index.js                   # React entry point
│       ├── components/
│       │   ├── Navbar.js              # Navigation bar
│       │   ├── HeroSection.js         # Hero/banner component
│       │   ├── MovieCard.js           # Content card component
│       │   ├── ScrollableRow.js       # Horizontal scroll row
│       │   ├── RatingModal.js         # Rating popup modal
│       │   ├── VideoPlayer.js         # HTML5 video player component
│       │   └── ProtectedRoute.js      # Route protection HOC
│       ├── pages/
│       │   ├── Home.js                # Home page
│       │   ├── Login.js               # Login page
│       │   ├── Signup.js              # Signup page
│       │   ├── Profiles.js            # Profile selection/management
│       │   ├── Movies.js              # Movies browsing
│       │   ├── TVShows.js             # TV shows browsing
│       │   ├── MovieDetail.js         # Movie detail with video player
│       │   ├── Watchlist.js           # Watchlist page
│       │   ├── ViewingHistory.js      # History page
│       │   └── Subscription.js        # Subscription management
│       ├── context/
│       │   └── AuthContext.js         # Authentication context provider
│       └── services/
│           └── api.js                 # Axios API service with interceptors
│
└── README.md                          # This file
```

---

## 🎥 Video Playback Feature

### Available Videos
- **The Dark Knight** - `15097-261402819_small.mp4`
- **Inception** - `26452-358778857_small.mp4`

### How It Works
1. User clicks on a movie card with available video
2. Navigates to MovieDetail page with integrated video player
3. Video plays using HTML5 `<video>` element
4. On video completion, viewing history is automatically logged
5. Watch duration tracked and stored in database

---

## 🔗 Frontend & Backend Integration

### API Communication Flow
```
User Action → React Component → Axios Service → Flask Route → Database → Response
```

### Authentication Flow
1. User logs in via `/api/user/login`
2. Backend validates credentials and generates JWT token
3. Frontend stores token in localStorage
4. All subsequent requests include token in Authorization header
5. Backend middleware validates token before processing

### Database Connection
- Connection pool with 30 connections prevents exhaustion
- All routes use pooled connections for efficiency
- Automatic connection management and cleanup

---

## 🎓 Key Features for Demonstration

### 1. Profile Limit Trigger
Show how database enforces business rules:
```sql
-- Check existing profiles
SELECT User_Id, COUNT(*) as profile_count 
FROM profile 
GROUP BY User_Id;

-- Try to create 4th profile (will fail)
INSERT INTO profile (User_Id, Profile_Name, Language_Preference, Age_Restriction)
VALUES (1, 'Fourth Profile', 'English', 'PG-13');
```

### 2. Watchlist Stored Procedures
Demonstrate stored procedure usage:
```sql
-- Add to watchlist (prevents duplicates)
CALL sp_AddToWatchlist(2, 'Movie', 4);

-- View watchlist
SELECT * FROM watchlist WHERE Profile_Id = 2;
```

### 3. Rating Triggers
Show automatic average calculation:
```sql
-- Add a rating
INSERT INTO rating_review (Profile_Id, Content_Type, Content_Id, Rating, Review_Text)
VALUES (2, 'Movie', 26, 9.0, 'Amazing film!');

-- Check updated average
SELECT Title, average_rating FROM movie WHERE Movie_Id = 26;
```

### 4. Most Watched Movies Query
Analytics query for viewing patterns:
```sql
SELECT 
    m.Title,
    COUNT(*) AS view_count,
    SUM(vh.Watch_Duration) AS total_watch_duration
FROM viewing_history vh
JOIN movie m ON vh.Content_Id = m.Movie_Id
WHERE vh.Content_Type = 'Movie'
GROUP BY vh.Content_Id, m.Title
ORDER BY view_count DESC;
```

---

## 🆘 Troubleshooting

### Backend Issues
- **Won't start**: Check MySQL is running and credentials in `.env` are correct
- **Connection pool exhaustion**: Verify pool_size=30 in `db.py`
- **Import errors**: Run `pip install -r requirements.txt`

### Frontend Issues
- **Won't connect**: Verify backend is running on port 3001
- **CORS errors**: Check Flask-CORS configuration in `app.py`
- **Video won't play**: Ensure video files exist in `public/videos/` directory

### Database Issues
- **Objects missing**: Run `database_objects.sql` to create all objects
- **Empty tables**: Run `populate_database_simple.py` to populate data
- **Trigger not working**: Check trigger exists with `SHOW TRIGGERS;`

---

## 📝 Notes

- Frontend runs on port **3002** (configured in package.json)
- Backend API on port **3001**
- All passwords hashed with bcrypt
- JWT tokens expire after 24 hours
- Database uses PascalCase naming (Movie_Id, Title, etc.)
- Video playback logs history only on completion (not during playback)
- Connection pool set to 30 to handle concurrent requests

---

## 👥 Contributors

**mzw111** - Full Stack Development, Database Design, API Implementation

---

## 📄 License

This project is for educational purposes as part of a Database Management Systems course.

---

**Happy Streaming! 🎬🍿**

Built with ❤️ using React, Flask, and MySQL
