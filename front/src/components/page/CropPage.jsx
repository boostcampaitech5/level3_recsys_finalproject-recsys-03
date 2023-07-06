import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Cropper from 'react-easy-crop';
import './CropPage.css';
// import generateDownload from '../utils/generateDownload';

function CropPage() {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);

  const location = useLocation();
  const Img = { ...location.state };
  const imgsrc = URL.createObjectURL(Img.url);

  const onCropComplete = (croppedArea, croppedAreaPixels) => {
    console.log(croppedArea, croppedAreaPixels);
  };

  return (
    <div>
      <div className="container-cropper">
        <div className="cropper">
          <Cropper
            image={imgsrc}
            crop={crop}
            zoom={zoom}
            aspect={1}
            onCropChange={setCrop}
            onCropComplete={onCropComplete}
            onZoomChange={setZoom}
          />
        </div>
      </div>
      <div>
        <button type="button">다시 선택</button>
        <button type="button">결과보기</button>
      </div>
    </div>
  );
}

export default CropPage;
