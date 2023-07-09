import React, { Component } from 'react';
import PropTypes from 'prop-types';
import defaultImg from '../../dummy512.jpg';
import backgroundMusicCardImg from '../../background-music-card.png';

const drawBackgroundMusicCard = (canvas, ctx, onLoadFinished) => {
  const backgroundImgTag = new Image();
  backgroundImgTag.src = backgroundMusicCardImg;

  backgroundImgTag.width = canvas.width;
  backgroundImgTag.height =
    backgroundImgTag.width + backgroundImgTag.width * 0.68;

  backgroundImgTag.onload = () => {
    // background
    ctx.drawImage(
      backgroundImgTag,
      0,
      0,
      backgroundImgTag.width,
      backgroundImgTag.height
    );

    onLoadFinished(backgroundImgTag);
  };
};

const drawQueryImage = (canvas, ctx, url, backgroundImgTag) => {
  const queryImgTag = new Image();
  queryImgTag.src = url;

  queryImgTag.onload = () => {
    const cornerRadius = 15; // radi
    const x = backgroundImgTag.width - backgroundImgTag.width * 0.939;
    const y = backgroundImgTag.height - backgroundImgTag.height * 0.932;
    const queryWidth = backgroundImgTag.width - backgroundImgTag.width * 0.118;
    const queryHeight = backgroundImgTag.width - backgroundImgTag.width * 0.118;

    ctx.beginPath();
    ctx.moveTo(x + cornerRadius, y);
    ctx.lineTo(x + queryWidth - cornerRadius, y);
    ctx.arcTo(
      x + queryWidth,
      y,
      x + queryWidth,
      y + cornerRadius,
      cornerRadius
    );
    ctx.lineTo(x + queryWidth, y + queryHeight - cornerRadius);
    ctx.arcTo(
      x + queryWidth,
      y + queryHeight,
      x + queryWidth - cornerRadius,
      y + queryHeight,
      cornerRadius
    );
    ctx.lineTo(x + cornerRadius, y + queryHeight);
    ctx.arcTo(
      x,
      y + queryHeight,
      x,
      y + queryHeight - cornerRadius,
      cornerRadius
    );
    ctx.lineTo(x, y + cornerRadius);
    ctx.arcTo(x, y, x + cornerRadius, y, cornerRadius);
    ctx.closePath();

    ctx.clip();

    ctx.drawImage(queryImgTag, x, y, queryWidth, queryHeight);
  };
};

class CardGenerator extends Component {
  constructor(props) {
    super(props);
    this.canvasRef = React.createRef();
  }

  componentDidMount() {
    const { imgUrl, artistName, musicTitle } = this.props;

    const canvas = this.canvasRef.current;
    // origin: 525
    canvas.width = 525;
    // origin: 884
    canvas.height = 884;

    // get date
    // const today = new Date();
    // const year = today.getFullYear();
    // const month = String(today.getMonth() + 1).padStart(2, '0');
    // const day = String(today.getDate()).padStart(2, '0');
    // const dateString = `${year}.${month}.${day}`;

    const ctx = canvas.getContext('2d');
    // font color
    ctx.fillStyle = 'white';

    drawBackgroundMusicCard(canvas, ctx, (backgroundImgTag) => {
      // // date
      // ctx.font = `${image.width - image.width * 0.962}px Arial`;
      // ctx.fillText(
      //   `PHOTO ${dateString}`,
      //   image.width - image.width * 0.4114,
      //   image.height - image.height * 0.946
      // );

      // title
      ctx.font = `${
        backgroundImgTag.width - backgroundImgTag.width * 0.918
      }px Arial`;
      ctx.fillText(
        musicTitle,
        backgroundImgTag.width - backgroundImgTag.width * 0.903,
        backgroundImgTag.height - backgroundImgTag.height * 0.293
      );

      // artist
      ctx.font = `${
        backgroundImgTag.width - backgroundImgTag.width * 0.9543
      }px Arial`;
      ctx.fillText(
        `By. ${artistName}`,
        backgroundImgTag.width - backgroundImgTag.width * 0.903,
        backgroundImgTag.height - backgroundImgTag.height * 0.25
      );

      drawQueryImage(canvas, ctx, imgUrl, backgroundImgTag);
    });
  }

  handleDownload = () => {
    const canvas = this.canvasRef.current;

    if (canvas) {
      const dataURL = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.href = dataURL;
      link.download = 'card_image.png';
      link.click();
    }
  };

  render() {
    return (
      <>
        <div className="title">
          <canvas ref={this.canvasRef} style={{ width: '100%' }} />
        </div>
        <div className="bottom">
          <button
            className="downloadBnt"
            type="button"
            onClick={this.handleDownload}
          >
            <span>이미지 다운로드</span>
          </button>
        </div>
      </>
    );
  }
}

CardGenerator.defaultProps = {
  imgUrl: defaultImg,
  artistName: '아티스트 이름',
  musicTitle: '음악 제목',
};

CardGenerator.propTypes = {
  imgUrl: PropTypes.string,
  artistName: PropTypes.string,
  musicTitle: PropTypes.string,
};

export default CardGenerator;
