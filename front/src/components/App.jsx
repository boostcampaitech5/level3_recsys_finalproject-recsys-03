import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import MainPage from './MainPage';
import LoadingPage from './LoadingPage';
import SelectGenrePage from './SelectGenrePage';
import MusicRecommendPage from './RecommendMusicPage';
import UploadImagePage from './UploadImagePage';
import CropImagePage from './CropImagePage';
import NotFoundPage from './NotFoundPage';
import ErrorPage from './ErrorPage';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="page">
        <BrowserRouter>
          <Routes>
            <Route index element={<MainPage />} />
            <Route path="/upload" element={<UploadImagePage />} />
            <Route path="/crop" element={<CropImagePage />} />
            <Route path="/loading" element={<LoadingPage />} />
            <Route path="/genre-select" element={<SelectGenrePage />} />
            <Route path="/music-rec" element={<MusicRecommendPage />} />
            <Route path="/error" element={<ErrorPage />} />
            <Route path="/*" element={<NotFoundPage />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
