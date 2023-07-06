import React from 'react';
import { useNavigate } from 'react-router-dom';

function MainPage() {
  const navigate = useNavigate();
  const naviateToUpload = () => {
    navigate('/genre-select');
  };

  return (
    <div className="bg">
      <div className="Title">서비스명</div>
      <div className="NextPageBnt">
        <button type="button" onClick={naviateToUpload}>
          시작하기
        </button>
      </div>
    </div>
  );
}

export default MainPage;
