import React from 'react';
import './Modal.css';
import PropTypes from 'prop-types';
// import { saveAs } from 'file-saver';

function Modal({ setOpenModal }) {
  return (
    <div className="modalBackground">
      <div className="modalContainer">
        <div className="titleCloseBtn">
          <button
            type="button"
            onClick={() => {
              setOpenModal(false);
            }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="20"
              viewBox="0 -960 960 960"
              width="20"
              fill="#8B8B8C"
            >
              <path d="m249-207-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z" />
            </svg>
          </button>
        </div>
        <div className="title">
          <img
            className="cardImg"
            src={`${process.env.PUBLIC_URL}/dummy-music-card.png`}
            alt="music-card"
          />
        </div>
        <div className="bottom">
          <button className="downloadBnt" type="button">
            {/* <svg
              xmlns="http://www.w3.org/2000/svg"
              height="35"
              viewBox="0 -960 960 960"
              width="35"
            >
              <path d="M220-160q-24 0-42-18t-18-42v-143h60v143h520v-143h60v143q0 24-18 42t-42 18H220Zm260-153L287-506l43-43 120 120v-371h60v371l120-120 43 43-193 193Z" />
            </svg> */}
            <span>이미지 다운로드</span>
          </button>
        </div>
      </div>
    </div>
  );
}

Modal.propTypes = {
  setOpenModal: PropTypes.bool.isRequired,
};

export default Modal;
