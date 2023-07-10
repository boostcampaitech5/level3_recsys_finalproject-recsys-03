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
            videoId={songInfo.videoYtId}
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
