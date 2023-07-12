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
    const { songInfos, imgUrl } = this.props;

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
        {songInfos.map((songInfo) => (
          <swiper-slide key={songInfo.videoYtId}>
            <div className="songCard">
              <img src={imgUrl} alt={`${songInfo.musicTitle} 엘범 이미지`} />
              <div className="songDetail">
                <p className="songTitle">{songInfo.musicTitle}</p>
                <p className="artistName">{songInfo.artistName}</p>
                <p className="albumTitle">{songInfo.albumTitle}</p>
              </div>
            </div>
          </swiper-slide>
        ))}
      </swiper-container>
    );
  }
}

MusicSelector.propTypes = {
  songInfos: PropTypes.arrayOf(
    PropTypes.shape({
      videoYtId: PropTypes.string,
      musicTitle: PropTypes.string,
      artistName: PropTypes.string,
      albumTitle: PropTypes.string,
    })
  ).isRequired,
  onSlideChange: PropTypes.func.isRequired,
  imgUrl: PropTypes.string.isRequired,
};
