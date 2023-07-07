import React, { PureComponent } from 'react';
import MusicSelector from './MusicSelector';
import './MusicRecommend.css';

const songInfos = [
  {
    videoYtId: 'XHMdIA6bEOE',
    src: '/dummy-1.jpg',
    musicTitle: '짱구는 못말려 오프닝',
    artistName: '아이브',
  },
  {
    videoYtId: '_sQhN4dLC60',
    src: '/dummy-1.jpg',
    musicTitle: '첫사랑',
    artistName: '버스커 버스커',
  },
  {
    videoYtId: 'y5MAgMVwfFs',
    src: '/dummy-1.jpg',
    musicTitle: '좋다고 말해',
    artistName: '볼빨간사춘기',
  },
  {
    videoYtId: 'XHMdIA6bEOE',
    src: '/dummy-1.jpg',
    musicTitle: '짱구는 못말려 오프닝',
    artistName: '아이브',
  },
  {
    videoYtId: '_sQhN4dLC60',
    src: '/dummy-1.jpg',
    musicTitle: '첫사랑',
    artistName: '버스커 버스커',
  },
  {
    videoYtId: 'y5MAgMVwfFs',
    src: '/dummy-1.jpg',
    musicTitle: '좋다고 말해',
    artistName: '볼빨간사춘기',
  },
];

export default class MusicRecommend extends PureComponent {
  constructor(props) {
    super(props);

    this.onSlideChange = (e) => {
      // eslint-disable-next-line no-unused-vars
      const songInfo = songInfos[e.target.swiper.realIndex];
    };
  }

  render() {
    return (
      <div className="MusicRecommend">
        <div className="header">
          <h1>일상의 노래를 찾았어요!</h1>
          <h3>당신의 일상과 취향을 모두 반영했어요</h3>
        </div>

        <MusicSelector
          songInfos={songInfos}
          onSlideChange={this.onSlideChange}
        />
        <button type="button">결과 공유하기</button>
      </div>
    );
  }
}
