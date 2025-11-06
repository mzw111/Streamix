import React, { useState, useEffect } from 'react';
import { FiClock, FiTrash2, FiCalendar } from 'react-icons/fi';
import { viewingHistoryAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';
import './ViewingHistory.css';

// Viewing History Page - Shows all watched content for the current profile
const ViewingHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const profileId = localStorage.getItem('profileId');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const response = await viewingHistoryAPI.getByProfile(profileId);
        console.log('Full history response:', response);
        console.log('History response data:', response.data);
        
        // Handle both possible response structures
        let historyData = [];
        if (response.data.success) {
          historyData = response.data.history || response.data.viewing_history || [];
        } else {
          historyData = response.data.history || response.data.viewing_history || response.data || [];
        }
        
        console.log('Extracted history data:', historyData);
        
        // Ensure it's an array
        if (Array.isArray(historyData)) {
          setHistory(historyData);
        } else {
          console.error('History data is not an array:', historyData);
          setHistory([]);
        }
      } catch (error) {
        console.error('Error fetching history:', error);
        setHistory([]);
      } finally {
        setLoading(false);
      }
    };

    if (!profileId) {
      navigate('/profiles');
      return;
    }
    fetchHistory();
  }, [profileId, navigate]);

  const handleDelete = async (historyId) => {
    if (!window.confirm('Remove this entry from your viewing history?')) {
      return;
    }

    try {
      await viewingHistoryAPI.delete(historyId);
      setHistory(history.filter(item => item.History_Id !== historyId));
    } catch (error) {
      console.error('Error deleting history:', error);
      alert('Failed to delete history entry');
    }
  };

  const handleItemClick = (item) => {
    const contentType = item.Content_Type === 'TV_Show' ? 'tv_show' : 'movie';
    const contentId = item.Content_Id;
    navigate(`/${contentType}/${contentId}`);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="viewing-history-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading viewing history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="viewing-history-page">
      <div className="history-header">
        <h1>Viewing History</h1>
        <p className="subtitle">
          {!Array.isArray(history) || history.length === 0 
            ? 'No viewing history yet' 
            : `${history.length} item${history.length !== 1 ? 's' : ''} watched`}
        </p>
      </div>

      <div className="container">
        {!Array.isArray(history) || history.length === 0 ? (
          <div className="empty-state">
            <FiClock size={64} />
            <h2>No viewing history</h2>
            <p>Start watching movies and TV shows to see your history here!</p>
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/movies')}
            >
              Browse Movies
            </button>
          </div>
        ) : (
          <div className="history-list">
            {history.map((item) => (
              <div 
                key={item.History_Id} 
                className="history-item"
                onClick={() => handleItemClick(item)}
              >
                <div className="history-info">
                  <h3 className="history-title">
                    {item.Title || 'Unknown Title'}
                  </h3>
                  <div className="history-meta">
                    <span className="history-type">
                      {item.Content_Type === 'TV_Show' ? 'TV Show' : 'Movie'}
                    </span>
                    <span className="separator">•</span>
                    <span className="history-date">
                      <FiCalendar size={14} />
                      {formatDate(item.Watch_Date)}
                    </span>
                    {item.Watch_Duration > 0 && (
                      <>
                        <span className="separator">•</span>
                        <span className="history-duration">
                          <FiClock size={14} />
                          {item.Watch_Duration} min
                        </span>
                      </>
                    )}
                  </div>
                </div>
                <button
                  className="delete-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(item.History_Id);
                  }}
                  title="Remove from history"
                >
                  <FiTrash2 />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ViewingHistory;

