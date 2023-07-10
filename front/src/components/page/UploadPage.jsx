import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiUpload } from 'react-icons/fi';
import './UploadPage.css';
import heic2any from 'heic2any';

function ImageUploadPage() {
  const location = useLocation();
  const info = { ...location.state };

  const navigate = useNavigate();
  const naviagteToNext = (Imgurl) => {
    navigate('/crop', {
      state: {
        url: Imgurl,
        genres: info.genres,
      },
    });
  };

  const insertImg = (e) => {
    const reader = new FileReader();
    const image = e.target.files[0];

    // check data is inputted
    if (image) {
      reader.readAsDataURL(image);
    }

    // check image type is heic and send it to next page
    reader.onloadend = async () => {
      const previewImgUrl = reader.result;
      let url = URL.createObjectURL(image);

      if (previewImgUrl) {
        if (
          image.type.indexOf('image/heic') !== -1 ||
          image.type.indexOf('image/heif') !== -1
        ) {
          const blobURL = URL.createObjectURL(image);
          const blobRes = await fetch(blobURL);
          const blob = await blobRes.blob();
          const conversionResult = await heic2any({
            blob,
            toType: 'image/jpeg',
            quality: 1,
          });
          url = URL.createObjectURL(conversionResult);
        }
        naviagteToNext(url);
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
          accept="image/png, image/jpg, image/jpeg, image/gif, image/heic, image/heif"
          onChange={(e) => insertImg(e)}
          style={{ display: 'none' }}
        />
      </div>
    </div>
  );
}

export default ImageUploadPage;
