import React, { PureComponent, createRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FiRotateCcw, FiSave } from 'react-icons/fi';
import PropTypes from 'prop-types';
import MusicSelector from './MusicSelector';
import './MusicRecommend.css';
import YouTubeVideo from './YouTubeVideo';
import Modal from '../modal/Modal';
import defaultImg from '../../imgs/dummy512.jpg';

const Serveyurl =
  'https://docs.google.com/forms/d/e/1FAIpQLSf3iJv6ShZTjAbdVbo9DZVH1Z9YRluCKDW9EHlrYXj56ngGhA/viewform?entry.264447075=';

const defaultSongs = [
  {
    song_id: 1,
    youtube_id: 'XHMdIA6bEOE',
    song_title: '음악1',
    artist_name: '가수1',
    album_title: '앨범1',
  },
  {
    song_id: 2,
    youtube_id: 'Sq_mS6xWpvk',
    song_title: '음악2',
    artist_name: '가수가수가수가수가수가수가수가수2',
    album_title: '앨범2',
  },
  {
    song_id: 3,
    youtube_id: 'A1tZgPAcpjE',
    song_title: '음악3',
    artist_name: '가수3',
    album_title: '앨범앨범앨범앨범앨범앨범앨범앨범3',
  },
  {
    song_id: 4,
    youtube_id: 'NbKH4iZqq1Y',
    song_title: '음악4',
    artist_name: '가수4',
    album_title: '앨범4',
  },
  {
    song_id: 5,
    youtube_id: '2Kff0U8w-aU',
    song_title: '음악5',
    artist_name: '가수5',
    album_title: '앨범5',
  },
  {
    song_id: 6,
    youtube_id: 'j1uXcHwLhHM',
    song_title: '음악6',
    artist_name: '가수6',
    album_title: '앨범6',
  },
];
const defaultId = -1;

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
    const { imgUrl, songs, sessionId } = this.props;
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
          <button
            className="servey"
            onClick={() => {
              window.open(Serveyurl + { sessionId });
            }}
            type="button"
          >
            <span>간단한 설문조사하고 커피 받기! ☕️</span>
          </button>
        </div>
      </div>
    );
  }
}

MusicRecommend.defaultProps = {
  imgUrl: defaultImg,
  songs: defaultSongs,
  sessionId: defaultId,
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
  sessionId: PropTypes.string,
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
      sessionId={location.state?.sessionId}
    />
  );
}
