import { React, useState } from 'react';
import './Modal.css';
import PropTypes from 'prop-types';
import CardGen from './CardGenerator';

function Modal({ setOpenModal, imgUrl, artistName, musicTitle }) {
  const [thumup, setThumup] = useState(false);
  const [thumdown, setThumdown] = useState(false);
  const onThumup = () => {
    setThumdown(false);
    setThumup(!thumup);
  };
  const onThumdown = () => {
    setThumup(false);
    setThumdown(!thumdown);
  };

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
        <CardGen
          imgUrl={imgUrl}
          musicTitle={musicTitle}
          artistName={artistName}
        />
        <div className="feedback">
          <span>결과가 마음에 드셨나요?</span>
          <div className="thumbtns">
            <button
              className="thumbtn"
              onClick={() => onThumup()}
              type="button"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="20"
                viewBox="0 -960 960 960"
                width="20"
                fill={thumup ? '#f44404' : 'white'}
              >
                <path d="M716-120H272v-512l278-288 39 31q6 5 9 14t3 22v10l-45 211h299q24 0 42 18t18 42v81.839q0 7.161 1.5 14.661T915-461L789-171q-8.878 21.25-29.595 36.125Q738.689-120 716-120Zm-384-60h397l126-299v-93H482l53-249-203 214v427Zm0-427v427-427Zm-60-25v60H139v392h133v60H79v-512h193Z" />
              </svg>
            </button>
            <button
              className="thumbtn"
              onClick={() => onThumdown()}
              type="button"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="20"
                viewBox="0 -960 960 960"
                width="20"
                fill={thumdown ? '#f44404' : 'white'}
              >
                <path d="M242-840h444v512L408-40l-39-31q-6-5-9-14t-3-22v-10l45-211H103q-24 0-42-18t-18-42v-81.839Q43-477 41.5-484.5T43-499l126-290q8.878-21.25 29.595-36.125Q219.311-840 242-840Zm384 60H229L103-481v93h373l-53 249 203-214v-427Zm0 427v-427 427Zm60 25v-60h133v-392H686v-60h193v512H686Z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

Modal.propTypes = {
  setOpenModal: PropTypes.bool.isRequired,
  imgUrl: PropTypes.string.isRequired,
  artistName: PropTypes.string.isRequired,
  musicTitle: PropTypes.string.isRequired,
};

export default Modal;
