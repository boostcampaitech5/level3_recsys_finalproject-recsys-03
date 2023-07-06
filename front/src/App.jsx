import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import MainPage from './components/page/MainPage';
import ImageUploadPage from './components/page/UploadPage';
import Loading from './components/page/Loading';
import GenreSelector from './components/page/GenreSelectPage';
import MusicRecommend from './MusicRecommend';
import './App.css';

export default (
  <div className="App">
    <BrowserRouter>
      <Routes>
        <Route index element={<MainPage />} />
        <Route path="/upload" element={<ImageUploadPage />} />
        <Route path="/loading" element={<Loading />} />
        <Route path="/genre-select" element={<GenreSelector />} />
        <Route path="/music-rec" element={<MusicRecommend />} />
      </Routes>
    </BrowserRouter>
  </div>
);
