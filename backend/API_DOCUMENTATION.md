# Streamix Backend API Documentation

## Base URL
```
http://localhost:3001/api
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 1. User Authentication (`/api/user`)

### POST `/api/user/signup`
Register a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "dob": "1990-01-01",
  "country": "USA"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully!"
}
```

### POST `/api/user/login`
Login and receive JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful!",
  "token": "eyJhbGc...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### POST `/api/user/logout`
Logout user (client-side token removal).

**Response:**
```json
{
  "success": true,
  "message": "User logged out successfully!"
}
```

---

## 2. User Management (`/api/users`)

### GET `/api/users/profile` 🔒
Get current user's profile information.

**Response:**
```json
{
  "success": true,
  "user": {
    "User_Id": 1,
    "Name": "John Doe",
    "DOB": "1990-01-01",
    "Country": "USA",
    "Email": "john@example.com"
  }
}
```

### PUT `/api/users/update` 🔒
Update user profile.

**Request Body:**
```json
{
  "name": "John Updated",
  "dob": "1990-01-01",
  "country": "Canada"
}
```

### PUT `/api/users/change-password` 🔒
Change user password.

**Request Body:**
```json
{
  "old_password": "oldpassword",
  "new_password": "newpassword"
}
```

---

## 3. Profiles (`/api/profile`)

### POST `/api/profile/create` 🔒
Create a new profile for the current user.

**Request Body:**
```json
{
  "name": "John's Profile",
  "picture": "avatar1.png",
  "language": "English",
  "age_restriction": "18+"
}
```

### GET `/api/profile/list` 🔒
Get all profiles for the current user.

**Response:**
```json
{
  "success": true,
  "profiles": [
    {
      "Profile_Id": 1,
      "User_Id": 1,
      "Profile_Name": "John's Profile",
      "Profile_Picture": "avatar1.png",
      "Language_Preference": "English",
      "Age_Restriction": "18+"
    }
  ]
}
```

### DELETE `/api/profile/delete/<profile_id>` 🔒
Delete a specific profile.

---

## 4. Movies (`/api/movies`)

