import axios from 'axios';

const API_BASE_URL = 'http://localhost:3001/api';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle responses and errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  signup: (data) => api.post('/user/signup', data),
  login: (data) => api.post('/user/login', data),
  logout: () => api.post('/user/logout'),
};

// User APIs
export const userAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/update', data),
  changePassword: (data) => api.put('/users/change-password', data),
};

// Profile APIs
export const profileAPI = {
  create: (data) => api.post('/profile/create', data),
  list: () => api.get('/profile/list'),
  delete: (id) => api.delete(`/profile/delete/${id}`),
};

// Movies APIs
export const moviesAPI = {
  getAll: () => api.get('/movies/'),
  getById: (id) => api.get(`/movies/${id}`),
  getByGenre: (genre) => api.get(`/movies/genre/${genre}`),
};

// TV Shows APIs
export const tvShowsAPI = {
  getAll: () => api.get('/tvshows/'),
  getById: (id) => api.get(`/tvshows/${id}`),
  getByGenre: (genre) => api.get(`/tvshows/genre/${genre}`),
};

// Genres APIs
export const genresAPI = {
  getAll: () => api.get('/genres/'),
  getById: (id) => api.get(`/genres/${id}`),
};

// Home Page API
export const homeAPI = {
  getContent: () => api.get('/home/'),
};

// Watchlist APIs
export const watchlistAPI = {
  add: (data) => api.post('/watchlist/add', data),
  remove: (data) => api.delete('/watchlist/remove', { data }),
  getAll: (profileId) => api.get(`/watchlist/all/${profileId}`),
};

// Ratings APIs
export const ratingsAPI = {
  add: (data) => api.post('/ratings/add', data),
  getByContent: (contentType, contentId) =>
    api.get(`/ratings/content/${contentType}/${contentId}`),
  getByProfile: (profileId) => api.get(`/ratings/profile/${profileId}`),
};

// Viewing History APIs
export const viewingHistoryAPI = {
  log: (data) => api.post('/viewing_history/log', data),
  getByProfile: (profileId) => api.get(`/viewing_history/profile/${profileId}`),
  delete: (historyId) => api.delete(`/viewing_history/delete/${historyId}`),
};

// Subscriptions APIs
export const subscriptionsAPI = {
  getPlans: () => api.get('/subscriptions/plans'),
  subscribe: (data) => api.post('/subscriptions/subscribe', data),
  create: (data) => api.post('/subscriptions/create', data),
  list: () => api.get('/subscriptions/list'),
  getStatus: () => api.get('/subscriptions/status'),
};

// Payments APIs
export const paymentsAPI = {
  create: (data) => api.post('/payments/create', data),
  getBySubscription: (subscriptionId) =>
    api.get(`/payments/subscription/${subscriptionId}`),
  getHistory: () => api.get('/payments/history'),
};

export default api;
