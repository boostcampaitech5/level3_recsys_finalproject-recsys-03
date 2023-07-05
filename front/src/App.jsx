import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import MainPage from './components/page/MainPage';
import ImageUploadPage from './components/page/UploadPage';
import MusicRecommend from './MusicRecommend';
import './App.css';

export default (
  <div className="App">
    <BrowserRouter>
      <Routes>
        <Route index element={<MainPage />} />
        <Route path="/upload" element={<ImageUploadPage />} />
        <Route path="/music-rec" element={<MusicRecommend />} />
      </Routes>
    </BrowserRouter>
  </div>
);
