# Streamix Backend

Flask-based REST API for Streamix streaming platform with MySQL database integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

### Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure Database**:
Edit `db.py` with your MySQL credentials:
```python
host="localhost"
user="root"
password="your_password"
database="streamingdb"
```

3. **Run Server**:
```bash
python app.py
```
Server will start on `http://127.0.0.1:3001`

## 📁 Structure

```
backend/
├── app.py                    # Main Flask application
├── db.py                     # Database connection pool
├── requirements.txt          # Dependencies
├── routes/                   # API route modules
│   ├── user_auth.py         # Authentication endpoints
│   ├── users.py             # User management
│   ├── profile.py           # Profile operations
│   ├── movies.py            # Movie endpoints
│   ├── tvshows.py           # TV show endpoints
│   ├── watchlist.py         # Watchlist (uses stored procedures)
│   └── subscriptions.py     # Subscriptions (uses functions)
└── utils/
    └── auth_middleware.py   # JWT authentication
```

## 🔌 API Endpoints

See **API_DOCUMENTATION.md** for complete endpoint documentation.

### Quick Reference

**Authentication**:
- `POST /api/user/signup` - Register
- `POST /api/user/login` - Login (returns JWT)

**Content**:
- `GET /api/movies/` - All movies
- `GET /api/tvshows/` - All TV shows
- `GET /api/home/` - Featured content

**Watchlist** (uses stored procedures):
- `GET /api/watchlist/all/<profile_id>`
- `POST /api/watchlist/add` - Calls `sp_AddToWatchlist`
- `DELETE /api/watchlist/remove/<id>` - Calls `sp_RemoveFromWatchlist`

**Subscriptions** (uses database functions):
- `GET /api/subscriptions/status` - Uses `fn_GetSubscriptionStatus`

## 🔐 Authentication

Most endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

Get token from `/api/user/login` endpoint.

## 🗄 Database Integration

### Stored Procedures Used
- `sp_AddToWatchlist` - Add to watchlist with duplicate check
- `sp_RemoveFromWatchlist` - Remove from watchlist
- `sp_GetWatchHistory` - Get viewing history
- `sp_GetRecommendations` - Get recommendations
- `sp_ProcessPayment` - Process payments

### Functions Used
- `fn_GetSubscriptionStatus` - Check subscription status
- `fn_GetTotalWatchTime` - Calculate watch time

### Triggers Active
- `trg_UpdateMovieRating` - Auto-update average ratings on INSERT
- `trg_UpdateRatingOnUpdate` - Auto-update on rating UPDATE

## 📦 Dependencies

```
Flask==3.0.0
flask-cors==4.0.0
mysql-connector-python==8.2.0
PyJWT==2.8.0
python-dotenv==1.0.0
```

## 🔧 Configuration

### Database Connection
The app uses a connection pool configured in `db.py`:
- Pool size: 5-10 connections
- Auto-reconnect enabled
- Connection timeout: 5 seconds

### CORS
CORS is enabled for `http://localhost:3000` (frontend development server).

## 📝 Development Notes

- Database columns use PascalCase (e.g., `Movie_Id`, `Title`)
- API responses transformed to snake_case for frontend
- Poster URLs mapped to TMDB CDN in `movies.py` and `tvshows.py`
- JWT tokens expire after 24 hours

## 🧪 Testing

Run test scripts from backend directory:
```bash
python test_all_database_features.py
python test_rating_trigger.py
python verify_database_objects.py
```

See **../TESTING_RESULTS.md** for complete test documentation.

---

For complete API documentation, see **API_DOCUMENTATION.md**

A complete RESTful API backend for a streaming platform built with Flask and MySQL.

## Features

✅ User authentication with JWT tokens and bcrypt password hashing  
✅ Profile management (multiple profiles per user)  
✅ Movie & TV Show catalog with genre filtering  
✅ Watchlist functionality using stored procedures  
✅ Ratings & Reviews with automatic average calculation via triggers  
✅ Viewing history tracking  
✅ Subscription management with status checking via SQL functions  
✅ Payment processing and history  
✅ Home page content aggregation  

## Database Integration

### Stored Procedures
- **sp_AddToWatchlist**: Safely adds items to watchlist

### Triggers
- **trg_UpdateAverageRating**: Auto-updates average ratings when new reviews are added

### Functions
- **fn_GetSubscriptionStatus**: Returns subscription status (Active/Expired/None)

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## Installation

### 1. Clone the repository
```bash
cd backend
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the backend directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=streamingdb
JWT_SECRET=your_super_secret_key_here
```

### 4. Set up the database

Make sure your MySQL database `streamingdb` is created with all tables, and the stored procedure, trigger, and function are implemented:

```sql
-- Run your DDL scripts to create all 13 tables
-- Then create the stored procedure, trigger, and function
```

### 5. Run the application
```bash
python app.py
```

The server will start on `http://localhost:3001`

## Project Structure

