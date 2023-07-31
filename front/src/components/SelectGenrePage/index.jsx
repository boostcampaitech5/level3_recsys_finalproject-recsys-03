import React, { useCallback, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiChevronsRight, FiChevronsLeft } from 'react-icons/fi';
import './style.css';
import SelectButton from './SelectButton';
import genres from './genres';

function SelectGenrePage() {
  const navigate = useNavigate();

  const [selectedNoMatter, setSelectedNoMatter] = useState(false);

  const selectButtons = useRef(new Array(genres.length));
  const genreSelectorRef = useRef();

  const getSelectedGenreTypes = useCallback(() => {
    const selectedGenreTypes = [];

    selectButtons.current.forEach((selectButton, index) => {
      if (selectedNoMatter || selectButton.state.isSelected) {
        selectedGenreTypes.push(genres[index].type);
      }
    });

    return selectedGenreTypes;
  }, [selectButtons, selectedNoMatter]);

  const canSelectSelectButton = useCallback(() => {
    const selectedGenreTypes = getSelectedGenreTypes();

    if (selectedGenreTypes.length >= 8) {
      alert('8개까지 선택할 수 있습니다');
      return false;
    }
    return true;
  }, [getSelectedGenreTypes]);

  const goNext = useCallback(() => {
    const selectedGenreTypes = getSelectedGenreTypes();

    if (selectedGenreTypes.length === 0) {
      alert('장르를 선택해야 합니다');
      return;
    }

    navigate('/upload', {
      state: {
        genres: selectedGenreTypes,
      },
    });
  }, [getSelectedGenreTypes, navigate]);

  const goPrev = useCallback(() => {
    navigate('/');
  }, [navigate]);

  const toggleNoMatter = useCallback(() => {
    const newSelectedNoMatter = !selectedNoMatter;

    setSelectedNoMatter(newSelectedNoMatter);

    selectButtons.current.forEach((selectButton) => {
      if (newSelectedNoMatter) {
        selectButton.disable();
      } else {
        selectButton.enable();
      }
    });

    if (newSelectedNoMatter) genreSelectorRef.current.classList.add('disabled');
    else genreSelectorRef.current.classList.remove('disabled');
  }, [selectedNoMatter, selectButtons, genreSelectorRef]);

  return (
    <div className="GenreSelectPage">
      <div className="content">
        <div className="header">
          <h1>당신의 취향을 알려주세요</h1>
          <h3>AI가 당신의 취향을 고려해서 노래를 찾아드릴게요</h3>
        </div>
        <div className="GenreSelectorWrapper">
          <div className="GenreSelector" ref={genreSelectorRef}>
            {genres.map((genre, index) => (
              <div className="genreBox" key={genre.type}>
                <SelectButton
                  canSelect={canSelectSelectButton}
                  key={genre.type}
                  ref={(el) => {
                    selectButtons.current[index] = el;
                  }}
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
            onChange={() => toggleNoMatter()}
          />
          <label htmlFor="no-matter">상관없음</label>
        </div>
      </div>
      <div className="footer">
        <div className="buttons">
          <button className="prev" type="button" onClick={() => goPrev()}>
            <FiChevronsLeft />
            이전으로
          </button>
          <button className="next" type="button" onClick={() => goNext()}>
            다음으로
            <FiChevronsRight />
          </button>
        </div>
      </div>
    </div>
  );
}

export default SelectGenrePage;
