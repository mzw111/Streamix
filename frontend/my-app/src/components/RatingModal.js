import React, { useState } from 'react';
import { FiStar, FiX } from 'react-icons/fi';
import './RatingModal.css';

const RatingModal = ({ isOpen, onClose, onSubmit, contentTitle, currentRating = 0 }) => {
  const [rating, setRating] = useState(currentRating || 0);
  const [hoverRating, setHoverRating] = useState(0);
  const [reviewText, setReviewText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (rating === 0) {
      alert('Please select a rating');
      return;
    }

    setSubmitting(true);
    try {
      await onSubmit({ rating, review_text: reviewText });
      setRating(0);
      setReviewText('');
      onClose();
    } catch (error) {
      console.error('Rating submission error:', error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="rating-modal-overlay" onClick={onClose}>
      <div className="rating-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-modal-btn" onClick={onClose}>
          <FiX />
        </button>
        
        <h2>Rate {contentTitle}</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="rating-stars-container">
            <div className="rating-stars">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  className={`star-btn ${star <= (hoverRating || rating) ? 'active' : ''}`}
                  onClick={() => setRating(star)}
                  onMouseEnter={() => setHoverRating(star)}
                  onMouseLeave={() => setHoverRating(0)}
                >
                  <FiStar />
                </button>
              ))}
            </div>
            <p className="rating-value">
              {hoverRating || rating ? `${hoverRating || rating}/5` : 'Select a rating'}
            </p>
          </div>

          <div className="form-group">
            <label htmlFor="review">Review (Optional)</label>
            <textarea
              id="review"
              placeholder="Share your thoughts about this content..."
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              rows="4"
              maxLength="500"
            />
            <span className="char-count">{reviewText.length}/500</span>
          </div>

          <div className="modal-actions">
            <button 
              type="button" 
              className="btn btn-secondary"
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={submitting || rating === 0}
            >
              {submitting ? 'Submitting...' : 'Submit Rating'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RatingModal;
