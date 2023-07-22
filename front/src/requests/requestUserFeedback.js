import axios from 'axios';

const backendUrl = process.env.REACT_APP_BACKEND_HOST;

export default async function requestUserFeedback(
  sessionId,
  songId,
  thumbsup,
  thumbsdown
) {
  const data = {
    session_id: sessionId,
    song_id: songId,
    thumbs_up: thumbsup,
    thumbs_down: thumbsdown,
  };
  return axios.post(`${backendUrl}/userFeedback`, JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
