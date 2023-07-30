import React from 'react';
import './style.css';

function LoadingPage() {
  return (
    <div className="contents">
      <div className="Loading-div">
        <h1 className="top-text">노래를 찾고있어요</h1>
        <p className="bott-text">
          10초 뒤면 결과를 볼 수 있습니다!
          <br />
          화면을 이탈하면 오류가 날 수 있으니 조금만 기다려주세요
        </p>
        <br />
        <img
          className="Spinner"
          src={`${process.env.PUBLIC_URL}/spinner.svg`}
          alt="spinner"
        />
      </div>
    </div>
  );
}

export default LoadingPage;
