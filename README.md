# 🎬 Streamix - Streaming Platform



A full-stack Netflix-like streaming platform built with React, Flask, and MySQL featuring user authentication, profile management, content browsing, watchlists, viewing history, and subscription management.A full-stack Netflix-like streaming platform built with React, Flask, and MySQL featuring user authentication, profile management, content browsing, watchlists, viewing history, and subscription management.



------



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



------



## 🎯 Project Overview



Streamix is a comprehensive streaming platform that allows users to:Streamix is a comprehensive streaming platform that allows users to:

- Browse and search movies and TV shows by genre- Browse and search movies and TV shows by genre

- Create multiple profiles per account (with a 3-profile limit enforced by database trigger)
  
- Manage personal watchlists- Manage personal watchlists

- Track viewing history automatically- Track viewing history automatically

- Rate and review content- Rate and review content

- Subscribe to different plans- Subscribe to different plans

- View personalized home page with featured content- View personalized home page with featured content



------



## 🏗️ Architecture



### System Architecture



``````

┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐

│                 │         │                 │         │                 ││                 │         │                 │         │                 │

│  React Frontend │ ◄─────► │  Flask Backend  │ ◄─────► │  MySQL Database ││  React Frontend │ ◄─────► │  Flask Backend  │ ◄─────► │  MySQL Database │

│  (Port 3000)    │  HTTP   │  (Port 3001)    │   SQL   │  (Port 3306)    ││  (Port 3000)    │  HTTP   │  (Port 3001)    │   SQL   │  (Port 3306)    │

│                 │  /API   │                 │         │                 ││                 │  /API   │                 │         │                 │

└─────────────────┘         └─────────────────┘         └─────────────────┘└─────────────────┘         └─────────────────┘         └─────────────────┘

``````



### Component Flow### Component Flow



1. **Frontend (React)**: User interface for browsing content, managing profiles, and interacting with features. 

2. **Backend (Flask)**: REST API handling business logic, authentication, and database operations.

3. **Database (MySQL)**: Stores all application data with enforced relationships and constraints


------



## ✨ Features



### User Management

- **Authentication**: Secure login/signup with JWT tokens
  
- **Profiles**: Multiple profiles per user (max 3, enforced by trigger)

- **Subscriptions**: Basic, Standard, and Premium plans



### Content Features

- **Browse**: Movies and TV shows with genre filtering

- **Search**: Filter content by genre with dropdown

- **Watchlist**: Add/remove content to personal watchlist

- **Ratings**: Rate and review movies/shows

- **Viewing History**: Automatic tracking when clicking content



### Database Features

- **Stored Procedures**: `sp_AddToWatchlist`, `sp_GetWatchHistory`, `sp_ProcessPayment`

- **Functions**: `fn_GetSubscriptionStatus`, `fn_GetTotalWatchTime`
  
- **Triggers**: `trg_CheckProfileLimit` (prevents >3 profiles per user)



------



## 🛠️ Technology Stack



### Frontend

- **React** 19.2.0 - UI library

- **React Router** 7.0.2 - Navigation
  
- **Axios** 1.6.2 - HTTP client

- **React Icons** 5.4.0 - Icon components

- **CSS3** - Styling



### Backend

- **Flask** 3.0.0 - Web framework

- **Flask-CORS** 5.0.0 - Cross-origin requests
  
- **MySQL Connector** 9.1.0 - Database driver

- **PyJWT** 2.9.0 - JWT authentication

- **Bcrypt** 4.2.1 - Password hashing



### Database### Database

- **MySQL** 8.0+ - Relational database

- 13 tables with foreign key relationships

- Stored procedures, functions, and triggers

- **MySQL 8.0+**

---- 12 tables with proper relationships

- 5 stored procedures

## 🗄️ Database Schema- 2 custom functions

- 3 triggers

### Core Tables

## 🗄 Database Architecture

#### User Management

