import React from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Home from './Home';
import MusicRecommend from './MusicRecommend';
import './App.css';

export default (
  <div className="App">
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/music-rec" element={<MusicRecommend />} />
      </Routes>
    </BrowserRouter>
  </div>
);
