import React, { useState, useEffect } from 'react';
import { FiBookmark } from 'react-icons/fi';
import MovieCard from '../components/MovieCard';
import { watchlistAPI } from '../services/api';
import './Watchlist.css';

const Watchlist = () => {
  const [watchlistItems, setWatchlistItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, movies, tvshows

  useEffect(() => {
    fetchWatchlist();
  }, []);

  const fetchWatchlist = async () => {
    try {
      setLoading(true);
      const profile = JSON.parse(localStorage.getItem('selectedProfile'));
      
      if (!profile) {
        setLoading(false);
        return;
      }
      
      const response = await watchlistAPI.getAll(profile.profile_id);
      setWatchlistItems(response.data.watchlist || []);
    } catch (err) {
      console.error('Error fetching watchlist:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFromWatchlist = (itemId) => {
    setWatchlistItems(prev => prev.filter(item => 
      !(item.movie_id === itemId || item.tv_show_id === itemId)
    ));
  };

  const getFilteredItems = () => {
    if (filter === 'movies') {
      return watchlistItems.filter(item => item.movie_id);
    }
    if (filter === 'tvshows') {
      return watchlistItems.filter(item => item.tv_show_id);
    }
    return watchlistItems;
  };

  const filteredItems = getFilteredItems();

  if (loading) {
    return (
      <div className="watchlist-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading your watchlist...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="watchlist-page">
      <div className="watchlist-header">
        <div className="header-content">
          <div className="header-title">
            <FiBookmark className="header-icon" />
            <h1>My List</h1>
          </div>
          <p className="subtitle">
            {filteredItems.length} {filteredItems.length === 1 ? 'item' : 'items'} in your watchlist
          </p>
        </div>
      </div>
      
      <div className="container">
        {watchlistItems.length === 0 ? (
          <div className="empty-watchlist">
            <FiBookmark className="empty-icon" />
            <h2>Your watchlist is empty</h2>
            <p>Start adding movies and TV shows to watch later</p>
          </div>
        ) : (
          <>
            <div className="watchlist-filters">
              <button 
                className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                onClick={() => setFilter('all')}
              >
                All ({watchlistItems.length})
              </button>
              <button 
                className={`filter-btn ${filter === 'movies' ? 'active' : ''}`}
                onClick={() => setFilter('movies')}
              >
                Movies ({watchlistItems.filter(item => item.movie_id).length})
              </button>
              <button 
                className={`filter-btn ${filter === 'tvshows' ? 'active' : ''}`}
                onClick={() => setFilter('tvshows')}
              >
                TV Shows ({watchlistItems.filter(item => item.tv_show_id).length})
              </button>
            </div>
            
            <div className="watchlist-grid">
              {filteredItems.map(item => {
                const isMovie = !!item.movie_id;
                return (
                  <MovieCard
                    key={isMovie ? `movie-${item.movie_id}` : `show-${item.tv_show_id}`}
                    content={item}
                    type={isMovie ? 'Movie' : 'TV_Show'}
                    profileId={localStorage.getItem('profileId')}
                    isFromWatchlist={true}
                  />
                );
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Watchlist;
