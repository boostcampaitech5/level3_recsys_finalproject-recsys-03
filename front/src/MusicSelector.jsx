import React, { createRef, PureComponent } from 'react';
import PropTypes from 'prop-types';

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
      >
        {songInfos.map((songInfo) => (
          <swiper-slide>
            <img
              src={process.env.PUBLIC_URL + songInfo.src}
              alt={`${songInfo.musicTitle} 엘범 이미지`}
              width="150"
            />
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
