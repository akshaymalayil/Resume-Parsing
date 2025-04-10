import React, { useState } from 'react';
import axios from 'axios';
import { FaCloudUploadAlt } from 'react-icons/fa';
import ParsedResumeForm from './ParsedResumeForm';

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [parsedData, setParsedData] = useState(null);
  const [showForm, setShowForm] = useState(false);
  
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
    setParsedData(null);
    setShowForm(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    setUploading(true);
    try {
      const response = await axios.post(`${API_URL}/upload/`, formData);
      if (response.data.success) {
        setMessage('Resume uploaded and parsed successfully!');
        setParsedData(response.data.data);
        setShowForm(true);
      } else {
        setMessage('Error: ' + response.data.error);
      }
      setFile(null);
    } catch (error) {
      setMessage('Error uploading resume. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleSaveForm = async (formData) => {
    try {
      // Send the form data to the backend
      const response = await axios.post(`${API_URL}/save-resume/`, formData);
      
      if (response.data.success) {
        setMessage('Resume information saved successfully!');
        setParsedData(null);
        setShowForm(false);
      } else {
        setMessage('Error: ' + response.data.error);
      }
    } catch (error) {
      setMessage('Error saving information. Please try again.');
      console.error('Save error:', error);
    }
  };

  const handleCancelForm = () => {
    setParsedData(null);
    setShowForm(false);
    setMessage('');
  };

  // Show the form if data has been parsed
  if (showForm && parsedData) {
    return (
      <div className="max-w-4xl mx-auto">
        <ParsedResumeForm 
          parsedData={parsedData}
          onSave={handleSaveForm}
          onCancel={handleCancelForm}
        />
      </div>
    );
  }

  // Otherwise show the upload form
  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Resume</h2>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <FaCloudUploadAlt className="mx-auto h-12 w-12 text-gray-400" />
          <div className="mt-4">
            <label htmlFor="resume" className="cursor-pointer">
              <span className="text-blue-600 hover:text-blue-800">
                Click to upload
              </span>
              <input
                id="resume"
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>
            <p className="text-sm text-gray-500 mt-2">
              or drag and drop PDF, DOC, or DOCX files
            </p>
          </div>
          {file && (
            <p className="mt-2 text-sm text-gray-600">
              Selected file: {file.name}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={uploading || !file}
          className={`w-full py-2 px-4 rounded-lg text-white ${
            uploading || !file
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {uploading ? 'Uploading...' : 'Upload Resume'}
        </button>

        {message && (
          <p
            className={`text-sm ${
              message.includes('Error') ? 'text-red-600' : 'text-green-600'
            }`}
          >
            {message}
          </p>
        )}
      </form>
    </div>
  );
}

export default ResumeUpload; 