- **user**: User accounts (User_Id, Name, Email, Password, DOB, Country)### Tables

- **profile**: User profiles (Profile_Id, User_Id, Profile_Name, Language_Preference, Age_Restriction)1. **user** - User accounts

- **subscription**: User subscriptions (Subscription_Id, User_Id, Plan_Type, Start_Date, End_Date, Status)2. **profile** - User profiles (multiple per user)

- **payment**: Payment records (Payment_Id, User_Id, Amount, Payment_Date, Payment_Method, Status)3. **subscription** - Subscription plans and status

4. **movie** - Movie catalog (20 movies)

#### Content5. **tv_show** - TV show catalog (15 shows)

- **movie**: Movies (Movie_Id, Title, Description, Release_Date, Duration, Age_Rating, average_rating)6. **genre** - Genre categories (17 genres)

- **tv_show**: TV shows (Show_Id, Title, Description, Release_Year, Status, Age_Rating, average_rating)7. **watchlist** - User's watchlist

- **genre**: Content genres (Genre_Id, Genre_Name, Description)8. **rating_review** - Ratings and reviews

- **movie_genre**: Movie-genre relationships9. **viewing_history** - Watch history tracking

- **tvshow_genre**: TV show-genre relationships10. **home_page** - Featured content

- **home_page**: Featured content (Content_Id, Content_Type, Release_Date, Language, Age_Rating)11. **payment** - Payment records

12. **movie_genre** & **tvshow_genre** - Many-to-many relationships

#### User Interactions

- **watchlist**: User watchlists (Watchlist_Id, Profile_Id, Content_Type, Content_Id, Date_Added)### Database Objects

- **rating_review**: Ratings and reviews (Rating_Id, Profile_Id, Content_Type, Content_Id, Rating, Review_Text)

- **viewing_history**: Watch history (History_Id, Profile_Id, Content_Type, Content_Id, Watch_Duration, Watch_Date)#### Stored Procedures

- **sp_AddToWatchlist**: Add content to watchlist with duplicate prevention

### Key Relationships- **sp_RemoveFromWatchlist**: Remove content from watchlist

- User → Profile (1:N, max 3 enforced by trigger)- **sp_GetWatchHistory**: Retrieve complete viewing history

- User → Subscription (1:N)- **sp_GetRecommendations**: Get personalized recommendations

- Profile → Watchlist (1:N)- **sp_ProcessPayment**: Process subscription payments

- Profile → Rating (1:N)

- Profile → Viewing History (1:N)#### Functions

- Movie/TV Show → Genre (N:M)- **fn_GetSubscriptionStatus**: Check user subscription status (Active/Expired/Inactive)

- **fn_GetTotalWatchTime**: Calculate total watch time for a profile

---

#### Triggers

## 🚀 Setup & Installation- **trg_UpdateMovieRating**: Update movie average rating on new review (INSERT)

- **trg_UpdateRatingOnUpdate**: Update rating when review is modified (UPDATE)

### Prerequisites- **trg_UpdateAverageRating**: Recalculate average rating on review changes

- **Node.js** 18+ and npm

- **Python** 3.11+## 📁 Project Structure

- **MySQL** 8.0+

```

### 1. Clone Repositorystreamix/

```bash├── backend/

git clone https://github.com/mzw111/Streamix.git│   ├── app.py                    # Flask application entry point

cd Streamix│   ├── db.py                     # Database connection pool

```│   ├── requirements.txt          # Python dependencies

│   ├── routes/

### 2. Database Setup│   │   ├── movies.py            # Movie endpoints

│   │   ├── tvshows.py           # TV show endpoints

#### Create Database│   │   ├── user_auth.py         # Authentication

```sql│   │   ├── profile.py           # Profile management

CREATE DATABASE streamingdb;│   │   ├── watchlist.py         # Watchlist operations (uses procedures)

USE streamingdb;│   │   ├── subscriptions.py     # Subscription management (uses functions)

