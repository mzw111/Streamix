# Streamix Frontend

React-based frontend for Streamix streaming platform with dark purple theme.

## 🚀 Quick Start

### Prerequisites
- Node.js 14+
- npm or yarn

### Installation

1. **Install dependencies**:
```bash
npm install
```

2. **Configure API URL**:
The app connects to backend at `http://127.0.0.1:3001/api`
Update in `src/services/api.js` if different.

3. **Run Development Server**:
```bash
npm start
```
Opens on `http://localhost:3000`

## 📁 Structure

```
src/
├── pages/                    # Main page components
│   ├── Home.js              # Homepage with featured content
│   ├── Login.js             # Login page
│   ├── Signup.js            # Registration page
│   ├── Profiles.js          # Profile selection/creation
│   ├── Movies.js            # Movie catalog
│   ├── TVShows.js           # TV show catalog
│   └── Watchlist.js         # User watchlist
├── components/              # Reusable components
│   ├── Navbar.js           # Navigation bar
│   ├── MovieCard.js        # Content card component
│   ├── SearchBar.js        # Search functionality
│   ├── GenreFilter.js      # Genre filtering
│   └── ProfileCard.js      # Profile display card
├── services/
│   └── api.js              # Axios API client with JWT
├── App.js                  # Main app with routing
├── App.css                 # Global styles
└── index.js                # Entry point
```

## 🎨 Features

### Pages
1. **Home** - Featured movies and TV shows
2. **Login** - User authentication
3. **Signup** - New user registration
4. **Profiles** - Create and select profiles
5. **Movies** - Browse all movies with search/filter
6. **TV Shows** - Browse all TV shows with search/filter
7. **Watchlist** - View and manage watchlist

### Components
- **Navbar** - Responsive navigation with auth state
- **MovieCard** - Reusable content card with poster, title, ratings
- **SearchBar** - Real-time search functionality
- **GenreFilter** - Filter content by genre
- **ProfileCard** - Profile selection cards

## 🎨 Theme

Dark purple theme:
- Background: `#1a0033`
- Primary: `#9b59b6`
- Hover: `#8e44ad`
- Text: `#ecf0f1`
- Card background: `#2c003e`

## 🔐 Authentication

- JWT tokens stored in `localStorage`
- Automatic token attachment to API requests
- Protected routes redirect to login
- Profile ID stored for watchlist operations

## 📦 Dependencies

```json
{
  "react": "^19.2.0",
  "react-router-dom": "^6.20.0",
  "axios": "^1.6.2"
}
```

## 🛠 Available Scripts

### `npm start`
Runs the app in development mode on `http://localhost:3000`

### `npm test`
Launches the test runner

### `npm run build`
Builds the app for production to the `build` folder

### `npm run eject`
**One-way operation** - ejects from Create React App

## 🔧 Configuration

### API Client (`src/services/api.js`)
```javascript
const API_BASE_URL = 'http://127.0.0.1:3001/api';
```

Automatically includes JWT token in requests:
```javascript
Authorization: Bearer <token>
```

### Routing (`App.js`)
```javascript
/             → Home
/login        → Login
/signup       → Signup
/profiles     → Profiles
/movies       → Movies
/tvshows      → TVShows
/watchlist    → Watchlist
```

## 📝 Development Notes

### Data Flow
1. User logs in → JWT token saved to localStorage
2. User selects profile → Profile ID saved to localStorage
3. API calls include both JWT and profile ID
4. Backend returns PascalCase → Frontend expects snake_case

### Key Features
- All content shows unique TMDB posters
- Search works across title and description
- Genre filtering with 17 genres
- Watchlist uses stored procedures on backend
- Average ratings update automatically via triggers

## 🧪 Testing

1. Start backend server first (`cd backend && python app.py`)
2. Start frontend (`npm start`)
3. Register new account or use test credentials
4. Create a profile
5. Test features:
   - Browse movies/TV shows
   - Search functionality
   - Genre filtering
   - Add to watchlist
   - View watchlist

## 📱 Responsive Design

- Desktop-optimized layout
- Grid-based content display
- Responsive navigation
- Mobile-friendly cards

---

Built with React and Create React App

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
