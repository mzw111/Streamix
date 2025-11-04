import React from 'react';
import { FiPlay, FiInfo } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';
import './HeroSection.css';

const HeroSection = ({ content }) => {
  const navigate = useNavigate();

  if (!content) return null;

  const backdropUrl = content.backdrop_url || `https://via.placeholder.com/1920x800/1a1a2e/8B5CF6?text=${encodeURIComponent(content.Title || 'Featured Content')}`;

  const handlePlay = () => {
    const id = content.Movie_Id || content.Show_Id || content.Content_Id;
    const type = content.Content_Type === 'TV_Show' ? 'tv-shows' : 'movies';
    navigate(`/${type}/${id}`);
  };

  const handleMoreInfo = () => {
    const id = content.Movie_Id || content.Show_Id || content.Content_Id;
    const type = content.Content_Type === 'TV_Show' ? 'tv-shows' : 'movies';
    navigate(`/${type}/${id}`);
  };

  return (
    <div className="hero-section">
      <div className="hero-background">
        <img src={backdropUrl} alt={content.Title} />
        <div className="hero-gradient"></div>
      </div>

      <div className="hero-content">
        <div className="hero-info">
          <h1 className="hero-title">{content.Title}</h1>
          
          <p className="hero-description">
            {content.Description || 'A captivating story that will keep you on the edge of your seat. Discover this amazing content and experience entertainment like never before.'}
          </p>

          <div className="hero-meta">
            {content.average_rating && (
              <span className="hero-rating">
                <span className="rating-star">★</span>
                {Number(content.average_rating).toFixed(1)}
              </span>
            )}
            {content.Release_Date && (
              <span className="hero-year">
                {new Date(content.Release_Date).getFullYear()}
              </span>
            )}
            {content.Release_Year && (
              <span className="hero-year">{content.Release_Year}</span>
            )}
            {content.Duration && (
              <span className="hero-duration">{content.Duration} min</span>
            )}
            {content.Age_Rating && (
              <span className="hero-rating-badge">{content.Age_Rating}</span>
            )}
          </div>

          <div className="hero-buttons">
            <button className="btn btn-primary hero-play-btn" onClick={handlePlay}>
              <FiPlay /> Play
            </button>
            <button className="btn btn-secondary hero-info-btn" onClick={handleMoreInfo}>
              <FiInfo /> More Info
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