```│   │   └── users.py             # User management

│   └── utils/

#### Run Schema and Objects│       └── auth_middleware.py   # JWT middleware

```bash├── frontend/

cd backend│   └── my-app/

mysql -u root -p streamingdb < database_objects.sql│       ├── package.json

```│       ├── public/

│       └── src/

#### Populate Database│           ├── pages/           # 7 main pages

```bash│           │   ├── Home.js

python populate_database_simple.py│           │   ├── Login.js

```│           │   ├── Signup.js

│           │   ├── Profiles.js

This will populate:│           │   ├── Movies.js

- 5 users│           │   ├── TVShows.js

- 15 genres│           │   └── Watchlist.js

- 21 movies│           ├── components/      # 5 reusable components

- 20 TV shows│           │   ├── Navbar.js

- 7 profiles│           │   ├── MovieCard.js

- 10 featured home page items│           │   ├── SearchBar.js

│           │   ├── GenreFilter.js

#### Apply Profile Limit Trigger│           │   └── ProfileCard.js

```bash│           └── services/

python apply_trigger.py│               └── api.js       # Axios API client

```├── database_objects.sql         # All procedures, functions, triggers

├── DATABASE_FEATURES.md         # Detailed database documentation

### 3. Backend Setup└── TESTING_RESULTS.md          # Comprehensive test results



#### Create `.env` file in `backend/` directory:```

```env

DB_HOST=localhost## 🚀 Setup Instructions

DB_USER=root

DB_PASSWORD=your_password### Prerequisites

DB_NAME=streamingdb- **Node.js** 14+ and npm

JWT_SECRET=your_secret_key_here- **Python** 3.8+

```- **MySQL** 8.0+

- **Git**

#### Install Dependencies

```bash### 1. Clone Repository

cd backend```bash

pip install -r requirements.txtgit clone <your-repo-url>

```cd streamix

```

### 4. Frontend Setup

### 2. Database Setup

#### Install Dependencies```bash

```bash# Login to MySQL

cd frontend/my-appmysql -u root -p

npm install

```# Create database

CREATE DATABASE streamingdb;

---USE streamingdb;



## ▶️ Running the Application# Import schema (run your schema file)

source path/to/your/schema.sql;

### Start Backend (Terminal 1)

```bash# Create database objects

cd backendsource database_objects.sql;

python app.py```

```

Backend runs on: `http://localhost:3001`### 3. Backend Setup

```bash

### Start Frontend (Terminal 2)cd backend

```bash

cd frontend/my-app# Create virtual environment (optional)

npm startpython -m venv venv

```venv\Scripts\activate  # Windows

Frontend runs on: `http://localhost:3000`# source venv/bin/activate  # Linux/Mac



### Access Application# Install dependencies

Open browser and navigate to: `http://localhost:3000`pip install -r requirements.txt



---# Update db.py with your MySQL credentials

# Edit db.py and set:

## 📡 API Documentation# host="localhost"

# user="root"

### Base URL# password="your_password"

```# database="streamingdb"

http://localhost:3001/api

```# Run Flask server

python app.py

### Authentication Endpoints# Server runs on http://127.0.0.1:3001

```

#### POST /user/signup

Register a new user### 4. Frontend Setup

```json```bash

{cd frontend/my-app

  "name": "John Doe",

  "email": "john@example.com",# Install dependencies

  "password": "password123",npm install

  "dob": "1990-05-15",

  "country": "USA"# Run development server

}npm start

```# Server runs on http://localhost:3000

```

#### POST /user/login

Login user### 5. Access Application

```json- Frontend: http://localhost:3000

{- Backend API: http://127.0.0.1:3001/api

  "email": "john@example.com",- Default test credentials:

  "password": "password123"  - Email: `user1@example.com`

}  - Password: (check your database)

```

Returns: `{ "token": "jwt_token", "user_id": 1 }`## 📡 API Documentation



### Profile Endpoints### Authentication

```

