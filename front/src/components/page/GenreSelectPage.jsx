import React, { PureComponent, createRef } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import './GenreSelectPage.css';
import SelectButton from './SelectButton';

const genres = [
  {
    img: './dummy-1.jpg',
    type: '장르1',
  },
  {
    img: './dummy-1.jpg',
    type: '장르1',
  },
  {
    img: './dummy-1.jpg',
    type: '장르1',
  },
  {
    img: './dummy-1.jpg',
    type: '장르1',
  },
  {
    img: './dummy-1.jpg',
    type: '장르1',
  },
  {
    img: './dummy-1.jpg',
    type: '장르1',
  },
];

class GenreSelectorPage extends PureComponent {
  constructor(props) {
    super(props);
    this.nxtButton = createRef();
  }

  onSubmit() {
    const { navigate } = this.props;
    navigate('/loading');
  }

  render() {
    return (
      <div className="GenreSelector">
        {genres.map((genre) => (
          <SelectButton>
            <img src={process.env.PUBLIC_URL + genre.img} alt={genre.type} />
            <p>{genre.type}</p>
          </SelectButton>
        ))}
        <button
          ref={this.nxtButton}
          onClick={() => this.onSubmit()}
          type="submit"
        >
          다음으로
        </button>
      </div>
    );
  }
}

GenreSelectorPage.propTypes = {
  navigate: PropTypes.func.isRequired,
};

export default function GenreSelectorPageWrapper(props) {
  const navigate = useNavigate();

  // eslint-disable-next-line react/jsx-props-no-spreading
  return <GenreSelectorPage {...props} navigate={navigate} />;
}
