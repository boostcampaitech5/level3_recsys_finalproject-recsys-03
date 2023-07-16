import axios from 'axios';

const urlToBlob = async (url) => {
  const res = await fetch(url);
  return res.blob();
};

export default async function requestRecommendMusic(imageUrl, genres) {
  const imageBlob = await urlToBlob(imageUrl);

  const formData = new FormData();
  formData.append('image', imageBlob);
  formData.append('genres', genres);

  return axios
    .post(`/api/recommendMusic`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((res) => res.data);
}
