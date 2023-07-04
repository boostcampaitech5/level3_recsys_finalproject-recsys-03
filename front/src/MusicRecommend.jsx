import React, { PureComponent } from 'react';
import YouTubeVideo from './YouTubeVideo';

export default class MusicRecommend extends PureComponent {
  render() {
    const videoId = 'rcEyUNeZqmY';
    return (
      <div className="MusicRec">
        <YouTubeVideo videoId={videoId} />
      </div>
    );
  }
}
