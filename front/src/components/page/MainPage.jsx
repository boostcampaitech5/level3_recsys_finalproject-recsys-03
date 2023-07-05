import React from 'react';
import { useNavigate } from 'react-router-dom';

// const MainPage = () => {
//     const {} = props;
//     const navigate = useNavigate;
// };

function MainPage() {
  const navigate = useNavigate();
  const naviateToUpload = () => {
    navigate('/upload');
  };

  return (
    <div className="bg">
      <div className="NextPageBnt">
        <button type="button" onClick={naviateToUpload}>
          시작하기
        </button>
      </div>
    </div>
  );
}

export default MainPage;
