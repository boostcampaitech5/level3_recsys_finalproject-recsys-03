import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FiRotateCcw, FiHeart } from 'react-icons/fi';
import { TbCards } from 'react-icons/tb';
import Marquee from 'react-fast-marquee';
import AudioPlayer, { RHAP_UI } from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';
import MusicSelector from './MusicSelector';
import './style.css';
import Modal from './Modal';
import defaultImg from '../../imgs/dummy512.jpg';
import requestUserFeedback from './requestUserFeedback';

const defaultSongs = [
  {
    song_id: 1,
    song_title: '음악1',
    artist_name: '가수1',
    album_title: '앨범1',
    music_url:
      'https://p.scdn.co/mp3-preview/6801b88192f9a6dc4ee0c256dfbf72671dc83c7a?cid=0037db4c059245e2a697e420eaf107e0',
  },
  {
    song_id: 2,
    song_title: '음악2음악2음악2음악2음악2음악2음악2음악2음악2',
    artist_name:
      '가수가수가수가수가수가수가수가수가수가수가수가수가수가수가수2',
    album_title: '앨범2',
    music_url:
      'https://p.scdn.co/mp3-preview/bd50f6e6d92ed09aaf38b759ddd96c7164931aa1?cid=0037db4c059245e2a697e420eaf107e0',
  },
  {
    song_id: 3,
    song_title:
      '사랑하긴 했었나요 스쳐가는 인연이었나요 짧지 않은 우리 함께했던 시간들이 자꾸 내 마음을 가둬두네',
    artist_name: '잔미',
    album_title: '앨범앨범앨범앨범앨범앨범앨범앨범3',
    music_url:
      'https://p.scdn.co/mp3-preview/5274582d3f3f34e82fb83e814dcad59182c92ae4?cid=0037db4c059245e2a697e420eaf107e0',
  },
  {
    song_id: 4,
    song_title: '음악4',
    artist_name:
      '사랑하긴 했었나요 스쳐가는 인연이었나요 짧지 않은 우리 함께했던 시간들이 자꾸 내 마음을 가둬두네',
    album_title: '앨범4',
    music_url:
      'https://p.scdn.co/mp3-preview/a54a328016674ea6da346af84c6c06c6536195c8?cid=0037db4c059245e2a697e420eaf107e0',
  },
  {
    song_id: 5,
    song_title: '음악5',
    artist_name: '가수5',
    album_title: '앨범5',
    music_url:
      'https://p.scdn.co/mp3-preview/1aaf30001acf34f7c6c0d9aee23c354d05923fc4?cid=0037db4c059245e2a697e420eaf107e0',
  },
  {
    song_id: 6,
    song_title: '음악6',
    artist_name: '가수6',
    album_title: '앨범6',
    music_url:
      'https://p.scdn.co/mp3-preview/1eff5d6411ae2c65990552133729f3e907c4a793?cid=0037db4c059245e2a697e420eaf107e0',
  },
];
const defaultId = 'NULL';

function RecommendMusicPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const imgUrl = location.state?.url ?? defaultImg;
  const songs = location.state?.songs ?? defaultSongs;
  const sessionId = location.state?.sessionId ?? defaultId;

  const [modalOpen, setModalOpen] = useState(false);
  const [song, setSong] = useState(songs[0]);
  const [isLike, setIsLike] = useState(false);
  const [toggleLazyPause, setToggleLazyPause] = useState(false);
  const isShortSongTitle = song.song_title.length < 23;
  const isShortArtistName = song.artist_name.length < 29;

  const playerRef = useRef();

  const onSlideChange = useCallback(
    (e) => {
      const index = e.target.swiper.realIndex;

      setSong(songs[index]);
      setIsLike(false);
      setToggleLazyPause(true);
    },
    [songs, setSong, setIsLike, setToggleLazyPause]
  );

  const goMainPage = useCallback(() => {
    navigate('/');
  }, [navigate]);

  useEffect(() => {
    if (toggleLazyPause) {
      playerRef.current.audio.current.pause();
      setToggleLazyPause(false);
    }
  }, [toggleLazyPause]);

  return (
    <div className="MusicRecommend">
      <div className="contents">
        <div>
          {modalOpen && (
            <Modal
              imgUrl={imgUrl}
              artistName={song.artist_name}
              musicTitle={song.song_title}
              setOpenModal={setModalOpen}
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
          onSlideChange={onSlideChange}
        />
        <h2>지금 노래를 들어보세요</h2>
        {isShortSongTitle && isShortArtistName && (
          <div className="infoBox">
            <div className="songName">{song.song_title}</div>
            <div className="artistName">{song.artist_name}</div>
          </div>
        )}
        {isShortSongTitle && !isShortArtistName && (
          <div className="infoBox">
            <div className="songName">{song.song_title}</div>
            <Marquee pauseOnHover speed={40}>
              <div className="artistName">{song.artist_name}</div>
            </Marquee>
          </div>
        )}
        {!isShortSongTitle && isShortArtistName && (
          <div className="infoBox">
            <Marquee pauseOnHover speed={40}>
              <div className="songName">{song.song_title}</div>
            </Marquee>
            <div className="artistName">{song.artist_name}</div>
          </div>
        )}
        {!isShortSongTitle && !isShortArtistName && (
          <Marquee pauseOnHover speed={40}>
            <div className="infoBox">
              <div className="songName">{song.song_title}</div>
              <div className="artistName">{song.artist_name}</div>
            </div>
          </Marquee>
        )}

        <div className="playerBox">
          <AudioPlayer
            customAdditionalControls={[
              RHAP_UI.LOOP,
              <button
                className="feedbackbtn"
                onClick={() => {
                  setIsLike(!isLike);
                  requestUserFeedback(sessionId, song.song_id, !isLike);
                }}
                type="button"
              >
                <FiHeart fill={isLike ? '#f44404' : 'black'} color="#f44404" />
              </button>,
            ]}
            className="audio"
            autoPlay={false}
            src={song.music_url}
            volume={0.3}
            timeFormat="mm:ss"
            defaultCurrentTime="00:00"
            showJumpControls={false}
            ref={playerRef}
          />
        </div>
      </div>
      <div className="footer">
        <div className="buttons">
          <button className="retry" type="button" onClick={goMainPage}>
            <FiRotateCcw />
            다시하기
          </button>
          <button
            className="save"
            type="button"
            onClick={() => {
              setModalOpen(true);
            }}
          >
            <TbCards />
            포토카드 받기
          </button>
        </div>
      </div>
    </div>
  );
}

export default RecommendMusicPage;
