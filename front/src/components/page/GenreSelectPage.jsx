import React, { PureComponent, createRef } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import './GenreSelectPage.css';
import SelectButton from './SelectButton';

const genres = [
  {
    img: './dummy-1.jpg',
    type: 'POP',
  },
  {
    img: './dummy-2.jpg',
    type: 'K-POP',
  },
  {
    img: './dummy-3.jpg',
    type: '락',
  },
  {
    img: './dummy-1.jpg',
    type: '인디',
  },
  {
    img: './dummy-2.jpg',
    type: '댄스',
  },
  {
    img: './dummy-3.jpg',
    type: '랩/힙합',
  },
  {
    img: './dummy-3.jpg',
    type: '발라드',
  },
  {
    img: './dummy-3.jpg',
    type: 'R&B',
  },
  {
    img: './dummy-3.jpg',
    type: '기타',
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
        genres: selectedGenreTypes,
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
      <div className="GenreSelectPage">
        <div className="header">
          <h1>당신의 취향을 알려주세요</h1>
          <h3>AI가 당신의 취향을 고려해서 노래를 찾아드릴게요</h3>
        </div>
        <div className="GenreSelectorWrapper">
          <div className="GenreSelector">
            {genres.map((genre, index) => (
              <SelectButton ref={this.selectButtons[index]}>
                <img
                  src={process.env.PUBLIC_URL + genre.img}
                  alt={genre.type}
                />
                <p>{genre.type}</p>
              </SelectButton>
            ))}
          </div>
          <button
            className="NextButton"
            onClick={() => this.onSubmit()}
            type="submit"
          >
            <span>다음으로</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="35"
              viewBox="0 -960 960 960"
              width="35"
            >
              <path d="m242-200 210-280-210-280h74l210 280-210 280h-74Zm252 0 210-280-210-280h74l210 280-210 280h-74Z" />
            </svg>
          </button>
        </div>
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
