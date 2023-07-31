import React, { PureComponent, createRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiChevronsRight, FiChevronsLeft } from 'react-icons/fi';
import PropTypes from 'prop-types';
import './style.css';
import SelectButton from './SelectButton';
import genres from './genres';

class SelectGenrePage extends PureComponent {
  constructor(props) {
    super(props);
    this.selectButtons = genres.map(() => createRef());
    this.genreSelectorRef = createRef();
    this.state = {
      selectedNoMatter: false,
    };
  }

  getSelectedGenreTypes() {
    const { selectedNoMatter } = this.state;
    const selectedGenreTypes = [];

    this.selectButtons.forEach((selectButton, index) => {
      if (selectedNoMatter || selectButton.current.state.isSelected) {
        selectedGenreTypes.push(genres[index].type);
      }
    });

    return selectedGenreTypes;
  }

  canSelectSelectButton() {
    const selectedGenreTypes = this.getSelectedGenreTypes();

    if (selectedGenreTypes.length >= 8) {
      alert('8개까지 선택할 수 있습니다');
      return false;
    }
    return true;
  }

  goNext() {
    const { navigate } = this.props;

    const selectedGenreTypes = this.getSelectedGenreTypes();

    if (selectedGenreTypes.length === 0) {
      alert('장르를 선택해야 합니다');
      return;
    }

    navigate('/upload', {
      state: {
        genres: selectedGenreTypes,
      },
    });
  }

  goPrev() {
    const { navigate } = this.props;
    navigate('/');
  }

  toggleNoMatter() {
    const { selectedNoMatter } = this.state;
    const newSelectedNoMatter = !selectedNoMatter;

    this.setState(
      {
        selectedNoMatter: newSelectedNoMatter,
      },
      () => {
        this.selectButtons.forEach((selectButton) => {
          if (newSelectedNoMatter) {
            selectButton.current.disable();
          } else {
            selectButton.current.enable();
          }
        });
      }
    );

    if (newSelectedNoMatter)
      this.genreSelectorRef.current.classList.add('disabled');
    else this.genreSelectorRef.current.classList.remove('disabled');
  }

  render() {
    const { selectedNoMatter } = this.state;

    return (
      <div className="GenreSelectPage">
        <div className="content">
          <div className="header">
            <h1>당신의 취향을 알려주세요</h1>
            <h3>AI가 당신의 취향을 고려해서 노래를 찾아드릴게요</h3>
          </div>
          <div className="GenreSelectorWrapper">
            <div className="GenreSelector" ref={this.genreSelectorRef}>
              {genres.map((genre, index) => (
                <div className="genreBox">
                  <SelectButton
                    canSelect={() => this.canSelectSelectButton()}
                    key={genre.type}
                    ref={this.selectButtons[index]}
                    img={genre.img}
                  />
                  <p>{genre.type}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="noMatterWrapper">
            <input
              type="checkbox"
              name="no-matter"
              id="no-matter"
              checked={selectedNoMatter}
              onChange={() => this.toggleNoMatter()}
            />
            <label htmlFor="no-matter">상관없음</label>
          </div>
        </div>
        <div className="footer">
          <div className="buttons">
            <button
              className="prev"
              type="button"
              onClick={() => this.goPrev()}
            >
              <FiChevronsLeft />
              이전으로
            </button>
            <button
              className="next"
              type="button"
              onClick={() => this.goNext()}
            >
              다음으로
              <FiChevronsRight />
            </button>
          </div>
        </div>
      </div>
    );
  }
}

SelectGenrePage.propTypes = {
  navigate: PropTypes.func.isRequired,
};

export default function SelectGenrePageWrapper(props) {
  const navigate = useNavigate();

  // eslint-disable-next-line react/jsx-props-no-spreading
  return <SelectGenrePage {...props} navigate={navigate} />;
}
