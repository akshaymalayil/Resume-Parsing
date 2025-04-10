import React, { useState, useEffect } from 'react';

const ParsedResumeForm = ({ parsedData, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    yearOfPassing: '',
    branchOfEngineering: '',
    cgpa: '',
    backlogs: '0',
    liveBacklogs: '0',
    internships: '',
    programmingLanguages: [],
    projects: '',
    skills: []
  });

  // Initialize form with parsed data when it becomes available
  useEffect(() => {
    if (parsedData) {
      const education = parsedData.education || {};
      
      setFormData({
        name: parsedData.name || '',
        email: parsedData.email || '',
        phone: parsedData.phone || '',
        yearOfPassing: education.year_of_passing || '',
        branchOfEngineering: education.branch_of_engineering || '',
        cgpa: education.cgpa || '',
        backlogs: '0', // These might not be parsed directly
        liveBacklogs: '0',
        internships: '', // These might need to be extracted from text
        programmingLanguages: parsedData.skills ? 
          parsedData.skills.filter(skill => 
            ['python', 'java', 'c++', 'javascript', 'c#', 'php', 'ruby', 'swift'].includes(skill.toLowerCase())
          ) : [],
        projects: '',
        skills: parsedData.skills || []
      });
    }
  }, [parsedData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSkillChange = (e) => {
    const skills = e.target.value.split(',').map(skill => skill.trim());
    setFormData({
      ...formData,
      skills
    });
  };

  const handleProgrammingLanguageChange = (e) => {
    const languages = e.target.value.split(',').map(lang => lang.trim());
    setFormData({
      ...formData,
      programmingLanguages: languages
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Review Parsed Resume</h2>
      <p className="text-gray-600 mb-4">
        Please review and correct the information extracted from your resume.
      </p>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Personal Information */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Phone</label>
            <input
              type="text"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          {/* Education Information */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Year of Passing</label>
            <input
              type="text"
              name="yearOfPassing"
              value={formData.yearOfPassing}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Branch of Engineering</label>
            <input
              type="text"
              name="branchOfEngineering"
              value={formData.branchOfEngineering}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">CGPA</label>
            <input
              type="text"
              name="cgpa"
              value={formData.cgpa}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          {/* Academic Details */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Number of Backlogs</label>
            <input
              type="number"
              name="backlogs"
              min="0"
              value={formData.backlogs}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Number of Live Backlogs</label>
            <input
              type="number"
              name="liveBacklogs"
              min="0"
              value={formData.liveBacklogs}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          
          {/* Professional Details */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Internships</label>
            <textarea
              name="internships"
              value={formData.internships}
              onChange={handleChange}
              rows="3"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Enter internship details (company, duration, role)"
            ></textarea>
          </div>
          
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Projects</label>
            <textarea
              name="projects"
              value={formData.projects}
              onChange={handleChange}
              rows="3"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Enter project details"
            ></textarea>
          </div>
          
          {/* Skills */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Programming Languages</label>
            <input
              type="text"
              value={formData.programmingLanguages.join(', ')}
              onChange={handleProgrammingLanguageChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Enter programming languages (separated by commas)"
            />
          </div>
          
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Skills</label>
            <input
              type="text"
              value={formData.skills.join(', ')}
              onChange={handleSkillChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Enter skills (separated by commas)"
            />
          </div>
        </div>
        
        {/* Form Actions */}
        <div className="flex justify-end space-x-3 mt-6">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Save Information
          </button>
        </div>
      </form>
    </div>
  );
};

export default ParsedResumeForm; 