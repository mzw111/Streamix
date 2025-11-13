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
      setError('');
      const response = await profileAPI.list();
      console.log('Profiles response:', response.data);
      
      if (response.data && response.data.profiles) {
        setProfiles(response.data.profiles);
      }
    } catch (err) {
      console.error('Fetch profiles error:', err);
      setError('Failed to load profiles');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectProfile = (profile) => {
    if (!profile || !profile.profile_id) {
      console.error('Invalid profile selected');
      return;
    }
    
    localStorage.setItem('selectedProfile', JSON.stringify(profile));
    localStorage.setItem('profileId', profile.profile_id);
    navigate('/');
  };

  const handleCreateProfile = async (e) => {
    e.preventDefault();
    
    const trimmedName = newProfileName.trim();
    
    if (!trimmedName) {
      setError('Profile name cannot be empty');
      return;
    }
    
    setCreating(true);
    setError('');
    
    try {
      console.log('Creating profile with name:', trimmedName);
      
      const response = await profileAPI.create({ name: trimmedName });
      console.log('Create response:', response);
      
      if (response.data && response.data.success) {
        console.log('Profile created:', response.data.profile);
        
        // Close modal first
        setShowCreateModal(false);
        setNewProfileName('');
        
        // Then refresh profiles list
        await fetchProfiles();
        
        // Clear any errors
        setError('');
      } else {
        throw new Error(response.data?.message || 'Failed to create profile');
      }
      
    } catch (err) {
      console.error('Create profile error:', err);
      
      const errorMessage = err.response?.data?.message 
        || err.message 
        || 'Failed to create profile. Please try again.';
      
      setError(errorMessage);
      
      // Close modal and show error on main page if it's a limit error
      if (errorMessage.includes('Maximum') || errorMessage.includes('limit') || errorMessage.includes('3')) {
        setShowCreateModal(false);
      }
      
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteProfile = async (profileId) => {
    try {
      setError('');
      await profileAPI.delete(profileId);
      
      // Refresh profiles after deletion
      await fetchProfiles();
      setDeleteConfirm(null);
      
    } catch (err) {
      console.error('Delete error:', err);
      setError(err.response?.data?.message || 'Failed to delete profile');
    }
  };

  const openCreateModal = () => {
    // Check if already at limit
    if (profiles.length >= 3) {
      setError('Maximum profile limit (3) reached. Please delete a profile to create a new one.');
      return;
    }
    
    // Otherwise open modal
    setError('');
    setNewProfileName('');
    setShowCreateModal(true);
  };

  const closeCreateModal = () => {
    if (!creating) {
      setShowCreateModal(false);
      setNewProfileName('');
      setError('');
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
          {profiles && profiles.length > 0 ? (
            profiles.map((profile) => {
              if (!profile || !profile.profile_id) return null;
              
              return (
                <div 
                  key={profile.profile_id}
                  className={`profile-card ${manageMode ? 'manage-mode' : ''}`}
                  onClick={() => !manageMode && handleSelectProfile(profile)}
                >
                  <div className="profile-avatar">
                    <FiUser />
                  </div>
                  <p className="profile-name">
                    {profile.profile_name || profile.name || 'Profile'}
                  </p>
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
              );
            })
          ) : (
            <div style={{ color: 'white', gridColumn: '1 / -1', textAlign: 'center', padding: '20px' }}>
              <p>No profiles found. Create your first profile to get started!</p>
            </div>
          )}
          
          {/* ALWAYS show Add Profile button, regardless of count */}
          {!manageMode && (
            <div 
              className="profile-card add-profile"
              onClick={openCreateModal}
            >
              <div className="profile-avatar">
                <FiPlus />
              </div>
              <p className="profile-name">Add Profile</p>
            </div>
          )}
        </div>
        
        {profiles.length > 0 && (
          <button 
            className="btn btn-secondary manage-profiles-btn"
            onClick={() => {
              setManageMode(!manageMode);
              setError('');
            }}
          >
            <FiEdit2 /> {manageMode ? 'Done' : 'Manage Profiles'}
          </button>
        )}
      </div>
      
      {showCreateModal && (
        <div className="modal-overlay" onClick={closeCreateModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Create Profile</h2>
            {error && <p className="error-text" style={{marginBottom: '10px'}}>{error}</p>}
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
                  required
                />
              </div>
              
              <div className="modal-actions">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={closeCreateModal}
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
