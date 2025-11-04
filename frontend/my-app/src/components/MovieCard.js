import React, { useState } from 'react';
import { FiPlay, FiPlus, FiCheck, FiInfo } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';
import { watchlistAPI } from '../services/api';
import './MovieCard.css';

const MovieCard = ({ content, type = 'Movie', profileId }) => {
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const navigate = useNavigate();

  // Safety check
  if (!content) {
    return null;
  }

  // Get the correct ID based on content type
  const contentId = content.movie_id || content.tv_show_id || content.Movie_Id || content.Show_Id;
  const title = content.title || content.Title || 'Untitled';
  const rating = content.rating || content.average_rating || 0;

  const handleWatchlist = async (e) => {
    e.stopPropagation();
    
    if (!profileId) {
      alert('Please select or create a profile first!');
      return;
    }
    
    console.log('Watchlist request:', {
      profile_id: parseInt(profileId),
      content_type: type,
      content_id: contentId,
    });
    
    try {
      if (isInWatchlist) {
        await watchlistAPI.remove({
          profile_id: parseInt(profileId),
          content_type: type,
          content_id: contentId,
        });
        setIsInWatchlist(false);
      } else {
        await watchlistAPI.add({
          profile_id: parseInt(profileId),
          content_type: type,
          content_id: contentId,
        });
        setIsInWatchlist(true);
      }
    } catch (error) {
      console.error('Watchlist error:', error);
      console.error('Error details:', error.response?.data);
      alert(`Failed to update watchlist: ${error.response?.data?.message || error.message}`);
    }
  };

  const handleClick = () => {
    navigate(`/${type.toLowerCase()}/${contentId}`);
  };

  // Placeholder image if none provided
  const posterUrl = content.poster_url || `https://via.placeholder.com/300x450/1a1a2e/8B5CF6?text=${encodeURIComponent(title)}`;

  return (
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
  );
};

export default MovieCard;
