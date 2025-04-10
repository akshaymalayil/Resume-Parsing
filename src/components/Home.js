import React from 'react';
import { Link } from 'react-router-dom';
import { FaUpload } from 'react-icons/fa';

function Home() {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">
        Welcome to Resume Parser
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        Upload resumes and get detailed insights about candidates
      </p>
      <Link
        to="/upload"
        className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        <FaUpload className="mr-2" />
        Upload Resume
      </Link>
    </div>
  );
}

export default Home; 