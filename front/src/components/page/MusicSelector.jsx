import React, { createRef, PureComponent } from 'react';
import PropTypes from 'prop-types';
import './MusicSelector.css';

export default class MusicSelector extends PureComponent {
  constructor(props) {
    super(props);

    this.swiperElRef = createRef();
    this.onSlideChange = props.onSlideChange;
  }

  componentDidMount() {
    this.swiperElRef.current.addEventListener(
      'realindexchange',
      this.onSlideChange
    );
  }

  componentWillUnmount() {
    this.swiperElRef.current.removeEventListener(
      'realindexchange',
      this.onSlideChange
    );
  }

  render() {
    const { songs, imgUrl } = this.props;

    return (
      <swiper-container
        ref={this.swiperElRef}
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
