import React, { useCallback, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiCheckSquare, FiRotateCcw } from 'react-icons/fi';
import Cropper from 'react-easy-crop';
import './CropPage.css';
import getCroppedImg from '../../utils/cropImage';

function CropPage() {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);

  const location = useLocation();
  const info = { ...location.state };
  const [imgurl] = useState(() => URL.createObjectURL(info.url));
  const [croppedImage, setCroppedImage] = useState();

  const onCropComplete = useCallback(
    async (croppedArea, croppedAreaPixels) => {
      const croppedImageTmp = await getCroppedImg(imgurl, croppedAreaPixels);
      setCroppedImage(croppedImageTmp);
    },
    [imgurl, setCroppedImage]
  );

  const navigate = useNavigate();
  const naviagteToNext = () => {
    // sending data(cropped img, genres) must be added here
    navigate('/loading', {
      state: {
        url: croppedImage,
        genres: info.genres,
      },
    });
  };
  const goUploadPage = () => {
    // sending data(cropped img, genres) must be added here
    navigate('/upload', {
      state: {
        url: croppedImage,
        genres: info.genres,
      },
    });
  };

  return (
    <div className="CropPage">
      <div className="contents">
        <div className="header">
          <h1>이미지를 편집해주세요</h1>
          <h3>박스를 움직여 원하는 영역을 지정해주세요</h3>
        </div>

        <div className="container-cropper">
          <div className="cropper">
            <Cropper
              objectFit="cover"
              image={imgurl}
              crop={crop}
              zoom={zoom}
              aspect={3 / 3}
              maxZoom={3}
              onCropChange={setCrop}
              onCropComplete={onCropComplete}
              onZoomChange={setZoom}
            />
          </div>
        </div>
      </div>

      <div className="footer">
        <div className="buttons">
          <button
            className="retry"
            type="button"
            onClick={() => goUploadPage()}
          >
            <FiRotateCcw />
            다시선택
          </button>
          <button
            className="next"
            type="button"
            onClick={() => naviagteToNext()}
          >
            <FiCheckSquare />
            결과 보기
          </button>
        </div>
      </div>
    </div>
  );
}

export default CropPage;
