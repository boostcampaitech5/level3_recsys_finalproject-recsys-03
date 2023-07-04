import React, { PureComponent } from 'react';
import YouTubeVideo from './YouTubeVideo';

export default class MusicRecommend extends PureComponent {
  render() {
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

    return (
      <div className="MusicRec">
        <swiper-container pagination="true" navigation="true">
          {songInfos.map((songInfo) => (
            <swiper-slide>
              <img
                src={process.env.PUBLIC_URL + songInfo.src}
                alt={`${songInfo.musicTitle} 엘범 이미지`}
                width="150"
              />
              <h1>Music Title: {songInfo.musicTitle}</h1>
              <h1>Artist Name: {songInfo.artistName}</h1>
              <YouTubeVideo videoId={songInfo.videoYtId} />
            </swiper-slide>
          ))}
        </swiper-container>
        <button type="button">결과 공유하기</button>
      </div>
    );
  }
}
