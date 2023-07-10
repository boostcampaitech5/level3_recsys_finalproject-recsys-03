import React, { PureComponent, createRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FiRotateCcw, FiSave } from 'react-icons/fi';
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
    videoYtId: '_sQhN4dLC60',
    musicTitle: '첫사랑2',
    artistName: '버스커 버스커',
    albumTitle: '버스커 버스커 1집',
  },
  {
    videoYtId: 'y5MAgMVwfFs',
    musicTitle: '좋다고 말해3',
    artistName: '볼빨간사춘기',
    albumTitle: 'Full Album RED PLANET',
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
              <FiRotateCcw />
              다시하기
            </button>
            <button
              className="save"
              type="button"
              onClick={() => {
                this.setModalOpen(true);
              }}
            >
              <FiSave />
              저장하기
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
