import React from 'react';
import { useNavigate } from 'react-router-dom';
import './style.css';
import error from './error.png';

function ErrorPage() {
  const navigate = useNavigate();
  const goBack = () => {
    navigate(-1);
  };

  return (
    <div className="ErrorPage">
      <div className="contents">
        <img src={error} alt="error" />
        <h1 className="top-text">오류가 발생했습니다.</h1>
      </div>
      <div className="footer">
        <button type="button" onClick={goBack}>
          <span>뒤로가기</span>
        </button>
      </div>
    </div>
  );
}

export default ErrorPage;
