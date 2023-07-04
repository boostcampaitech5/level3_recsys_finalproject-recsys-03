import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import YouTubeVideo from './YouTubeVideo';

export default class MusicDetail extends PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      songInfo: props.songInfo,
    };
  }

  // eslint-disable-next-line react/no-unused-class-component-methods
  updateSongInfo(songInfo) {
    this.setState(() => ({
      songInfo,
    }));
  }

  render() {
    const { songInfo } = this.state;

    return (
      <div>
        <h1>Music Title: {songInfo.musicTitle}</h1>
        <h1>Artist Name: {songInfo.artistName}</h1>
        <YouTubeVideo videoId={songInfo.videoYtId} />
      </div>
    );
  }
}

MusicDetail.propTypes = {
  songInfo: PropTypes.shape({
    videoYtId: PropTypes.string,
    src: PropTypes.string,
    musicTitle: PropTypes.string,
    artistName: PropTypes.string,
  }).isRequired,
};
