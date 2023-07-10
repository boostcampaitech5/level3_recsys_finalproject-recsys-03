import React, { PureComponent, createRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import MusicSelector from './MusicSelector';
import './MusicRecommend.css';
import YouTubeVideo from './YouTubeVideo';
import Modal from '../modal/Modal';
import defaultImg from '../../dummy512.jpg';

const songInfos = [
  {
    videoYtId: 'XHMdIA6bEOE',
    musicTitle: '짱구는 못말려 오프닝1',
    artistName: '아이브',
    albumTitle: '짱구 1기',
  },
  {
    videoYtId: 'Sq_mS6xWpvk',
    musicTitle: 'Kiss Goodnightrrrrrrrrrr',
    artistName: 'I Dont Know How But They Found Meeeee',
    albumTitle: 'Razzmatazz',
  },
  {
    videoYtId: 'A1tZgPAcpjE',
    musicTitle:
      '사랑하긴 했었나요 스쳐가는 인연이었나요 짧지않은 우리 함께했던 시간들이 자꾸 내 마음을 가둬두네',
    artistName: '잔나비 잔나비 잔미잔미 잔나비 잔나비 잔미잔미',
    albumTitle: '봉춤을 추네',
  },
  {
    videoYtId: 'NbKH4iZqq1Y',
    musicTitle: 'Drowning',
    artistName: 'WOODZ',
    albumTitle: 'OO-LI',
  },
  {
    videoYtId: '2Kff0U8w-aU',
    musicTitle: 'OMG',
    artistName: 'NewJeans',
    albumTitle: "NewJeans 'OMG'",
  },
  {
    videoYtId: 'j1uXcHwLhHM',
    musicTitle: '사건의 지평선',
    artistName: '윤하',
    albumTitle: 'END THEORY : Final Edition',
  },
];

class MusicRecommend extends PureComponent {
  constructor(props) {
    super(props);

    this.youTubeVideoRef = createRef();
    this.state = {
      modalOpen: false,
      songInfo: songInfos[0],
    };

    this.onSlideChange = (e) => {
      this.setState((state) => ({
        modalOpen: state.modalOpen,
        songInfo: songInfos[e.target.swiper.realIndex],
      }));

      this.youTubeVideoRef.current.changeVideoId(
        songInfos[e.target.swiper.realIndex].videoYtId
      );
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
    const { imgUrl } = this.props;
    const { modalOpen, songInfo } = this.state;
    return (
      <div className="MusicRecommend">
        <div className="contents">
          <div>
            {modalOpen && (
              <Modal
                imgUrl={imgUrl}
                artistName={songInfo.artistName}
                musicTitle={songInfo.musicTitle}
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
            imgUrl={imgUrl}
            onSlideChange={this.onSlideChange}
          />
          <h2>지금 노래를 들어보세요</h2>
          <YouTubeVideo
            ref={this.youTubeVideoRef}
            videoId={songInfos.videoYtId}
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

MusicRecommend.defaultProps = {
  imgUrl: defaultImg,
};

MusicRecommend.propTypes = {
  navigate: PropTypes.func.isRequired,
  imgUrl: PropTypes.string,
};

export default function MusicRecommendWrapper(props) {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <MusicRecommend
      // eslint-disable-next-line react/jsx-props-no-spreading
      {...props}
      navigate={navigate}
      imgUrl={location.state?.url}
    />
  );
}
