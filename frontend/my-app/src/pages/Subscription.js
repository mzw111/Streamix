import React, { useState, useEffect } from 'react';
import { FiCheck, FiClock, FiPackage } from 'react-icons/fi';
import { subscriptionsAPI } from '../services/api';
import Navbar from '../components/Navbar';
import './Subscription.css';

const Subscription = () => {
  const [plans, setPlans] = useState([]);
  const [currentStatus, setCurrentStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [subscribing, setSubscribing] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch plans
      const plansResponse = await subscriptionsAPI.getPlans();
      setPlans(plansResponse.data.plans || []);
      
      // Fetch current status
      const statusResponse = await subscriptionsAPI.getStatus();
      setCurrentStatus(statusResponse.data);
      
      setError('');
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load subscription data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async (planId) => {
    try {
      setSubscribing(true);
      setError('');
      
      await subscriptionsAPI.subscribe({ plan_id: planId });
      
      // Refresh status
      await fetchData();
      
      alert('Subscription successful!');
    } catch (err) {
      console.error('Subscription error:', err);
      setError(err.response?.data?.message || 'Failed to subscribe');
      alert('Failed to subscribe: ' + (err.response?.data?.message || err.message));
    } finally {
      setSubscribing(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active':
        return '#10b981'; // green
      case 'Expired':
        return '#ef4444'; // red
      default:
        return '#6b7280'; // gray
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Active':
        return <FiCheck />;
      case 'Expired':
        return <FiClock />;
      default:
        return <FiPackage />;
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="subscription-page">
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading subscription data...</p>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="subscription-page">
        <div className="subscription-container">
          <div className="subscription-header">
            <h1>Subscription Plans</h1>
            <p className="subtitle">Choose the perfect plan for you</p>
          </div>

          {error && <div className="error-banner">{error}</div>}

          {/* Current Status Card */}
          {currentStatus && (
            <div className="current-status-card">
              <div className="status-header">
                <h2>Current Subscription Status</h2>
                <div 
                  className="status-badge"
                  style={{ 
                    backgroundColor: getStatusColor(currentStatus.status),
                    color: 'white'
                  }}
                >
                  <span className="status-icon">{getStatusIcon(currentStatus.status)}</span>
                  {currentStatus.status}
                </div>
              </div>

              {currentStatus.subscription && (
                <div className="status-details">
                  <div className="detail-item">
                    <span className="detail-label">Start Date:</span>
                    <span className="detail-value">
                      {new Date(currentStatus.subscription.start_date).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">End Date:</span>
                    <span className="detail-value">
                      {new Date(currentStatus.subscription.end_date).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Payment Status:</span>
                    <span className="detail-value">{currentStatus.subscription.payment_status}</span>
                  </div>
                </div>
              )}

              {currentStatus.status === 'None' && (
                <p className="no-subscription-text">
                  You don't have an active subscription. Choose a plan below to get started!
                </p>
              )}

              {currentStatus.status === 'Expired' && (
                <p className="expired-text">
                  Your subscription has expired. Renew now to continue enjoying our content!
                </p>
              )}
            </div>
          )}

          {/* Subscription Plans */}
          <div className="plans-grid">
            {plans.map((plan) => (
              <div key={plan.id} className="plan-card">
                <div className="plan-header">
                  <h3>{plan.name}</h3>
                  <div className="plan-price">
                    <span className="price-value">FREE</span>
                  </div>
                </div>

                <p className="plan-description">{plan.description}</p>

                <ul className="plan-features">
                  <li>
                    <FiCheck className="feature-icon" />
                    {plan.duration_months} Month{plan.duration_months > 1 ? 's' : ''} Access
                  </li>
                  <li>
                    <FiCheck className="feature-icon" />
                    Unlimited Streaming
                  </li>
                  <li>
                    <FiCheck className="feature-icon" />
                    All Movies & TV Shows
                  </li>
                  <li>
                    <FiCheck className="feature-icon" />
                    HD Quality
                  </li>
                  <li>
                    <FiCheck className="feature-icon" />
                    Multiple Profiles
                  </li>
                </ul>

                <button
                  className="subscribe-btn"
                  onClick={() => handleSubscribe(plan.id)}
                  disabled={subscribing || currentStatus?.status === 'Active'}
                >
                  {subscribing ? 'Processing...' : 
                   currentStatus?.status === 'Active' ? 'Currently Active' : 'Subscribe Now'}
                </button>
              </div>
            ))}
          </div>

          <div className="subscription-footer">
            <p>All plans are currently FREE for testing purposes</p>
            <p>Status is checked using database function: <code>fn_GetSubscriptionStatus()</code></p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Subscription;
