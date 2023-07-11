import React, { PureComponent, createRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiChevronsRight } from 'react-icons/fi';
import PropTypes from 'prop-types';
import './GenreSelectPage.css';
import SelectButton from './SelectButton';
import popImg from '../../imgs/pop.jpg';
import rockImg from '../../imgs/rock.jpg';
import kpopImg from '../../imgs/kpop.jpg';
import indieImg from '../../imgs/indie.jpg';
import danceImg from '../../imgs/dance.jpg';
import hippopImg from '../../imgs/hippop.jpg';
import balladeImg from '../../imgs/ballade.jpg';
import randbImg from '../../imgs/r&b.jpg';
import etcImg from '../../imgs/etc.jpg';

const genres = [
  {
    img: popImg,
    type: 'POP',
  },
  {
    img: kpopImg,
    type: 'K-POP',
  },
  {
    img: rockImg,
    type: '락',
  },
  {
    img: indieImg,
    type: '인디',
  },
  {
    img: danceImg,
    type: '댄스',
  },
  {
    img: hippopImg,
    type: '랩/힙합',
  },
  {
    img: balladeImg,
    type: '발라드',
  },
  {
    img: randbImg,
    type: 'R&B',
  },
  {
    img: etcImg,
    type: '기타',
  },
];

class GenreSelectorPage extends PureComponent {
  constructor(props) {
    super(props);
    this.selectButtons = genres.map(() => createRef());
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

  goNext() {
    const { navigate } = this.props;

    const selectedGenreTypes = this.getSelectedGenreTypes();
    navigate('/upload', {
      state: {
        genres: selectedGenreTypes,
      },
    });
  }

  render() {
    return (
      <div className="GenreSelectPage">
        <div className="content">
          <div className="header">
            <h1>당신의 취향을 알려주세요</h1>
            <h3>AI가 당신의 취향을 고려해서 노래를 찾아드릴게요</h3>
          </div>
          <div className="GenreSelectorWrapper">
            <div className="GenreSelector">
              {genres.map((genre, index) => (
                <div className="genreBox">
                  <SelectButton
                    key={genre.type}
                    ref={this.selectButtons[index]}
                    img={genre.img}
                  />
                  <p>{genre.type}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="footer">
          <button className="next" onClick={() => this.goNext()} type="button">
            <span>다음으로</span>
            <FiChevronsRight />
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
