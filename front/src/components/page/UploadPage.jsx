import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiUpload } from 'react-icons/fi';
import './UploadPage.css';
import WrongImg1 from '../../wrong1.jpg';
import WrongImg2 from '../../wrong2.jpeg';
import WrongImg3 from '../../wrong4.jpg';
import GoodImg1 from '../../good1.jpeg';
import GoodImg2 from '../../good2.jpg';
import GoodImg3 from '../../good3.JPG';

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
        <div
          className="guideBox"
          onContextMenu={(e) => {
            e.preventDefault();
          }}
          // onSelect={(e) => {
          //   e.preventDefault();
          // }}
          draggable="false"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="40"
            viewBox="0 -960 960 960"
            width="40"
            style={{ marginTop: '4%' }}
          >
            <path d="m421-298 283-283-46-45-237 237-120-120-45 45 165 166Zm59 218q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0-340Z" />
          </svg>
          <br />
          <div className="exImg">
            <img className="imgSet" src={GoodImg1} alt="shaking" />
            <img className="imgSet" src={GoodImg2} alt="shaking" />
            <img className="imgSet" src={GoodImg3} alt="shaking" />
          </div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="40"
            viewBox="0 -960 960 960"
            width="40"
            style={{ marginTop: '7%' }}
          >
            <path d="m330-288 150-150 150 150 42-42-150-150 150-150-42-42-150 150-150-150-42 42 150 150-150 150 42 42ZM480-80q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0-340Z" />
          </svg>
          <div className="exImg">
            <img className="imgSet" src={WrongImg1} alt="shaking" />
            <img className="imgSet" src={WrongImg2} alt="shaking" />
            <img className="imgSet" src={WrongImg3} alt="shaking" />
          </div>
          <p>
            너무 흐릿한 사진, 형태를 알아볼 수 없을 정도로 <br />
            흔들리거나 너무 확대해서 찍은 사진은 결과가 <br />잘 안 나올 수도
            있어요
          </p>
        </div>
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
