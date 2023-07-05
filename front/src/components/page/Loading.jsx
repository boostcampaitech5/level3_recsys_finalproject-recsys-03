import React, { PureComponent } from 'react';
import './Loading.css';

export default class Loading extends PureComponent {
  render() {
    return (
      <div className="Loading-div">
        <h1>⭐️ 곧 결과가 나옵니다 ⭐️</h1>
        <h3> 잠시만 기다려 주세요 ^~^</h3>
        <img
          className="Spinner"
          src={`${process.env.PUBLIC_URL}/spining.svg`}
          alt="spinner"
        />
      </div>
    );
  }
}
