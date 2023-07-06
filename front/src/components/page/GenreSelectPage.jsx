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
    type: '장르2',
  },
  {
    img: './dummy-1.jpg',
    type: '장르2',
  },
  {
    img: './dummy-1.jpg',
    type: '장르3',
  },
  {
    img: './dummy-1.jpg',
    type: '장르4',
  },
  {
    img: './dummy-1.jpg',
    type: '장르5',
  },
];

class GenreSelectorPage extends PureComponent {
  constructor(props) {
    super(props);
    this.selectButtons = genres.map(() => createRef());
  }

  onSubmit() {
    const { navigate } = this.props;

    const selectedGenreTypes = this.getSelectedGenreTypes();
    navigate('/upload', {
      state: {
        selectedGenreTypes,
      },
    });
  }

  getSelectedGenreTypes() {
    const selectedGenreTypes = [];

    this.selectButtons.forEach((selectButton, index) => {
      if (selectButton.current.state.isSelected) {
        selectedGenreTypes.push(genres[index].type);
      }
    });

    return selectedGenreTypes;
  }

  render() {
    return (
      <div className="GenreSelector">
        {genres.map((genre, index) => (
          <SelectButton ref={this.selectButtons[index]}>
            <img src={process.env.PUBLIC_URL + genre.img} alt={genre.type} />
            <p>{genre.type}</p>
          </SelectButton>
        ))}
        <button onClick={() => this.onSubmit()} type="submit">
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
