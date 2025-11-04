import React, { useState, useEffect } from 'react';
import HeroSection from '../components/HeroSection';
import ScrollableRow from '../components/ScrollableRow';
import { homeAPI, moviesAPI, tvShowsAPI } from '../services/api';
import './Home.css';

const Home = () => {
  const [featuredContent, setFeaturedContent] = useState(null);
  const [homeContent, setHomeContent] = useState([]);
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [trendingShows, setTrendingShows] = useState([]);
  const [newReleases, setNewReleases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [profileId, setProfileId] = useState(null);

  useEffect(() => {
    // Get profile ID from localStorage
    const storedProfileId = localStorage.getItem('profileId');
    setProfileId(storedProfileId);
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    try {
      setLoading(true);

      // Fetch home page content
      const homeResponse = await homeAPI.getContent();
      const homeData = homeResponse.data.content || [];
      setHomeContent(homeData);

      // Set featured content (first item from home page)
      if (homeData.length > 0) {
        setFeaturedContent(homeData[0]);
      }

      // Fetch movies and TV shows
      const [moviesResponse, showsResponse] = await Promise.all([
        moviesAPI.getAll(),
        tvShowsAPI.getAll(),
      ]);

      const movies = moviesResponse.data.data || [];
      const shows = showsResponse.data.data || [];

      // Sort by rating for trending
      const sortedMovies = [...movies].sort((a, b) => 
        (b.average_rating || 0) - (a.average_rating || 0)
      );
      const sortedShows = [...shows].sort((a, b) => 
        (b.average_rating || 0) - (a.average_rating || 0)
      );

      setTrendingMovies(sortedMovies.slice(0, 10));
      setTrendingShows(sortedShows.slice(0, 10));

      // Sort by release date for new releases
      const allContent = [...movies, ...shows].sort((a, b) => {
        const dateA = new Date(a.Release_Date || a.Release_Year || 0);
        const dateB = new Date(b.Release_Date || b.Release_Year || 0);
        return dateB - dateA;
      });
      setNewReleases(allContent.slice(0, 10));

    } catch (error) {
      console.error('Error fetching home data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading amazing content...</p>
      </div>
    );
  }

  return (
    <div className="home-page">
      <HeroSection content={featuredContent} />

      <div className="home-content">
        {trendingMovies.length > 0 && (
          <ScrollableRow
            title="Trending Now"
            items={trendingMovies}
            type="Movie"
            profileId={profileId}
          />
        )}

        {newReleases.length > 0 && (
          <ScrollableRow
            title="New Releases"
            items={newReleases}
            type="Movie"
            profileId={profileId}
          />
        )}

        {trendingShows.length > 0 && (
          <ScrollableRow
            title="Popular TV Shows"
            items={trendingShows}
            type="TV_Show"
            profileId={profileId}
          />
        )}

        {homeContent.length > 0 && (
          <ScrollableRow
            title="Featured Content"
            items={homeContent}
            type="Movie"
            profileId={profileId}
          />
        )}
      </div>
    </div>
  );
};

export default Home;
