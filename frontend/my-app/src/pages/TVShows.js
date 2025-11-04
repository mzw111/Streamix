import React, { useState, useEffect } from 'react';
import { FiSearch, FiFilter } from 'react-icons/fi';
import MovieCard from '../components/MovieCard';
import { tvShowsAPI, genresAPI } from '../services/api';
import './TVShows.css';

const TVShows = () => {
  const [tvShows, setTvShows] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('all');
  const [sortBy, setSortBy] = useState('rating');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [showsResponse, genresResponse] = await Promise.all([
        tvShowsAPI.getAll(),
        genresAPI.getAll()
      ]);
      
      setTvShows(showsResponse.data.tv_shows || []);
      setGenres(genresResponse.data.genres || []);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredAndSortedShows = () => {
    let filtered = [...tvShows];
    
    // Search filter
    if (searchQuery.trim()) {
      filtered = filtered.filter(show =>
        show.title.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    // Genre filter
    if (selectedGenre !== 'all') {
      filtered = filtered.filter(show =>
        show.genres?.some(g => g.genre_id === parseInt(selectedGenre))
      );
    }
    
    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'rating':
          return (b.average_rating || 0) - (a.average_rating || 0);
        case 'year':
          return b.release_year - a.release_year;
        case 'title':
          return a.title.localeCompare(b.title);
        case 'seasons':
          return b.total_seasons - a.total_seasons;
        default:
          return 0;
      }
    });
    
    return filtered;
  };

  const filteredShows = getFilteredAndSortedShows();

  if (loading) {
    return (
      <div className="tvshows-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading TV shows...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tvshows-page">
      <div className="tvshows-header">
        <div className="header-content">
          <h1>TV Shows</h1>
          <p className="subtitle">{filteredShows.length} shows available</p>
        </div>
      </div>
      
      <div className="container">
        <div className="tvshows-controls">
          <div className="search-box">
            <FiSearch className="search-icon" />
            <input
              type="text"
              placeholder="Search TV shows..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          <div className="filters">
            <div className="filter-group">
              <FiFilter />
              <select
                value={selectedGenre}
                onChange={(e) => setSelectedGenre(e.target.value)}
              >
                <option value="all">All Genres</option>
                {genres.map(genre => (
                  <option key={genre.genre_id} value={genre.genre_id}>
                    {genre.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="filter-group">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="rating">Highest Rated</option>
                <option value="year">Newest First</option>
                <option value="title">A-Z</option>
                <option value="seasons">Most Seasons</option>
              </select>
            </div>
          </div>
        </div>
        
        {filteredShows.length === 0 ? (
          <div className="no-results">
            <p>No TV shows found</p>
            <button 
              className="btn btn-secondary"
              onClick={() => {
                setSearchQuery('');
                setSelectedGenre('all');
              }}
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="tvshows-grid">
            {filteredShows.map(show => (
              <MovieCard
                key={show.tv_show_id}
                content={show}
                type="TV_Show"
                profileId={localStorage.getItem('profileId')}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TVShows;
