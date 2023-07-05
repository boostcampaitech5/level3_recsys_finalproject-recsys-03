import React, { PureComponent } from 'react';

export default class Loading extends PureComponent {
  render() {
    return (
      <header className="Loading-header">
        <h1 style={{ color: '#FFF', paddingTop: '270px' }}>
          ⭐️ 곧 결과가 나옵니다 ⭐️
        </h1>
        <h3 style={{ color: '#FFF' }}> 잠시만 기다려 주세요 ^~^</h3>
        <img
          width="80px"
          src={`${process.env.PUBLIC_URL}/spinner.gif`}
          alt="spinner"
        />
      </header>
    );
  }
}
