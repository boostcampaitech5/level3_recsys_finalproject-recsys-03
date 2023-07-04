import React, { PureComponent, createRef } from 'react';
import MusicSelector from './MusicSelector';
import MusicDetail from './MusicDetail';

const songInfos = [
  {
    videoYtId: 'XHMdIA6bEOE',
    src: '/dummy-1.jpg',
    musicTitle: '짱구는 못말려 오프닝',
    artistName: '아이브',
  },
  {
    videoYtId: '_sQhN4dLC60',
    src: '/dummy-2.jpg',
    musicTitle: '첫사랑',
    artistName: '버스커 버스커',
  },
  {
    videoYtId: 'y5MAgMVwfFs',
    src: '/dummy-3.jpg',
    musicTitle: '좋다고 말해',
    artistName: '볼빨간사춘기',
  },
];

export default class MusicRecommend extends PureComponent {
  constructor(props) {
    super(props);

    this.musicDetailRef = createRef();

    this.onSlideChange = (e) => {
      const songInfo = songInfos[e.target.swiper.realIndex];
      this.musicDetailRef.current.updateSongInfo(songInfo);
    };
  }

  render() {
    return (
      <div className="MusicRec">
        <MusicSelector
          songInfos={songInfos}
          onSlideChange={this.onSlideChange}
        />
        <MusicDetail ref={this.musicDetailRef} songInfo={songInfos[0]} />
        <button type="button">결과 공유하기</button>
      </div>
    );
  }
}
