import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './style.css';
import error from './error.png';

const defaultErrorMsg = '오류가 발생했습니다.';

function ErrorPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const backTo = location.state?.backTo;
  const errorMsg = location.state?.errorMsg ?? defaultErrorMsg;

  const goBack = () => {
    navigate(backTo);
  };

  return (
    <div className="ErrorPage">
      <div className="contents">
        <img src={error} alt="error" />
        <h1 className="top-text">{errorMsg}</h1>
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
