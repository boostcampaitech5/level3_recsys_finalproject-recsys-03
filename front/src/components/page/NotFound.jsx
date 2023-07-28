import React, { PureComponent } from 'react';
import logo from '../../imgs/logo.png';

export default class Home extends PureComponent {
  render() {
    return (
      <header className="App-header">
        <p>404 Not Found</p>
        <p>존재하지 않는 페이지 입니다.</p>
        <img src={logo} className="App-logo" alt="logo" />
      </header>
    );
  }
}
