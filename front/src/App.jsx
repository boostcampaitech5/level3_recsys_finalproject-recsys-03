import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainPage from './components/page/MainPage';
import ImageUploadPage from './components/page/UploadPage';

export default (
  <div className="App">
    <header className="App-header">
      <BrowserRouter>
        <Routes>
          <Route index element={<MainPage />} />
          <Route path="/upload" element={<ImageUploadPage />} />
        </Routes>
      </BrowserRouter>
    </header>
  </div>
);
