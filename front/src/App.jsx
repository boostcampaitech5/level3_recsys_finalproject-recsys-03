import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import MainPage from './components/page/MainPage';
import Loading from './components/page/Loading';
import MusicRecommend from './MusicRecommend';
import ImageUploader from './components/page/UploadPage';
import './App.css';

export default (
  <div className="App">
    <BrowserRouter>
      <Routes>
        <Route index element={<MainPage />} />
        <Route path="/upload" element={<ImageUploader />} />
        <Route path="/loading" element={<Loading />} />
        <Route path="/music-rec" element={<MusicRecommend />} />
      </Routes>
    </BrowserRouter>
  </div>
);