```
backend/
├── app.py                    # Main Flask application
├── db.py                     # Database connection pool & utilities
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── API_DOCUMENTATION.md      # Complete API documentation
├── routes/
│   ├── user_auth.py         # Authentication (signup/login/logout)
│   ├── users.py             # User profile management
│   ├── profile.py           # User profiles (multiple per user)
│   ├── movies.py            # Movie endpoints
│   ├── tvshows.py           # TV show endpoints
│   ├── genres.py            # Genre listing
│   ├── home_page.py         # Home page content
│   ├── watchlist.py         # Watchlist CRUD (uses stored procedure)
│   ├── ratings.py           # Ratings & reviews (triggers avg update)
│   ├── viewing_history.py   # Viewing history tracking
│   ├── subscriptions.py     # Subscription management (uses function)
│   └── payments.py          # Payment processing
└── utils/
    └── auth_middleware.py   # JWT authentication middleware
```

## API Endpoints

### Authentication
- `POST /api/user/signup` - Register new user
- `POST /api/user/login` - Login and get JWT token
- `POST /api/user/logout` - Logout

### Users
- `GET /api/users/profile` 🔒 - Get user profile
- `PUT /api/users/update` 🔒 - Update user info
- `PUT /api/users/change-password` 🔒 - Change password

### Profiles
- `POST /api/profile/create` 🔒 - Create profile
- `GET /api/profile/list` 🔒 - List user profiles
- `DELETE /api/profile/delete/<id>` 🔒 - Delete profile

### Content
- `GET /api/movies/` - List all movies
- `GET /api/movies/<id>` - Get movie by ID
- `GET /api/movies/genre/<name>` - Movies by genre
- `GET /api/tvshows/` - List all TV shows
- `GET /api/tvshows/<id>` - Get TV show by ID
- `GET /api/tvshows/genre/<name>` - TV shows by genre
- `GET /api/genres/` - List all genres
- `GET /api/home/` - Get home page content

### Watchlist
- `POST /api/watchlist/add` 🔒 - Add to watchlist (uses SP)
- `DELETE /api/watchlist/remove` 🔒 - Remove from watchlist
- `GET /api/watchlist/all/<profile_id>` 🔒 - Get watchlist

### Ratings & Reviews
- `POST /api/ratings/add` 🔒 - Submit rating (triggers avg update)
- `GET /api/ratings/content/<type>/<id>` - Get content ratings
- `GET /api/ratings/profile/<id>` 🔒 - Get profile ratings

### Viewing History
- `POST /api/viewing_history/log` 🔒 - Log viewing
- `GET /api/viewing_history/profile/<id>` 🔒 - Get history
- `DELETE /api/viewing_history/delete/<id>` 🔒 - Delete entry

### Subscriptions
- `POST /api/subscriptions/create` 🔒 - Create subscription
- `GET /api/subscriptions/list` 🔒 - List subscriptions
- `GET /api/subscriptions/status` 🔒 - Get status (uses function)

### Payments
- `POST /api/payments/create` 🔒 - Create payment
- `GET /api/payments/subscription/<id>` 🔒 - Get subscription payments
- `GET /api/payments/history` 🔒 - Get payment history

🔒 = Requires JWT authentication

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for detailed request/response examples.

## Database Schema

The backend integrates with 13 MySQL tables:
- `user` - User accounts
- `profile` - User profiles
- `movie` - Movie catalog
- `tv_show` - TV show catalog
- `genre` - Content genres
- `movie_genre` - Movie-genre relationships
- `tvshow_genre` - TV show-genre relationships
- `watchlist` - User watchlists
- `rating_review` - Ratings and reviews
- `viewing_history` - Watch history
- `subscription` - User subscriptions
- `payment` - Payment records
- `home_page` - Featured content

## Testing

Test the API using tools like:
- **Postman** - Import endpoints and test
- **curl** - Command line testing
- **Thunder Client** - VS Code extension

Example login request:
```bash
curl -X POST http://localhost:3001/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

## Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ Token expiration (6 hours)
- ✅ Protected routes with middleware
- ✅ Profile ownership verification
- ✅ SQL injection prevention (parameterized queries)

## CORS Configuration

CORS is enabled for all origins (development mode). For production, configure specific origins in `app.py`:

```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

## Dependencies

- **Flask 3.0.0** - Web framework
- **flask-cors 4.0.0** - CORS support
- **mysql-connector-python 8.2.0** - MySQL driver
- **python-dotenv 1.0.0** - Environment variables
- **bcrypt 4.1.1** - Password hashing
- **PyJWT 2.8.0** - JWT tokens

## Production Deployment

For production:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:3001 app:app
   ```

2. **Set strong JWT secret** in production `.env`

3. **Configure CORS** for your frontend domain

4. **Use environment-specific database credentials**

5. **Enable HTTPS** with reverse proxy (nginx/apache)

## Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check `.env` credentials
- Ensure database `streamingdb` exists

### Import Errors
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

### JWT Errors
- Ensure JWT_SECRET is set in `.env`
- Token format: `Bearer <token>`

## License

MIT

## Contact

For issues or questions, please open an issue on GitHub.
