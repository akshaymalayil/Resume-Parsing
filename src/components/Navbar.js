import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaUpload, FaList } from 'react-icons/fa';

function Navbar() {
  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold text-gray-800">
              Resume Parser
            </Link>
          </div>
          <div className="flex space-x-4">
            <Link to="/" className="flex items-center text-gray-600 hover:text-gray-900">
              <FaHome className="mr-2" />
              Home
            </Link>
            <Link to="/upload" className="flex items-center text-gray-600 hover:text-gray-900">
              <FaUpload className="mr-2" />
              Upload
            </Link>
            <Link to="/resumes" className="flex items-center text-gray-600 hover:text-gray-900">
              <FaList className="mr-2" />
              Resumes
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 