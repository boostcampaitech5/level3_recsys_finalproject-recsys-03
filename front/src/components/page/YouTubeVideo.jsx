import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import YouTube from 'react-youtube';
import './YouTubeVideo.css';

export default class YouTubeVideo extends PureComponent {
  render() {
    const { videoId } = this.props;
    return (
      <div className="YouTubeVideo">
        <YouTube
          key={videoId}
          videoId={videoId}
          opts={{
            width: '320px',
            height: '180px',
            playerVars: {
              rel: 0,
              modestbranding: 1,
            },
            host: 'https://www.youtube-nocookie.com',
          }}
        />
      </div>
    );
  }
}

YouTubeVideo.propTypes = {
  videoId: PropTypes.string.isRequired,
};
