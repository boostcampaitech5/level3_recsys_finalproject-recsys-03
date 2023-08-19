import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiChevronsLeft } from 'react-icons/fi';
import './style.css';
import heic2any from 'heic2any';
import WrongImg1 from './imgs/wrong1.jpg';
import WrongImg2 from './imgs/wrong2.jpg';
import WrongImg3 from './imgs/wrong3.jpg';
import GoodImg1 from './imgs/good1.jpg';
import GoodImg2 from './imgs/good2.jpg';
import GoodImg3 from './imgs/good3.jpg';

function UploadImagePage() {
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

  const naviagteToPrev = () => {
    navigate('/genre-select');
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
            배경이 잘 보이지 않는 사진은 <br />
            결과가 정확하지 않을 수도 있어요
          </p>
        </div>
      </div>
      <div className="footer">
        <div className="buttons">
          <button
            className="prev"
            type="button"
            onClick={() => naviagteToPrev()}
          >
            <FiChevronsLeft />
            이전으로
          </button>
          <label htmlFor="file" className="uploadBnt">
            <div>
              <span>업로드하기 </span>
            </div>
          </label>
          <input
            type="file"
            id="file"
            accept="image/png, image/jpg, image/jpeg, image/heic, image/heif"
            onChange={(e) => insertImg(e)}
            style={{ display: 'none' }}
          />
        </div>
      </div>
    </div>
  );
}

export default UploadImagePage;
