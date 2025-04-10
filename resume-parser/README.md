# Resume Parser

This application uses AI and NLP techniques to extract information from resumes in PDF format and displays the data in an editable form for verification.

## Features

- Upload resume in PDF format (drag & drop supported)
- Extract information including:
  - Personal details (name, email, phone, gender)
  - Education information (year of passing, branch, CGPA)
  - Professional details (internships, projects)
  - Technical skills (programming languages)
  - Academic performance (backlogs)
- Editable form for verifying and correcting extracted information
- Responsive UI that works on mobile and desktop

## Technology Stack

### Backend
- Flask (Python web framework)
- PyPDF2 & pdfminer.six (PDF text extraction)
- spaCy & NLTK (Natural Language Processing)
- Regular expressions for pattern matching

### Frontend
- React (UI library)
- Tailwind CSS (styling)
- Axios (API requests)
- React Icons

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd resume-parser/backend
   ```

2. Create a virtual environment:
   ```
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the setup script to download NLP models:
   ```
   python setup.py
   ```

5. Start the Flask server:
   ```
   python app.py
   ```

The backend server will start at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd resume-parser/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

The frontend application will be available at http://localhost:3000

## Usage

1. Open the application in your browser
2. Upload your resume by dragging and dropping it onto the designated area or by clicking to select a file
3. Wait for the parsing process to complete
4. Review the extracted information in the form
5. Make any necessary corrections
6. Submit the form when done

## Limitations

- Currently only supports PDF format
- Maximum file size is 5MB
- Best results with standard resume formats
- May not extract all information accurately from highly stylized resumes
- English language resumes only

## Future Improvements

- Support for more file formats (DOCX, TXT)
- Improved accuracy with machine learning models
- Multi-language support
- Integration with job application systems
- Export functionality (JSON, CSV)

## License

MIT 