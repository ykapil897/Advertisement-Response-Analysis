import { useState } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Analyse from './components/Analyse';
import Predict from './components/Predict';

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analyse" element={<Analyse />} />
        <Route path="/predict" element={<Predict />} />
      </Routes>
    </Router>
  )
}

export default App
