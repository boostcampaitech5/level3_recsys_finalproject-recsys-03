import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import MainPage from './components/page/MainPage';
import Loading from './components/page/Loading';
import GenreSelector from './components/page/GenreSelectPage';
import MusicRecommend from './MusicRecommend';
import ImageUploader from './components/page/UploadPage';
import ImgCropper from './components/page/CropPage';
import './App.css';

export default (
  <div className="App">
    <BrowserRouter>
      <Routes>
        <Route index element={<MainPage />} />
        <Route path="/upload" element={<ImageUploader />} />
        <Route path="/crop" element={<ImgCropper />} />
        <Route path="/loading" element={<Loading />} />
        <Route path="/genre-select" element={<GenreSelector />} />
        <Route path="/music-rec" element={<MusicRecommend />} />
      </Routes>
    </BrowserRouter>
  </div>
);
