import { React } from 'react';
import './style.css';
import PropTypes from 'prop-types';
import CardGen from './CardGenerator';

function Modal({ setOpenModal, imgUrl, artistName, musicTitle }) {
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
