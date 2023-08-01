import popImg from './imgs/pop.jpg';
import rockImg from './imgs/rock.jpg';
import kpopImg from './imgs/kpop.jpg';
import indieImg from './imgs/indie.jpg';
import danceImg from './imgs/dance.jpg';
import hippopImg from './imgs/hippop.jpg';
import balladeImg from './imgs/ballade.jpg';
import randbImg from './imgs/r&b.jpg';
import etcImg from './imgs/etc.jpg';

const genres = [
  {
    img: popImg,
    type: 'POP',
  },
  {
    img: kpopImg,
    type: '가요',
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

export default genres;
