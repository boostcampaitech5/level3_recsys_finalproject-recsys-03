import React from 'react';
import logo from '../imgs/logo.png';

function NotFoundPage() {
  return (
    <header className="App-header">
      <p>404 Not Found</p>
      <p>존재하지 않는 페이지 입니다.</p>
      <img src={logo} className="App-logo" alt="logo" />
    </header>
  );
}

export default NotFoundPage;
