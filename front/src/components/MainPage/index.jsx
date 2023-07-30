import React from 'react';
import { useNavigate } from 'react-router-dom';
import './style.css';

function MainPage() {
  const navigate = useNavigate();
  const naviateToUpload = () => {
    navigate('/genre-select');
  };

  return (
    <div className="MainPage">
      <div className="contents">
        <div className="space" />
        <div className="line" />
        <div className="title">
          당신의 <span className="colored">일상</span>에 <br />
          <span className="colored">노래</span>를 <br /> 찾아드립니다
        </div>
        <div className="line" />

        <div className="subtitle">
          AI가 당신의 일상 사진에
          <br />
          어울리는 노래를 찾아드립니다 <br />
          <br />
          <span className="border">내 일상의 BGM을 만나보세요</span>
        </div>

        <div className="footer">
          <button className="starbBnt" type="button" onClick={naviateToUpload}>
            <span>시작하기</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default MainPage;
