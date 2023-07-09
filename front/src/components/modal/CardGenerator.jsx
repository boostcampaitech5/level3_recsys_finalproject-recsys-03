import React, { Component } from 'react';
import PropTypes from 'prop-types';
import defaultImg from '../../dummy512.jpg';

class CardGenerator extends Component {
  constructor(props) {
    super(props);
    this.canvasRef = React.createRef();
  }

  componentDidMount() {
    const { imgUrl } = this.props;

    const canvas = this.canvasRef.current;
    // origin: 525
    canvas.width = 525;
    // origin: 884
    canvas.height = 884;
    const ctx = canvas.getContext('2d');

    // get date
    // const today = new Date();
    // const year = today.getFullYear();
    // const month = String(today.getMonth() + 1).padStart(2, '0');
    // const day = String(today.getDate()).padStart(2, '0');
    // const dateString = `${year}.${month}.${day}`;

    const image = new Image();
    const inner = new Image();

    image.src = `${process.env.PUBLIC_URL}/background-music-card.png`;
    inner.src = imgUrl;

    image.width = canvas.width;
    image.height = image.width + image.width * 0.68;
    image.onload = () => {
      // background
      ctx.drawImage(image, 0, 0, image.width, image.height);
      // user img
      inner.onload = () => {
        const cornerRadius = 15; // radi
        const x = image.width - image.width * 0.939;
        const y = image.height - image.height * 0.932;
        const innerwidth = image.width - image.width * 0.118;
        const innerheight = image.width - image.width * 0.118;

        ctx.beginPath();
        ctx.moveTo(x + cornerRadius, y);
        ctx.lineTo(x + innerwidth - cornerRadius, y);
        ctx.arcTo(
          x + innerwidth,
          y,
          x + innerwidth,
          y + cornerRadius,
          cornerRadius
        );
        ctx.lineTo(x + innerwidth, y + innerheight - cornerRadius);
        ctx.arcTo(
          x + innerwidth,
          y + innerheight,
          x + innerwidth - cornerRadius,
          y + innerheight,
          cornerRadius
        );
        ctx.lineTo(x + cornerRadius, y + innerheight);
        ctx.arcTo(
          x,
          y + innerheight,
          x,
          y + innerheight - cornerRadius,
          cornerRadius
        );
        ctx.lineTo(x, y + cornerRadius);
        ctx.arcTo(x, y, x + cornerRadius, y, cornerRadius);
        ctx.closePath();

        ctx.clip();

        ctx.drawImage(inner, x, y, innerwidth, innerheight);
      };
      // font color
      ctx.fillStyle = 'white';

      // // date
      // ctx.font = `${image.width - image.width * 0.962}px Arial`;
      // ctx.fillText(
      //   `PHOTO ${dateString}`,
      //   image.width - image.width * 0.4114,
      //   image.height - image.height * 0.946
      // );

      // title
      ctx.font = `${image.width - image.width * 0.918}px Arial`;
      ctx.fillText(
        `세렝게티처럼`,
        image.width - image.width * 0.903,
        image.height - image.height * 0.293
      );

      // artist
      ctx.font = `${image.width - image.width * 0.9543}px Arial`;
      ctx.fillText(
        `By. 조용필`,
        image.width - image.width * 0.903,
        image.height - image.height * 0.25
      );
    };
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
};

CardGenerator.propTypes = {
  imgUrl: PropTypes.string,
};

export default CardGenerator;
