import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import './style.css';

function MusicSelector({ onSlideChange, songs, imgUrl }) {
  const swiperElRef = useRef();

  useEffect(() => {
    swiperElRef.current.addEventListener('realindexchange', onSlideChange);
  }, [swiperElRef, onSlideChange]);

  return (
    <swiper-container
      ref={swiperElRef}
      navigation="true"
      loop="true"
      speed="500"
      effect="coverflow"
      grab-cursor="true"
      centered-slides="true"
      slides-per-view="2"
      coverflow-effect-rotate="0"
      coverflow-effect-stretch="55"
      coverflow-effect-depth="100"
      coverflow-effect-modifier="1"
    >
      {songs.map((song) => (
        <swiper-slide key={song.song_id}>
          <div className="songCard">
            <img src={imgUrl} alt={`${song.song_title} 엘범 이미지`} />
            <div className="songDetail">
              <p className="songTitle">{song.song_title}</p>
              <p className="artistName">{song.artist_name}</p>
              <p className="albumTitle">{song.album_title}</p>
            </div>
          </div>
        </swiper-slide>
      ))}
    </swiper-container>
  );
}

MusicSelector.propTypes = {
  songs: PropTypes.arrayOf(
    PropTypes.shape({
      song_id: PropTypes.int,
      song_title: PropTypes.string,
      artist_name: PropTypes.string,
      album_title: PropTypes.string,
      music_url: PropTypes.string,
    })
  ).isRequired,
  onSlideChange: PropTypes.func.isRequired,
  imgUrl: PropTypes.string.isRequired,
};

export default MusicSelector;
