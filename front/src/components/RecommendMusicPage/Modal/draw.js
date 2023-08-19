import backgroundMusicCardImg from './imgs/white_background_qr.png';

export const drawBackgroundMusicCard = (canvas, ctx, onLoadFinished) => {
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

export const drawQueryImage = (
  canvas,
  ctx,
  url,
  backgroundImgTag,
  onLoadFinished
) => {
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

    onLoadFinished();
  };
};
