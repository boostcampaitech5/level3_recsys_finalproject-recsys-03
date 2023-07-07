import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import YouTube from 'react-youtube';
import './YouTubeVideo.css';

export default class YouTubeVideo extends PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      videoId: props.videoId,
    };
  }

  // eslint-disable-next-line react/no-unused-class-component-methods
  changeVideoId(videoId) {
    this.setState({
      videoId,
    });
  }

  render() {
    const { videoId } = this.state;
    return (
      <div className="YouTubeVideo">
        <YouTube
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
