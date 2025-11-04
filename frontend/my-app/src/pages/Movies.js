import React, { useState, useEffect } from 'react';
import { FiSearch, FiFilter } from 'react-icons/fi';
import MovieCard from '../components/MovieCard';
import { moviesAPI, genresAPI } from '../services/api';
import './Movies.css';

const Movies = () => {
  const [movies, setMovies] = useState([]);
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
      const [moviesResponse, genresResponse] = await Promise.all([
        moviesAPI.getAll(),
        genresAPI.getAll()
      ]);
      
      setMovies(moviesResponse.data.movies || []);
      setGenres(genresResponse.data.genres || []);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredAndSortedMovies = () => {
    let filtered = [...movies];
    
    // Search filter
    if (searchQuery.trim()) {
      filtered = filtered.filter(movie =>
        movie.title.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    // Genre filter
    if (selectedGenre !== 'all') {
      filtered = filtered.filter(movie =>
        movie.genres?.some(g => g.genre_id === parseInt(selectedGenre))
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
        case 'duration':
          return b.duration - a.duration;
        default:
          return 0;
      }
    });
    
    return filtered;
  };

  const filteredMovies = getFilteredAndSortedMovies();

  if (loading) {
    return (
      <div className="movies-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading movies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="movies-page">
      <div className="movies-header">
        <div className="header-content">
          <h1>Movies</h1>
          <p className="subtitle">{filteredMovies.length} movies available</p>
        </div>
      </div>
      
      <div className="container">
        <div className="movies-controls">
          <div className="search-box">
            <FiSearch className="search-icon" />
            <input
              type="text"
              placeholder="Search movies..."
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
                <option value="duration">Longest First</option>
              </select>
            </div>
          </div>
        </div>
        
        {filteredMovies.length === 0 ? (
          <div className="no-results">
            <p>No movies found</p>
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
          <div className="movies-grid">
            {filteredMovies.map(movie => (
              <MovieCard
                key={movie.movie_id}
                content={movie}
                type="Movie"
                profileId={localStorage.getItem('profileId')}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Movies;
