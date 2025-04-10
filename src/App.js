import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import ResumeUpload from './components/ResumeUpload';
import ResumeList from './components/ResumeList';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<ResumeUpload />} />
            <Route path="/resumes" element={<ResumeList />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 