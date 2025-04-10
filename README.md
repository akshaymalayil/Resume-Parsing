# Resume Parser Frontend

This is the frontend part of the Resume Parser application, built with React and styled with Tailwind CSS.

## Features

- Modern, responsive UI
- Resume upload with drag and drop functionality
- View parsed resume information
- Download parsed resumes

## Setup Instructions

1. Make sure you have Node.js (version 14 or newer) installed on your system
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file in the root directory with the following content:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```
4. Start the development server:
   ```
   npm start
   ```
5. The application will be available at http://localhost:3000

## Project Structure

- `public/` - Static assets and HTML template
- `src/` - Source code
  - `components/` - React components
    - `Home.js` - Landing page component
    - `Navbar.js` - Navigation bar component
    - `ResumeUpload.js` - Resume upload form component
    - `ResumeList.js` - List of parsed resumes component
  - `styles/` - CSS stylesheets
    - `index.css` - Global styles with Tailwind imports
    - `App.css` - Custom application styles
  - `App.js` - Main application component
  - `index.js` - Entry point

## Building for Production

To create a production build:

```
npm run build
```

This will generate optimized static files in the `build/` directory that can be served by any web server.

## Notes

- Make sure the backend server is running at http://localhost:5000 before using the application
- The frontend expects the backend API endpoints to be prefixed with `/api` 