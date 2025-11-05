import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiPlus, FiEdit2, FiUser, FiTrash2 } from 'react-icons/fi';
import { profileAPI } from '../services/api';
import './Profiles.css';

const Profiles = () => {
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newProfileName, setNewProfileName] = useState('');
  const [creating, setCreating] = useState(false);
  const [manageMode, setManageMode] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  useEffect(() => {
    fetchProfiles();
  }, []);

  const fetchProfiles = async () => {
    try {
      setLoading(true);
      const response = await profileAPI.list();
      setProfiles(response.data.profiles || []);
    } catch (err) {
      setError('Failed to load profiles');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectProfile = (profile) => {
    // Store selected profile in localStorage
    localStorage.setItem('selectedProfile', JSON.stringify(profile));
    localStorage.setItem('profileId', profile.profile_id);
    navigate('/');
  };

  const handleCreateProfile = async (e) => {
    e.preventDefault();
    
    if (!newProfileName.trim()) {
      return;
    }
    
    if (profiles.length >= 5) {
      setError('Maximum 5 profiles allowed per account');
      return;
    }
    
    setCreating(true);
    setError('');
    
    try {
      const response = await profileAPI.create({ name: newProfileName.trim() });
      const newProfile = response.data.profile;
      setProfiles([...profiles, newProfile]);
      setNewProfileName('');
      setShowCreateModal(false);
      
      // Auto-select the new profile
      handleSelectProfile(newProfile);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create profile');
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteProfile = async (profileId) => {
    try {
      await profileAPI.delete(profileId);
      setProfiles(profiles.filter(p => p.profile_id !== profileId));
      setDeleteConfirm(null);
      setError('');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete profile');
    }
  };

  if (loading) {
    return (
      <div className="profiles-page">
        <div className="profiles-loading">
          <div className="spinner"></div>
          <p>Loading profiles...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profiles-page">
      <div className="profiles-container">
        <div className="profiles-header">
          <h1>Who's watching?</h1>
          {error && <p className="error-text">{error}</p>}
        </div>
        
        <div className="profiles-grid">
          {profiles.map((profile) => (
            <div 
              key={profile.profile_id}
              className={`profile-card ${manageMode ? 'manage-mode' : ''}`}
              onClick={() => !manageMode && handleSelectProfile(profile)}
            >
              <div className="profile-avatar">
                <FiUser />
              </div>
              <p className="profile-name">{profile.name}</p>
              {manageMode && (
                <button
                  className="delete-profile-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteConfirm(profile.profile_id);
                  }}
                >
                  <FiTrash2 />
                </button>
              )}
            </div>
          ))}
          
          {profiles.length < 5 && !manageMode && (
            <div 
              className="profile-card add-profile"
              onClick={() => setShowCreateModal(true)}
            >
              <div className="profile-avatar">
                <FiPlus />
              </div>
              <p className="profile-name">Add Profile</p>
            </div>
          )}
        </div>
        
        <button 
          className="btn btn-secondary manage-profiles-btn"
          onClick={() => setManageMode(!manageMode)}
        >
          <FiEdit2 /> {manageMode ? 'Done' : 'Manage Profiles'}
        </button>
      </div>
      
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => !creating && setShowCreateModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Create Profile</h2>
            <form onSubmit={handleCreateProfile}>
              <div className="form-group">
                <label htmlFor="profileName">Profile Name</label>
                <input
                  id="profileName"
                  type="text"
                  placeholder="Enter profile name"
                  value={newProfileName}
                  onChange={(e) => setNewProfileName(e.target.value)}
                  disabled={creating}
                  maxLength={30}
                  autoFocus
                />
              </div>
              
              <div className="modal-actions">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => setShowCreateModal(false)}
                  disabled={creating}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={creating || !newProfileName.trim()}
                >
                  {creating ? 'Creating...' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {deleteConfirm && (
        <div className="modal-overlay" onClick={() => setDeleteConfirm(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Delete Profile?</h2>
            <p>This will permanently delete this profile and all its data.</p>
            <div className="modal-actions">
              <button 
                className="btn btn-secondary"
                onClick={() => setDeleteConfirm(null)}
              >
                Cancel
              </button>
              <button 
                className="btn btn-danger"
                onClick={() => handleDeleteProfile(deleteConfirm)}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profiles;
