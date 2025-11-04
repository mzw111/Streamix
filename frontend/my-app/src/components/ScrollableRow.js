import React, { useRef } from 'react';
import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';
import MovieCard from './MovieCard';
import './ScrollableRow.css';

const ScrollableRow = ({ title, items, type = 'Movie', profileId }) => {
  const rowRef = useRef(null);

  const scroll = (direction) => {
    if (rowRef.current) {
      const scrollAmount = direction === 'left' ? -800 : 800;
      rowRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  if (!items || items.length === 0) {
    return null;
  }

  return (
    <div className="scrollable-row">
      <h2 className="row-title">{title}</h2>
      
      <div className="row-container">
        <button
          className="scroll-btn scroll-left"
          onClick={() => scroll('left')}
          aria-label="Scroll left"
        >
          <FiChevronLeft />
        </button>

        <div className="row-content" ref={rowRef}>
          {items.map((item) => (
            <MovieCard
              key={item.Movie_Id || item.Show_Id || item.Content_Id}
              content={item}
              type={type}
              profileId={profileId}
            />
          ))}
        </div>

        <button
          className="scroll-btn scroll-right"
          onClick={() => scroll('right')}
          aria-label="Scroll right"
        >
          <FiChevronRight />
        </button>
      </div>
    </div>
  );
};

export default ScrollableRow;
