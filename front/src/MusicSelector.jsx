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
      'slidechange',
      this.onSlideChange
    );
  }

  componentWillUnmount() {
    this.swiperElRef.current.removeEventListener(
      'slidechange',
      this.onSlideChange
    );
  }

  render() {
    const { songInfos } = this.props;

    return (
      <swiper-container
        ref={this.swiperElRef}
        pagination="true"
        navigation="true"
        loop="true"
        speed="500"
        effect="coverflow"
        grab-cursor="true"
        centered-slides="true"
        slides-per-view="2"
        coverflow-effect-rotate="0"
        coverflow-effect-stretch="0"
        coverflow-effect-depth="700"
        coverflow-effect-modifier="1"
        // coverflow-effect-slide-shadows="false"
      >
        {songInfos.map((songInfo) => (
          <swiper-slide>
            <div className="songCard">
              <img
                src={process.env.PUBLIC_URL + songInfo.src}
                alt={`${songInfo.musicTitle} 엘범 이미지`}
              />
              <h className="songTitle">{songInfo.musicTitle}</h>
              <p className="artistName">{songInfo.artistName}</p>
            </div>
          </swiper-slide>
        ))}
      </swiper-container>
    );
  }
}

MusicSelector.propTypes = {
  songInfos: PropTypes.shape([
    {
      videoYtId: PropTypes.string,
      src: PropTypes.string,
      musicTitle: PropTypes.string,
      artistName: PropTypes.string,
    },
  ]).isRequired,
  onSlideChange: PropTypes.func.isRequired,
};
