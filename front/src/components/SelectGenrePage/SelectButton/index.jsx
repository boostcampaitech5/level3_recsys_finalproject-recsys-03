import React, { PureComponent, createRef } from 'react';
import PropTypes from 'prop-types';
import './style.css';

export default class SelectButton extends PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      isSelected: false,
      enabled: true,
    };

    this.buttonRef = createRef();
  }

  setSelected = () => {
    const { isSelected, enabled } = this.state;

    if (!enabled) return;

    this.setState({
      isSelected: !isSelected,
    });

    if (!isSelected) {
      this.buttonRef.current.classList.add('selected');
    } else {
      this.buttonRef.current.classList.remove('selected');
    }
  };

  // eslint-disable-next-line react/no-unused-class-component-methods
  enable = () => {
    this.setState({
      enabled: true,
    });
  };

  // eslint-disable-next-line react/no-unused-class-component-methods
  disable = () => {
    const { isSelected } = this.state;
    this.setState({
      enabled: false,
    });

    if (isSelected) {
      this.setSelected();
    }
  };

  render() {
    const { img, canSelect } = this.props;
    const { enabled, isSelected } = this.state;

    return (
      <div className="SelectButton">
        <input
          ref={this.buttonRef}
          style={{ backgroundImage: `url('${img}')` }}
          type="button"
          onClick={() => {
            if (!isSelected && !canSelect()) {
              return;
            }

            this.setSelected();
          }}
          disabled={!enabled}
        />
        <svg
          className="CheckButton"
          width="30"
          height="30"
          viewBox="0 0 30 30"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          onClick={() => {
            if (!isSelected && !canSelect()) {
              return;
            }

            this.setSelected();
          }}
        >
          <circle cx="15" cy="15" r="15" fill="#F44404" />
          <path
            d="M22.8223 9.18559C22.9361 9.30458 23 9.46588 23 9.63405C23 9.80222 22.9361 9.96352 22.8223 10.0825L13.5047 19.8132C13.4476 19.8732 13.3796 19.9207 13.3047 19.9528C13.2297 19.9849 13.1494 20.0009 13.0684 20C12.9874 19.999 12.9074 19.9811 12.8331 19.9473C12.7589 19.9134 12.6919 19.8644 12.6361 19.803L8.17989 14.9377C8.12223 14.878 8.07661 14.8069 8.04571 14.7285C8.01482 14.6501 7.99929 14.566 8.00003 14.4812C8.00076 14.3964 8.01776 14.3127 8.05002 14.2349C8.08227 14.157 8.12913 14.0868 8.18782 14.0282C8.24651 13.9696 8.31584 13.9239 8.39173 13.8938C8.46762 13.8637 8.54851 13.8497 8.62964 13.8528C8.71078 13.8559 8.7905 13.8759 8.8641 13.9116C8.9377 13.9474 9.00369 13.9982 9.05817 14.0611L13.085 18.4568L21.9634 9.18559C22.0774 9.06675 22.2318 9 22.3929 9C22.5539 9 22.7083 9.06675 22.8223 9.18559Z"
            fill="white"
          />
        </svg>
      </div>
    );
  }
}

SelectButton.propTypes = {
  img: PropTypes.string.isRequired,
  canSelect: PropTypes.func.isRequired,
};
