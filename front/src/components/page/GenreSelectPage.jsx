import React, { PureComponent } from 'react';
import './GenreSelectPage.css';

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

export default class GenreSelector extends PureComponent {
  render() {
    return (
      <div className="GenreSelector">
        {genres.map((genre) => (
          <div>
            <img src={process.env.PUBLIC_URL + genre.img} alt={genre.type} />
            <p>{genre.type}</p>
          </div>
        ))}
      </div>
    );
  }
}
