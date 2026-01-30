# Streamix

A full-stack streaming platform built with React, Flask, and MySQL.

## Tech Stack

- **Frontend:** React, React Router, Axios
- **Backend:** Flask, Flask-CORS, PyJWT, Bcrypt
- **Database:** MySQL 8.0+

## Prerequisites

- Node.js 18+
- Python 3.11+
- MySQL 8.0+

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/mzw111/Streamix.git
cd Streamix
```

### 2. Database Setup

```sql
CREATE DATABASE streamingdb;
USE streamingdb;
```

```bash
cd backend
mysql -u root -p streamingdb < database_objects.sql
python populate_database_simple.py
```

### 3. Backend Setup

Create `backend/.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=streamingdb
JWT_SECRET=your_secret_key_here
```

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend/my-app
npm install
```

## Running the Application

Start backend:

```bash
cd backend
python app.py
```

Start frontend:

```bash
cd frontend/my-app
npm start
```

- Backend: http://localhost:3001
- Frontend: http://localhost:3002

## Features

- User authentication with JWT
- Multiple profiles per account (max 3)
- Browse movies and TV shows by genre
- Video playback with history tracking
- Watchlist management
- Ratings and reviews
- Subscription plans (Basic, Standard, Premium)

## Database Objects

- **Stored Procedures:** sp_AddToWatchlist, sp_RemoveFromWatchlist, sp_GetWatchHistory, sp_GetRecommendations, sp_ProcessPayment
- **Functions:** fn_GetSubscriptionStatus, fn_GetTotalWatchTime
- **Triggers:** trg_CheckProfileLimit, trg_UpdateMovieRating, trg_UpdateRatingOnUpdate

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/user/signup | Register user |
| POST | /api/user/login | Login user |
| GET | /api/profile/list | Get user profiles |
| POST | /api/profile/create | Create profile |
| GET | /api/movies/ | Get all movies |
| GET | /api/tvshows/ | Get all TV shows |
| GET | /api/genres/ | Get all genres |
| POST | /api/watchlist/add | Add to watchlist |
| GET | /api/watchlist/all/:profile_id | Get watchlist |
| POST | /api/ratings/add | Add rating |
| POST | /api/viewing_history/log | Log viewing history |
| GET | /api/subscriptions/plans | Get subscription plans |
| POST | /api/subscriptions/subscribe | Subscribe to plan |

## License

Educational project for Database Management Systems course.