### GET `/api/movies/`
Get all movies.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "Movie_Id": 1,
      "Title": "Inception",
      "Description": "A mind-bending thriller",
      "Release_Date": "2010-07-16",
      "Duration": 148,
      "Age_Rating": "PG-13",
      "average_rating": 8.8
    }
  ]
}
```

### GET `/api/movies/<movie_id>`
Get a specific movie by ID.

### GET `/api/movies/genre/<genre_name>`
Get movies by genre (e.g., "Action", "Drama").

---

## 5. TV Shows (`/api/tvshows`)

### GET `/api/tvshows/`
Get all TV shows.

### GET `/api/tvshows/<show_id>`
Get a specific TV show by ID.

### GET `/api/tvshows/genre/<genre_name>`
Get TV shows by genre.

---

## 6. Genres (`/api/genres`)

### GET `/api/genres/`
Get all genres.

**Response:**
```json
{
  "success": true,
  "genres": [
    {
      "Genre_Id": 1,
      "Genre_Name": "Action",
      "Description": "Action-packed movies"
    }
  ]
}
```

### GET `/api/genres/<genre_id>`
Get a specific genre by ID.

---

## 7. Home Page (`/api/home`)

### GET `/api/home/`
Get featured content for the home page.

**Response:**
```json
{
  "success": true,
  "content": [
    {
      "Content_Id": 1,
      "Content_Type": "Movie",
      "Title": "Inception",
      "Description": "...",
      "Release_Date": "2010-07-16",
      "Language": "English",
      "Age_Rating": "PG-13",
      "average_rating": 8.8
    }
  ]
}
```

---

## 8. Watchlist (`/api/watchlist`)

### POST `/api/watchlist/add` 🔒
Add content to watchlist using stored procedure `sp_AddToWatchlist`.

**Request Body:**
```json
{
  "profile_id": 1,
  "content_type": "Movie",
  "content_id": 5
}
```

### DELETE `/api/watchlist/remove` 🔒
Remove content from watchlist.

**Request Body:**
```json
{
  "profile_id": 1,
  "content_type": "Movie",
  "content_id": 5
}
```

### GET `/api/watchlist/all/<profile_id>` 🔒
Get all watchlist items for a profile.

**Response:**
```json
{
  "success": true,
  "watchlist": [
    {
      "Watchlist_Id": 1,
      "Content_Type": "Movie",
      "Content_Id": 5,
      "Title": "Inception",
      "Date_Added": "2024-11-04T10:30:00"
    }
  ]
}
```

---

## 9. Ratings & Reviews (`/api/ratings`)

### POST `/api/ratings/add` 🔒
Add a rating/review (triggers automatic average rating update via `trg_UpdateAverageRating`).

**Request Body:**
```json
{
  "profile_id": 1,
  "content_type": "Movie",
  "content_id": 5,
  "rating": 9,
  "review_text": "Amazing movie!"
}
```

### GET `/api/ratings/content/<content_type>/<content_id>`
Get all ratings for specific content.

**Example:** `/api/ratings/content/Movie/5`

### GET `/api/ratings/profile/<profile_id>` 🔒
Get all ratings by a specific profile.

---

## 10. Viewing History (`/api/viewing_history`)

### POST `/api/viewing_history/log` 🔒
Log a viewing session.

**Request Body:**
```json
{
  "profile_id": 1,
  "content_type": "Movie",
  "content_id": 5,
  "watch_duration": 148
}
```

### GET `/api/viewing_history/profile/<profile_id>` 🔒
Get viewing history for a profile.

### DELETE `/api/viewing_history/delete/<history_id>` 🔒
Delete a viewing history entry.

---

## 11. Subscriptions (`/api/subscriptions`)

### POST `/api/subscriptions/create` 🔒
Create a new subscription.

**Request Body:**
```json
{
  "start_date": "2024-11-01",
  "end_date": "2024-12-01",
  "auto_renewal": true,
  "payment_status": "Pending"
}
```

### GET `/api/subscriptions/list` 🔒
Get all subscriptions for the current user.

### GET `/api/subscriptions/status` 🔒
Get subscription status using SQL function `fn_GetSubscriptionStatus`.

**Response:**
```json
{
  "success": true,
  "status": "Active"
}
```

**Possible statuses:** `Active`, `Expired`, `None`

---

## 12. Payments (`/api/payments`)

### POST `/api/payments/create` 🔒
Create a payment record.

**Request Body:**
```json
{
  "subscription_id": 1,
  "amount": 9.99,
  "payment_method": "Credit Card",
  "payment_status": "Completed"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Payment recorded",
  "transaction_id": "TXN-A1B2C3D4E5F6"
}
```

### GET `/api/payments/subscription/<subscription_id>` 🔒
Get all payments for a specific subscription.

### GET `/api/payments/history` 🔒
Get complete payment history for the current user.

---

## Database Features Implemented

### 1. Stored Procedure: `sp_AddToWatchlist`
- **Used in:** POST `/api/watchlist/add`
- **Purpose:** Safely adds items to watchlist with auto-generated ID and timestamp

### 2. Trigger: `trg_UpdateAverageRating`
- **Fires on:** INSERT to `rating_review` table
- **Purpose:** Automatically updates `average_rating` in `movie` or `tv_show` tables

### 3. Function: `fn_GetSubscriptionStatus`
- **Used in:** GET `/api/subscriptions/status`
- **Returns:** `Active`, `Expired`, or `None` based on subscription end date

---

## Error Responses

All endpoints may return error responses in this format:

```json
{
  "success": false,
  "message": "Error description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing fields)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (not authorized for resource)
- `404` - Not Found

---

## Notes

- 🔒 indicates protected endpoints requiring JWT authentication
- All dates should be in `YYYY-MM-DD` format
- All datetime fields are returned in ISO format
- Content_Type must be either `'Movie'` or `'TV_Show'`
- JWT tokens expire after 6 hours

---

## Environment Variables

Create a `.env` file with:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=streamingdb
JWT_SECRET=your_secret_key
```
