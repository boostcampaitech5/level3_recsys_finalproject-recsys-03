import axios from 'axios';

const backendUrl = process.env.REACT_APP_BACKEND_HOST;

export default async function requestUserFeedback(sessionId, songId, isLike) {
  const data = {
    session_id: sessionId,
    song_id: songId,
    is_like: isLike,
  };
  return axios.post(`${backendUrl}/userFeedback`, JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
