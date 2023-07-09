import React, { PureComponent, createRef } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import MusicSelector from './MusicSelector';
import './MusicRecommend.css';
import YouTubeVideo from './YouTubeVideo';
import Modal from '../modal/Modal';

const songInfos = [
  {
    videoYtId: 'XHMdIA6bEOE',
    src: '/dummy-1.jpg',
    musicTitle: '짱구는 못말려 오프닝1',
    artistName: '아이브',
  },
  {
    videoYtId: '_sQhN4dLC60',
    src: '/dummy-1.jpg',
    musicTitle: '첫사랑2',
    artistName: '버스커 버스커',
  },
  {
    videoYtId: 'y5MAgMVwfFs',
    src: '/dummy-1.jpg',
    musicTitle: '좋다고 말해3',
    artistName: '볼빨간사춘기',
  },
  {
    videoYtId: 'XHMdIA6bEOE',
    src: '/dummy-1.jpg',
    musicTitle: '짱구는 못말려 오프닝4',
    artistName: '아이브',
  },
  {
    videoYtId: '_sQhN4dLC60',
    src: '/dummy-1.jpg',
    musicTitle: '첫사랑5',
    artistName: '버스커 버스커',
  },
  {
    videoYtId: 'y5MAgMVwfFs',
    src: '/dummy-1.jpg',
    musicTitle: '좋다고 말해6',
    artistName: '볼빨간사춘기',
  },
];

class MusicRecommend extends PureComponent {
  constructor(props) {
    super(props);

    this.youTubeVideoRef = createRef();
    this.state = {
      modalOpen: false,
    };

    this.onSlideChange = (e) => {
      const songInfo = songInfos[e.target.swiper.realIndex];
      this.youTubeVideoRef.current.changeVideoId(songInfo.videoYtId);
    };
  }

  setModalOpen(modalOpen) {
    this.setState({
      modalOpen,
    });
  }

  goMainPage() {
    const { navigate } = this.props;
    navigate('/');
  }

  render() {
    const { modalOpen } = this.state;
    return (
      <div className="MusicRecommend">
        <div className="contents">
          <div>
            {modalOpen && (
              <Modal
                setOpenModal={() => {
                  this.setModalOpen();
                }}
              />
            )}
          </div>
          <div className="header">
            <h1>일상의 노래를 찾았어요!</h1>
            <h3>당신의 일상과 취향을 모두 반영했어요</h3>
          </div>

          <MusicSelector
            songInfos={songInfos}
            onSlideChange={this.onSlideChange}
          />
          <h2>지금 노래를 들어보세요</h2>
          <YouTubeVideo
            ref={this.youTubeVideoRef}
            videoId={songInfos[0].videoYtId}
          />
        </div>
        <div className="footer">
          <div className="buttons">
            <button
              className="retry"
              type="button"
              onClick={() => this.goMainPage()}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="35"
                viewBox="0 -960 960 960"
                width="35"
              >
                <path d="M480-160q-133 0-226.5-93.5T160-480q0-133 93.5-226.5T480-800q85 0 149 34.5T740-671v-129h60v254H546v-60h168q-38-60-97-97t-137-37q-109 0-184.5 75.5T220-480q0 109 75.5 184.5T480-220q83 0 152-47.5T728-393h62q-29 105-115 169t-195 64Z" />
              </svg>
              다시하기
            </button>
            <button
              className="share"
              type="button"
              onClick={() => {
                this.setModalOpen(true);
              }}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="35"
                viewBox="0 -960 960 960"
                width="35"
              >
                <path d="M220-40q-24 0-42-18t-18-42v-509q0-24 18-42t42-18h169v60H220v509h520v-509H569v-60h171q24 0 42 18t18 42v509q0 24-18 42t-42 18H220Zm229-307v-457l-88 88-43-43 161-161 161 161-43 43-88-88v457h-60Z" />
              </svg>
              공유하기
            </button>
          </div>
        </div>
      </div>
    );
  }
}

MusicRecommend.propTypes = {
  navigate: PropTypes.func.isRequired,
};

export default function MusicRecommendWrapper(props) {
  const navigate = useNavigate();

  // eslint-disable-next-line react/jsx-props-no-spreading
  return <MusicRecommend {...props} navigate={navigate} />;
}
