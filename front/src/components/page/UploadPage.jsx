import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiUpload } from 'react-icons/fi';
import './UploadPage.css';

function ImageUploadPage() {
  const location = useLocation();
  const info = { ...location.state };

  const navigate = useNavigate();
  const naviagteToNext = (Imgurl) => {
    navigate('/crop', {
      state: {
        url: Imgurl,
        genres: info.selectedGenreTypes,
      },
    });
  };

  const insertImg = (e) => {
    const reader = new FileReader();

    if (e.target.files[0]) {
      reader.readAsDataURL(e.target.files[0]);
    }

    reader.onloadend = () => {
      const previewImgUrl = reader.result;
      if (previewImgUrl) {
        naviagteToNext(e.target.files[0]);
      }
    };
  };

  return (
    <div className="UploadPage">
      <div className="contents">
        <div className="header">
          <h1>일상 사진을 올려주세요</h1>
          <h3>어울리는 노래를 찾고싶은 사진을 선택해주세요</h3>
        </div>
        <div className="guideBox" />
      </div>

      <div className="footer">
        <label htmlFor="file" className="bnt-container">
          <div className="uploadBnt">
            <span>사진 업로드하기 </span>
            <FiUpload />
          </div>
        </label>
        <input
          type="file"
          id="file"
          accept="image/png, image/jpg, image/jpeg, image/gif"
          onChange={(e) => insertImg(e)}
          style={{ display: 'none' }}
        />
      </div>
    </div>
  );
}

export default ImageUploadPage;
