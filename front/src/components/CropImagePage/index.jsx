import React, { useCallback, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiCheckSquare, FiRotateCcw } from 'react-icons/fi';
import Cropper from 'react-easy-crop';
import './style.css';
import getCroppedImg from './cropImage';
import requestRecommendMusic from './requestRecommendMusic';

function CropImagePage() {
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
    navigate('/loading');

    requestRecommendMusic(croppedImage, info.genres)
      .then(({ session_id: sessionId, songs }) => {
        navigate('/music-rec', {
          state: {
            url: croppedImage,
            songs,
            sessionId,
          },
        });
      })
      .catch(() => {
        navigate('/error', {
          state: {
            backTo: '/upload',
          },
        });
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
        <div className="notice">
          <span>
            업로드한 이미지는 결과 분석 외의 용도로는 사용되지 않습니다
          </span>
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

export default CropImagePage;
