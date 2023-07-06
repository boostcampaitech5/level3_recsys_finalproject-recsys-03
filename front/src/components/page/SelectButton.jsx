import React, { PureComponent, createRef } from 'react';
import PropTypes from 'prop-types';
import './SelectButton.css';

export default class SelectButton extends PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      isSelected: false,
    };

    this.buttonRef = createRef();
  }

  setSelected = () => {
    const { isSelected } = this.state;

    this.setState({
      isSelected: !isSelected,
    });

    if (!isSelected) {
      this.buttonRef.current.classList.add('selected');
    } else {
      this.buttonRef.current.classList.remove('selected');
    }
  };

  render() {
    const { children } = this.props;

    return (
      <button
        ref={this.buttonRef}
        className="SelectButton"
        type="button"
        onClick={() => {
          this.setSelected();
        }}
      >
        {children}
      </button>
    );
  }
}

SelectButton.propTypes = {
  children: PropTypes.node.isRequired,
};