#### GET /profile/listPOST /api/user/register    # Register new user

Get all profiles for logged-in userPOST /api/user/login       # Login user (returns JWT)

- **Auth**: Required (JWT token)GET  /api/user/info        # Get user info (requires JWT)

```

#### POST /profile/create

Create new profile (max 3)### Content

```json```

{GET  /api/movies/          # Get all movies

  "profile_name": "John Main",GET  /api/movies/<id>      # Get movie by ID

  "language_preference": "English",GET  /api/tvshows/         # Get all TV shows

  "age_restriction": "PG-13"GET  /api/tvshows/<id>     # Get TV show by ID

}GET  /api/home/            # Get featured content

``````



#### DELETE /profile/delete/:id### Profile

Delete a profile```

GET  /api/profile/list     # Get user's profiles

### Content EndpointsPOST /api/profile/create   # Create new profile

GET  /api/profile/<id>     # Get profile details

#### GET /movies/```

Get all movies with genres

- **Query Params**: `genre` (optional)### Watchlist (Uses Stored Procedures)

```

#### GET /tvshows/GET    /api/watchlist/all/<profile_id>           # Get watchlist

Get all TV shows with genresPOST   /api/watchlist/add                        # Add to watchlist (calls sp_AddToWatchlist)

- **Query Params**: `genre` (optional)DELETE /api/watchlist/remove/<watchlist_id>      # Remove from watchlist (calls sp_RemoveFromWatchlist)

```

#### GET /genres/

Get all genres### Subscriptions (Uses Functions)

```

#### GET /home/GET  /api/subscriptions/status     # Get subscription status (uses fn_GetSubscriptionStatus)

Get featured home page contentGET  /api/subscriptions/plans      # Get available plans

POST /api/subscriptions/subscribe  # Subscribe to plan

### Watchlist Endpoints```



#### POST /watchlist/add### Search & Filter

Add to watchlist```

```jsonGET  /api/search?query=<text>           # Search movies/TV shows

