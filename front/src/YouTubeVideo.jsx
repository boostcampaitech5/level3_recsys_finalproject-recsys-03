import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import YouTube from 'react-youtube';

function onReady(event) {
  // access to player in all event handlers via event.target
  event.target.pauseVideo();
}

export default class YouTubeVideo extends PureComponent {
  render() {
    const { videoId } = this.props;
    return (
      <YouTube
        videoId={videoId}
        opts={{
          width: '560',
          height: '315',
          playerVars: {
            rel: 0, // 관련 동영상 표시하지 않음
            modestbranding: 1, // 컨트롤 바에 youtube 로고를 표시하지 않음
          },
          host: 'https://www.youtube-nocookie.com',
        }}
        onReady={onReady}
      />
    );
  }
}

YouTubeVideo.propTypes = {
  videoId: PropTypes.string.isRequired,
};
