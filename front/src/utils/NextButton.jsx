import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';

export default class NextButton extends PureComponent {
  render() {
    const { name } = this.props;
    return (
      <div>
        <span>{name}</span>
      </div>
    );
  }
}

NextButton.propTypes = {
  name: PropTypes.string.isRequired,
};