{GET  /api/movies/genre/<genre_name>     # Filter movies by genre

  "profile_id": 1,GET  /api/tvshows/genre/<genre_name>    # Filter TV shows by genre

  "content_type": "Movie",```

  "content_id": 26

}## 🧪 Testing

```

### Database Objects Testing

#### DELETE /watchlist/remove

Remove from watchlistAll database objects have been thoroughly tested. See `TESTING_RESULTS.md` for detailed results.



#### GET /watchlist/all/:profile_id#### Quick Test Commands

Get all watchlist items

**Test Stored Procedure**:

### Viewing History Endpoints```sql

-- Add to watchlist

#### POST /viewing_history/logCALL sp_AddToWatchlist(2, 'Movie', 4);

Log viewing historySELECT * FROM watchlist WHERE Profile_Id = 2;

```json```

{

  "profile_id": 1,**Test Function**:

  "content_type": "Movie",```sql

  "content_id": 26,-- Check subscription status

  "watch_duration": 120SELECT fn_GetSubscriptionStatus(1);

}```

```

**Test Trigger**:

#### GET /viewing_history/profile/:id```sql

Get viewing history for profile-- Insert rating (trigger auto-updates average)

INSERT INTO rating_review (User_Id, Movie_Id, Rating, Review_Text) 

#### DELETE /viewing_history/delete/:idVALUES (1, 26, 9.5, 'Great movie!');

Delete history entry

SELECT average_rating FROM movie WHERE Movie_Id = 26;

### Rating Endpoints```



#### POST /ratings/add#### Run Test Scripts

Add rating/review```bash

```jsoncd backend

{

  "profile_id": 1,# Test all database features

  "content_type": "Movie",python test_all_database_features.py

  "content_id": 26,

  "rating": 4.5,# Test specific trigger

  "review_text": "Great movie!"python test_rating_trigger.py

}

```# Verify all objects exist

python verify_database_objects.py

#### GET /ratings/profile/:id```

Get all ratings by profile

### Frontend Testing

### Subscription Endpoints1. Navigate to http://localhost:3000

2. Register a new account or login

#### GET /subscriptions/plans3. Create a profile

Get all subscription plans4. Browse movies/TV shows

5. Add items to watchlist

#### POST /subscriptions/subscribe6. Rate content and verify average rating updates

Subscribe to a plan

```json## 🔧 Database Objects

{

  "plan_type": "Premium",For complete documentation of all stored procedures, functions, and triggers, see:

  "payment_method": "Credit Card"- **DATABASE_FEATURES.md** - Detailed feature documentation

}- **TESTING_RESULTS.md** - Test results and SQL examples

```- **database_objects.sql** - Complete SQL source code



#### GET /subscriptions/status### Key Database Objects

Get user's subscription status

**Watchlist Management**:

---- `sp_AddToWatchlist` - Prevents duplicates, auto-timestamps

- `sp_RemoveFromWatchlist` - Safe removal with validation

## 🗂️ Database Objects

**Recommendations**:

### Stored Procedures- `sp_GetRecommendations` - Genre-based recommendations from watch history



#### sp_AddToWatchlist**Subscription**:

Adds content to user's watchlist (prevents duplicates)- `fn_GetSubscriptionStatus` - Returns Active/Expired/Inactive

```sql- `sp_ProcessPayment` - Complete payment processing workflow

CALL sp_AddToWatchlist(profile_id, content_type, content_id);

```**Rating System**:

- `trg_UpdateMovieRating` - Auto-calculates average on INSERT

#### sp_GetWatchHistory- `trg_UpdateRatingOnUpdate` - Recalculates on UPDATE

Retrieves viewing history for a profile- Uses DECIMAL(3,1) for 0.0-10.0 rating scale

```sql

CALL sp_GetWatchHistory(profile_id);## 📝 Notes

```

- All API endpoints require JWT token except `/register` and `/login`

#### sp_ProcessPayment- Database uses PascalCase column names (Movie_Id, Title, etc.)

Processes subscription payment and updates subscription- Backend transforms responses to snake_case for frontend

```sql- Poster URLs use TMDB image CDN

CALL sp_ProcessPayment(user_id, plan_id, amount, payment_method);- Dark purple theme: `#1a0033` background, `#9b59b6` accents

```

## 👥 Contributors

### Functions

- Database Design & Schema

#### fn_GetSubscriptionStatus- Backend API Development

Returns user's subscription status (Active/Inactive)- Frontend React Implementation

```sql- Database Objects & Triggers

SELECT fn_GetSubscriptionStatus(user_id);

```## 📄 License



#### fn_GetTotalWatchTimeThis project is for educational purposes.

Calculates total watch time for a profile

```sql---

SELECT fn_GetTotalWatchTime(profile_id);

```**Built with ❤️ using React, Flask, and MySQL**

### Triggers

#### trg_CheckProfileLimit
**Purpose**: Prevents users from creating more than 3 profiles

**Demonstration**: Perfect for showing teachers how triggers enforce business rules!

**How to demonstrate**:
1. Create 3 profiles for a user
2. Try to create a 4th profile
3. **Result**: Error message "Maximum profile limit (3) reached for this user."

```sql
-- Trigger automatically fires BEFORE INSERT on profile table
-- No manual execution needed!
```

---

## 📁 Project Structure

```
Streamix/
├── backend/
│   ├── app.py                          # Main Flask application
│   ├── db.py                           # Database connection pool
│   ├── requirements.txt                # Python dependencies
│   ├── database_objects.sql            # Stored procedures, functions, triggers
│   ├── populate_database_simple.py     # Database population script
│   ├── apply_trigger.py                # Apply profile limit trigger
│   ├── create_profile_limit_trigger.sql # Profile limit trigger SQL
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
│   │   └── index.html                 # HTML template
│   └── src/
│       ├── App.js                     # Main React component
│       ├── index.js                   # React entry point
│       ├── components/
│       │   ├── Navbar.js              # Navigation bar
│       │   ├── HeroSection.js         # Hero/banner component
│       │   ├── MovieCard.js           # Content card component
│       │   ├── ScrollableRow.js       # Horizontal scroll row
│       │   ├── RatingModal.js         # Rating popup
│       │   └── ProtectedRoute.js      # Route protection
│       ├── pages/
│       │   ├── Home.js                # Home page
│       │   ├── Login.js               # Login page
│       │   ├── Signup.js              # Signup page
│       │   ├── Profiles.js            # Profile selection/management
│       │   ├── Movies.js              # Movies browsing
│       │   ├── TVShows.js             # TV shows browsing
│       │   ├── Watchlist.js           # Watchlist page
│       │   ├── ViewingHistory.js      # History page
│       │   └── Subscription.js        # Subscription management
│       ├── context/
│       │   └── AuthContext.js         # Authentication context
│       └── services/
│           └── api.js                 # Axios API service
│
└── README.md                          # This file
```

---

## 🔗 How Frontend & Backend Connect

### 1. API Communication Flow

```
User Action → React Component → Axios API Call → Flask Route → Database Query → Response
```

**Example**: Adding to Watchlist
```javascript
// Frontend (MovieCard.js)
const handleWatchlist = async () => {
  const response = await watchlistAPI.add({
    profile_id: 15,
    content_type: 'Movie',
    content_id: 26
  });
};
```

```python
# Backend (watchlist.py)
@watchlist_bp.route('/add', methods=['POST'])
@token_required
def add_to_watchlist(current_user):
    data = request.get_json()
    execute_query(query, (profile_id, content_type, content_id))
    return jsonify({"success": True})
```

### 2. Authentication Flow

```
1. User logs in → POST /api/user/login
2. Backend validates credentials
3. Backend generates JWT token
4. Frontend stores token in localStorage
5. All subsequent requests include token in Authorization header
6. Backend middleware validates token before processing request
```

### 3. Database Connection

```python
# db.py - Connection Pool
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="streamix_pool",
    pool_size=5,
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
```

All backend routes use this pool for database operations.

---

## 🎓 For Teacher Demonstration

### Trigger Demonstration

**Show Profile Limit Trigger (`trg_CheckProfileLimit`)**:

1. Open MySQL Workbench
2. Show trigger code:
   ```sql
   SHOW CREATE TRIGGER trg_CheckProfileLimit;
   ```

3. Check current profiles:
   ```sql
   SELECT User_Id, COUNT(*) as profile_count 
   FROM profile 
   GROUP BY User_Id;
   ```

4. Try to insert 4th profile for a user with 3 profiles:
   ```sql
   INSERT INTO profile (User_Id, Profile_Name, Language_Preference, Age_Restriction)
   VALUES (1, 'Fourth Profile', 'English', 'PG-13');
   ```

5. **Result**: Error message appears!
   ```
   Error: Maximum profile limit (3) reached for this user.
   ```

This demonstrates how triggers automatically enforce business rules without application code!

---

## 📝 License

This project was created for educational purposes as part of a Database Management Systems course.

---

## 👥 Contributors

- **mihirstag** - Project Developer
- **mzw111** - Project Developer

---

## 🆘 Troubleshooting

### Backend won't start
- Check if MySQL is running
- Verify `.env` file has correct credentials
- Ensure all Python packages are installed

### Frontend won't connect
- Verify backend is running on port 3001
- Check CORS settings in Flask app
- Clear browser cache and localStorage

### Database errors
- Ensure database `streamingdb` exists
- Run `database_objects.sql` to create schema
- Run `populate_database_simple.py` to populate data

### Trigger not working
- Run `python apply_trigger.py` to create trigger
- Check if trigger exists: `SHOW TRIGGERS;`
- Verify MySQL user has TRIGGER privilege

---
