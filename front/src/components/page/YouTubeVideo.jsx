import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import YouTube from 'react-youtube';

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
            // autoplay: 1,
          },
          host: 'https://www.youtube-nocookie.com',
        }}
      />
    );
  }
}

YouTubeVideo.propTypes = {
  videoId: PropTypes.string.isRequired,
};
