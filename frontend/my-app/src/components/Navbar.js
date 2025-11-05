import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FiSearch, FiBell, FiUser } from 'react-icons/fi';
import './Navbar.css';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${searchQuery}`);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <Link to="/" className="navbar-logo">
            <span className="logo-icon">▶</span>
            <span className="logo-text">Streamify</span>
          </Link>

          <div className="navbar-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/movies" className="nav-link">Movies</Link>
            <Link to="/tv-shows" className="nav-link">TV Shows</Link>
            <Link to="/my-list" className="nav-link">My List</Link>
            <Link to="/history" className="nav-link">History</Link>
            <Link to="/subscription" className="nav-link">Subscription</Link>
          </div>
        </div>

        <div className="navbar-right">
          <form onSubmit={handleSearch} className="search-container">
            <FiSearch className="search-icon" />
            <input
              type="text"
              placeholder="Search..."
              className="search-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>

          {isAuthenticated ? (
            <>
              <button className="icon-btn">
                <FiBell />
              </button>
              
              <div className="profile-menu">
                <button
                  className="profile-btn"
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                >
                  <FiUser />
                </button>
                
                {showProfileMenu && (
                  <div className="profile-dropdown">
                    <div className="dropdown-item user-info">
                      <span>{user?.name}</span>
                      <span className="user-email">{user?.email}</span>
                    </div>
                    <div className="dropdown-divider"></div>
                    <Link to="/profiles" className="dropdown-item">
                      Manage Profiles
                    </Link>
                    <Link to="/history" className="dropdown-item">
                      Viewing History
                    </Link>
                    <Link to="/account" className="dropdown-item">
                      Account Settings
                    </Link>
                    <Link to="/subscription" className="dropdown-item">
                      Subscription
                    </Link>
                    <div className="dropdown-divider"></div>
                    <button onClick={handleLogout} className="dropdown-item logout-btn">
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <Link to="/login" className="btn btn-primary">
              Sign In
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
