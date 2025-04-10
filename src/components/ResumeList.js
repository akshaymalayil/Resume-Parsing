import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { FaFileAlt, FaDownload } from 'react-icons/fa';

function ResumeList() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  const fetchResumes = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/resumes/`);
      setResumes(response.data);
    } catch (error) {
      setError('Error fetching resumes. Please try again later.');
      console.error('Fetch error:', error);
    } finally {
      setLoading(false);
    }
  }, [API_URL]);

  useEffect(() => {
    fetchResumes();
  }, [fetchResumes]);

  const handleDownload = async (resumeId) => {
    try {
      const response = await axios.get(`${API_URL}/resumes/${resumeId}/download/`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `resume_${resumeId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setError('Error downloading resume. Please try again.');
      console.error('Download error:', error);
    }
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-600">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Parsed Resumes</h2>
      {resumes.length === 0 ? (
        <p className="text-center text-gray-600">No resumes found.</p>
      ) : (
        <div className="grid gap-4">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <FaFileAlt className="h-6 w-6 text-gray-400 mr-3" />
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">
                      {resume.name}
                    </h3>
                    <p className="text-sm text-gray-600">
                      Uploaded on: {new Date(resume.uploaded_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDownload(resume.id)}
                  className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <FaDownload className="mr-2" />
                  Download
                </button>
              </div>
              <div className="mt-4">
                <h4 className="font-semibold text-gray-700">Parsed Information:</h4>
                <div className="mt-2 grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Email: {resume.email}</p>
                    <p className="text-sm text-gray-600">Phone: {resume.phone}</p>
                    <p className="text-sm text-gray-600">Skills: {resume.skills.join(', ')}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Experience: {resume.experience} years</p>
                    <p className="text-sm text-gray-600">Education: {resume.education}</p>
                    <p className="text-sm text-gray-600">Location: {resume.location}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ResumeList; 