import React, { useCallback, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Cropper from 'react-easy-crop';
import './CropPage.css';
import getCroppedImg from '../../utils/cropImage';

function CropPage() {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);

  const location = useLocation();
  const info = { ...location.state };
  const [imgurl] = useState(info.url);
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
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="35"
              viewBox="0 -960 960 960"
              width="35"
            >
              <path d="M480-160q-133 0-226.5-93.5T160-480q0-133 93.5-226.5T480-800q85 0 149 34.5T740-671v-129h60v254H546v-60h168q-38-60-97-97t-137-37q-109 0-184.5 75.5T220-480q0 109 75.5 184.5T480-220q83 0 152-47.5T728-393h62q-29 105-115 169t-195 64Z" />
            </svg>
            다시선택
          </button>
          <button
            className="next"
            type="button"
            onClick={() => naviagteToNext()}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="35"
              viewBox="0 -960 960 960"
              width="35"
            >
              <path d="M220-40q-24 0-42-18t-18-42v-509q0-24 18-42t42-18h169v60H220v509h520v-509H569v-60h171q24 0 42 18t18 42v509q0 24-18 42t-42 18H220Zm229-307v-457l-88 88-43-43 161-161 161 161-43 43-88-88v457h-60Z" />
            </svg>
            결과 보기
          </button>
        </div>
      </div>
    </div>
  );
}

export default CropPage;
