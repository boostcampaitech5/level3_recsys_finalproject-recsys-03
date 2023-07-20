import React, { PureComponent, createRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FiRotateCcw, FiSave } from 'react-icons/fi';
import PropTypes from 'prop-types';
import MusicSelector from './MusicSelector';
import './MusicRecommend.css';
import YouTubeVideo from './YouTubeVideo';
import Modal from '../modal/Modal';
import defaultImg from '../../imgs/dummy512.jpg';

const defaultSongs = [
  {
    song_id: 1,
    youtube_id: 'XHMdIA6bEOE',
    song_title: '음악1',
    artist_name: '아이브',
    album_title: '짱구 1기',
  },
  {
    song_id: 2,
    youtube_id: 'Sq_mS6xWpvk',
    song_title: '음악2',
    artist_name: 'I Dont Know How But They Found Meeeee',
    album_title: 'Razzmatazz',
  },
  {
    song_id: 3,
    youtube_id: 'A1tZgPAcpjE',
    song_title: '음악3',
    artist_name: '잔나비 잔나비 잔미잔미 잔나비 잔나비 잔미잔미',
    album_title: '봉춤을 추네',
  },
  {
    song_id: 4,
    youtube_id: 'NbKH4iZqq1Y',
    song_title: '음악4',
    artist_name: 'WOODZ',
    album_title: 'OO-LI',
  },
  {
    song_id: 5,
    youtube_id: '2Kff0U8w-aU',
    song_title: '음악5',
    artist_name: 'NewJeans',
    album_title: "NewJeans 'OMG'",
  },
  {
    song_id: 6,
    youtube_id: 'j1uXcHwLhHM',
    song_title: '음악6',
    artist_name: '윤하',
    album_title: 'END THEORY : Final Edition',
  },
];

class MusicRecommend extends PureComponent {
  constructor(props) {
    super(props);

    const { songs } = this.props;

    this.youTubeVideoRef = createRef();
    this.state = {
      modalOpen: false,
      song: songs[0],
    };

    this.onSlideChange = (e) => {
      this.setState((state) => ({
        modalOpen: state.modalOpen,
        song: songs[e.target.swiper.realIndex],
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
    const { imgUrl, songs } = this.props;
    const { modalOpen, song } = this.state;
    return (
      <div className="MusicRecommend">
        <div className="contents">
          <div>
            {modalOpen && (
              <Modal
                imgUrl={imgUrl}
                artistName={song.artist_name}
                musicTitle={song.song_title}
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
            songs={songs}
            imgUrl={imgUrl}
            onSlideChange={this.onSlideChange}
          />
          <h2>지금 노래를 들어보세요</h2>
          <YouTubeVideo ref={this.youTubeVideoRef} videoId={song.youtube_id} />
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
  songs: defaultSongs,
};

MusicRecommend.propTypes = {
  navigate: PropTypes.func.isRequired,
  imgUrl: PropTypes.string,
  songs: PropTypes.arrayOf(
    PropTypes.shape({
      song_id: PropTypes.int,
      song_title: PropTypes.string,
      artist_name: PropTypes.string,
      album_title: PropTypes.string,
      youtube_id: PropTypes.string,
    })
  ),
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
      songs={location.state?.songs}
    />
  );
}
