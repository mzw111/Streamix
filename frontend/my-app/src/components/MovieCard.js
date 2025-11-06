import React, { useState } from 'react';
import { FiPlay, FiPlus, FiCheck, FiInfo, FiStar } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';
import { watchlistAPI, ratingsAPI, viewingHistoryAPI } from '../services/api';
import RatingModal from './RatingModal';
import './MovieCard.css';

const MovieCard = ({ content, type = 'Movie', profileId }) => {
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const navigate = useNavigate();

  // Safety check
  if (!content) {
    return null;
  }

  // Get the correct ID based on content type
  const contentId = content.movie_id || content.tv_show_id || content.show_id || content.Movie_Id || content.Show_Id || content.content_id;
  const title = content.title || content.Title || 'Untitled';
  const rating = content.rating || content.average_rating || 0;

  const handleWatchlist = async (e) => {
    e.stopPropagation();
    
    if (!profileId) {
      alert('Please select or create a profile first!');
      return;
    }

    if (!contentId) {
      console.error('Content ID not found:', content);
      alert('Cannot add to watchlist: Content ID missing');
      return;
    }
    
    const watchlistData = {
      profile_id: parseInt(profileId),
      content_type: type === 'TV_Show' ? 'TV_Show' : 'Movie',
      content_id: parseInt(contentId),
    };

    console.log('Watchlist request:', watchlistData);
    
    try {
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
      console.error('Error details:', error.response?.data);
      alert(`Failed to update watchlist: ${error.response?.data?.message || error.message}`);
    }
  };

  const handleClick = async () => {
    // Log viewing history when clicking on content
    if (profileId && contentId) {
      try {
        const historyData = {
          profile_id: parseInt(profileId),
          content_type: type === 'TV_Show' ? 'TV_Show' : 'Movie',
          content_id: parseInt(contentId),
          watch_duration: 120 // Set to 120 minutes as default watch duration
        };
        console.log('Logging viewing history:', historyData);
        const response = await viewingHistoryAPI.log(historyData);
        console.log('✅ Viewing history logged successfully:', response.data);
      } catch (error) {
        console.error('❌ Failed to log viewing history:', error);
        console.error('Error response:', error.response?.data);
        // Don't block navigation if logging fails
      }
    }
    navigate(`/${type.toLowerCase()}/${contentId}`);
  };

  const handleRatingSubmit = async (ratingData) => {
    if (!profileId) {
      alert('Please select a profile first!');
      return;
    }

    if (!contentId) {
      alert('Content ID is missing!');
      return;
    }

    try {
      await ratingsAPI.add({
        profile_id: parseInt(profileId),
        content_type: type === 'TV_Show' ? 'TV_Show' : 'Movie',
        content_id: parseInt(contentId),
        rating: parseFloat(ratingData.rating),
        review_text: ratingData.review_text || null
      });
      alert('Rating submitted successfully! The average rating will be updated automatically.');
      setShowRatingModal(false);
    } catch (error) {
      console.error('Rating error:', error);
      alert(`Failed to submit rating: ${error.response?.data?.message || error.message}`);
    }
  };

  // Placeholder image if none provided
  const posterUrl = content.poster_url || `https://via.placeholder.com/300x450/1a1a2e/8B5CF6?text=${encodeURIComponent(title)}`;

  return (
    <>
      <div
        className="movie-card"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={handleClick}
      >
        <div className="movie-card-image">
          <img src={posterUrl} alt={title} loading="lazy" />
          
          {isHovered && (
            <div className="movie-card-overlay">
              <button className="play-btn">
                <FiPlay />
              </button>
              
              <div className="card-actions">
                <button
                  className="action-btn"
                  onClick={handleWatchlist}
                  title={isInWatchlist ? 'Remove from list' : 'Add to list'}
                >
                  {isInWatchlist ? <FiCheck /> : <FiPlus />}
                </button>
                
                <button
                  className="action-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowRatingModal(true);
                  }}
                  title="Rate this"
                >
                  <FiStar />
                </button>
                
                <button
                  className="action-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/${type.toLowerCase()}/${contentId}`);
                  }}
                  title="More info"
                >
                  <FiInfo />
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="movie-card-info">
          <h4 className="movie-title">{title}</h4>
          {rating > 0 && (
            <div className="movie-rating">
              <span className="rating-star">★</span>
              <span>{Number(rating).toFixed(1)}</span>
            </div>
          )}
          {(content.release_year || content.Release_Year) && (
            <span className="movie-year">
              {content.release_year || content.Release_Year}
            </span>
          )}
          {content.Release_Date && (
            <span className="movie-year">
              {new Date(content.Release_Date).getFullYear()}
            </span>
          )}
          {(content.duration || content.Duration) && (
            <span className="movie-duration">{content.duration || content.Duration} min</span>
          )}
          {(content.total_seasons) && (
            <span className="movie-duration">{content.total_seasons} Season{content.total_seasons !== 1 ? 's' : ''}</span>
          )}
        </div>
      </div>

      <RatingModal
        isOpen={showRatingModal}
        onClose={() => setShowRatingModal(false)}
        onSubmit={handleRatingSubmit}
        contentTitle={title}
      />
    </>
  );
};

export default MovieCard;
