import React from 'react';
import { useLocation } from 'react-router-dom';

function ImgCropper() {
  const location = useLocation();
  const Img = { ...location.state };
  return (
    <div>
      <img src={Img.url} alt="user_image" />
    </div>
  );
}

export default ImgCropper;
