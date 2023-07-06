import React, { useCallback, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Cropper from 'react-easy-crop';
import './CropPage.css';

function CropPage() {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);

  const location = useLocation();
  const info = { ...location.state };
  const imgurl = URL.createObjectURL(info.url);

  // eslint-disable-next-line no-unused-vars
  const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
    // console.log(croppedArea, croppedAreaPixels);
  }, []);

  const navigate = useNavigate();
  const naviagteToNext = () => {
    // sending data(cropped img, genres) must be added here
    navigate('/loading');
  };

  return (
    <div>
      <div className="page-title">이미지를 잘라주세요.</div>
      <div className="container-cropper">
        <div className="cropper">
          <Cropper
            image={imgurl}
            crop={crop}
            zoom={zoom}
            aspect={3 / 3}
            onCropChange={setCrop}
            onCropComplete={onCropComplete}
            onZoomChange={setZoom}
          />
        </div>
      </div>
      <div className="buttons">
        <button type="button" onClick={() => navigate(-1)}>
          다시 선택
        </button>
        <button type="button" onClick={naviagteToNext}>
          결과보기
        </button>
      </div>
    </div>
  );
}

export default CropPage;
