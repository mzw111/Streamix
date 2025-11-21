import React, { useRef, useEffect } from 'react';
import { FiPlay, FiPause, FiVolume2, FiMaximize } from 'react-icons/fi';
import './VideoPlayer.css';

const VideoPlayer = ({ videoUrl, onTimeUpdate, onEnded }) => {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = React.useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => {
      if (onTimeUpdate) {
        onTimeUpdate(Math.floor(video.currentTime)); // Pass seconds
      }
    };

    const handleEnded = () => {
      setIsPlaying(false);
      if (onEnded) {
        onEnded();
      }
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('ended', handleEnded);

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('ended', handleEnded);
    };
  }, [onTimeUpdate, onEnded]);

  const togglePlay = () => {
    const video = videoRef.current;
    if (video.paused) {
      video.play();
      setIsPlaying(true);
    } else {
      video.pause();
      setIsPlaying(false);
    }
  };

  const toggleFullscreen = () => {
    const video = videoRef.current;
    if (video.requestFullscreen) {
      video.requestFullscreen();
    }
  };

  return (
    <div className="video-player-container">
      <video
        ref={videoRef}
        className="video-player"
        src={videoUrl}
        controls
        controlsList="nodownload"
      >
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoPlayer;
