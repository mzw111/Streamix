import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FiArrowLeft, FiPlay, FiPlus, FiCheck, FiStar } from 'react-icons/fi';
import VideoPlayer from '../components/VideoPlayer';
import RatingModal from '../components/RatingModal';
import { moviesAPI, watchlistAPI, ratingsAPI, viewingHistoryAPI } from '../services/api';
import './MovieDetail.css';

const MovieDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showVideo, setShowVideo] = useState(false);
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [watchDuration, setWatchDuration] = useState(0);

  const profileId = localStorage.getItem('profileId');

  useEffect(() => {
    fetchMovieDetails();
    checkIfInWatchlist();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchMovieDetails = async () => {
    try {
      setLoading(true);
      const response = await moviesAPI.getById(id);
      setMovie(response.data.movie);
    } catch (err) {
      console.error('Error fetching movie:', err);
    } finally {
      setLoading(false);
    }
  };

  const checkIfInWatchlist = async () => {
    if (!profileId) return;

    try {
      const response = await watchlistAPI.getAll(profileId);
      const watchlist = response.data.watchlist || [];
      const isInList = watchlist.some(item => 
        item.content_type === 'Movie' && parseInt(item.content_id) === parseInt(id)
      );
      setIsInWatchlist(isInList);
    } catch (error) {
      console.error('Error checking watchlist:', error);
    }
  };

  const handlePlayClick = () => {
    setShowVideo(true);
  };

  const handleVideoTimeUpdate = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    setWatchDuration(minutes);
    // Log viewing history only when video ends to reduce database load
  };

  const handleVideoEnded = () => {
    // Log final viewing history when video ends
    const finalDuration = Math.max(watchDuration, 1);
    logViewingHistory(finalDuration);
  };

  const logViewingHistory = async (duration) => {
    if (!profileId || !movie) return;

    try {
      await viewingHistoryAPI.log({
        profile_id: parseInt(profileId),
        content_type: 'Movie',
        content_id: parseInt(movie.movie_id),
        watch_duration: duration || watchDuration
      });
      console.log('✅ Viewing history logged');
    } catch (error) {
      console.error('❌ Failed to log viewing history:', error);
    }
  };

  const handleWatchlist = async () => {
    if (!profileId) {
      alert('Please select a profile first!');
      return;
    }

    try {
      const watchlistData = {
        profile_id: parseInt(profileId),
        content_type: 'Movie',
        content_id: parseInt(movie.movie_id)
      };

      if (isInWatchlist) {
        await watchlistAPI.remove(watchlistData);
        setIsInWatchlist(false);
        alert('Removed from watchlist!');
      } else {
        await watchlistAPI.add(watchlistData);
        setIsInWatchlist(true);
        alert('Added to watchlist!');
      }
    } catch (error) {
      console.error('Watchlist error:', error);
      alert(`Failed to update watchlist: ${error.response?.data?.message || error.message}`);
    }
  };

  const handleRatingSubmit = async (ratingData) => {
    if (!profileId) {
      alert('Please select a profile first!');
      return;
    }

    try {
      await ratingsAPI.add({
        profile_id: parseInt(profileId),
        content_type: 'Movie',
        content_id: parseInt(movie.movie_id),
        rating: parseFloat(ratingData.rating),
        review_text: ratingData.review_text || null
      });
      alert('Rating submitted successfully!');
      setShowRatingModal(false);
      fetchMovieDetails(); // Refresh to get updated rating
    } catch (error) {
      console.error('Rating error:', error);
      alert(`Failed to submit rating: ${error.response?.data?.message || error.message}`);
    }
  };

  if (loading) {
    return (
      <div className="movie-detail-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading movie...</p>
        </div>
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="movie-detail-page">
        <div className="error-container">
          <h2>Movie not found</h2>
          <button className="btn btn-primary" onClick={() => navigate('/movies')}>
            Back to Movies
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="movie-detail-page">
      <div className="movie-detail-header">
        <button className="back-btn" onClick={() => navigate('/movies')}>
          <FiArrowLeft /> Back
        </button>
      </div>

      {showVideo && movie.video_url ? (
        <VideoPlayer
          videoUrl={movie.video_url}
          onTimeUpdate={handleVideoTimeUpdate}
          onEnded={handleVideoEnded}
        />
      ) : (
        <div className="movie-hero">
          <img
            src={movie.poster_url || 'https://via.placeholder.com/1200x600'}
            alt={movie.title}
            className="movie-backdrop"
          />
          <div className="movie-hero-overlay">
            <div className="movie-hero-content">
              <h1>{movie.title}</h1>
              <div className="movie-meta">
                {movie.release_year && <span>{movie.release_year}</span>}
                {movie.duration && <span>{movie.duration} min</span>}
                {movie.age_rating && <span className="age-badge">{movie.age_rating}</span>}
                {movie.average_rating > 0 && (
                  <span className="rating-badge">
                    <FiStar /> {Number(movie.average_rating).toFixed(1)}
                  </span>
                )}
              </div>

              <div className="movie-actions">
                {movie.video_url ? (
                  <button className="btn btn-primary btn-large" onClick={handlePlayClick}>
                    <FiPlay /> Play
                  </button>
                ) : (
                  <button className="btn btn-primary btn-large" disabled>
                    <FiPlay /> Video Not Available
                  </button>
                )}

                <button
                  className="btn btn-secondary"
                  onClick={handleWatchlist}
                  title={isInWatchlist ? 'Remove from list' : 'Add to list'}
                >
                  {isInWatchlist ? <FiCheck /> : <FiPlus />}
                  {isInWatchlist ? 'In Watchlist' : 'Add to Watchlist'}
                </button>

                <button
                  className="btn btn-secondary"
                  onClick={() => setShowRatingModal(true)}
                >
                  <FiStar /> Rate
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="movie-detail-content">
        <div className="movie-info-section">
          <h2>Overview</h2>
          <p className="movie-description">
            {movie.description || 'No description available.'}
          </p>

          {movie.genres && movie.genres.length > 0 && (
            <div className="movie-genres">
              <h3>Genres</h3>
              <div className="genre-tags">
                {movie.genres.map((genre) => (
                  <span key={genre.genre_id} className="genre-tag">
                    {genre.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <RatingModal
        isOpen={showRatingModal}
        onClose={() => setShowRatingModal(false)}
        onSubmit={handleRatingSubmit}
        contentTitle={movie.title}
      />
    </div>
  );
};

export default MovieDetail;
