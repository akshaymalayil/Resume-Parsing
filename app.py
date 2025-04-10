from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from resume_parser import ResumeParser

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload/', methods=['POST'])
def parse_resume():
    # Check if a file was uploaded
    if 'resume' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['resume']
    
    # Check if the file has a valid name and extension
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'File type not allowed. Please upload a PDF, DOC, or DOCX file.'}), 400
    
    # Save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Parse the resume
        parser = ResumeParser(filepath)
        result = parser.parse()
        
        # Delete the file after parsing if needed
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 500
            
        # Format the response to match the frontend expectations
        formatted_result = {
            'name': result.get('name', ''),
            'email': result.get('email', ''),
            'phone': result.get('phone', ''),
            'skills': result.get('skills', []),
            'programming_languages': result.get('programming_languages', []),
            'education': {
                'year_of_passing': result.get('education', {}).get('year_of_passing', ''),
                'branch_of_engineering': result.get('education', {}).get('branch_of_engineering', ''),
                'cgpa': result.get('education', {}).get('cgpa', ''),
                'backlogs': result.get('education', {}).get('backlogs', '0'),
                'live_backlogs': result.get('education', {}).get('live_backlogs', '0')
            },
            'internships': result.get('internships', ''),
            'projects': result.get('projects', ''),
            'experience': result.get('experience', '0'),
            'location': result.get('location', 'Unknown')
        }
        
        return jsonify({
            'success': True,
            'message': 'Resume parsed successfully',
            'data': formatted_result
        })
    except Exception as e:
        # Delete the file in case of error
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/resumes/', methods=['GET'])
def get_resumes():
    # This would typically fetch from a database
    # For now, returning dummy data
    return jsonify([
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '123-456-7890',
            'skills': ['Python', 'Flask', 'React'],
            'experience': 2,
            'education': 'Bachelor of Computer Science',
            'location': 'New York',
            'uploaded_at': '2023-01-15T10:30:00Z'
        }
    ])

@app.route('/api/resumes/<int:resume_id>/download/', methods=['GET'])
def download_resume(resume_id):
    # This would typically fetch from a database and file system
    # Return a mock response for now
    return 'This would be the PDF file content', 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename=resume_{resume_id}.pdf'
    }

@app.route('/api/save-resume/', methods=['POST'])
def save_resume():
    # This would typically save the edited resume data to a database
    data = request.json
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    # Here you would save the data to your database
    # For now, we'll just return success
    return jsonify({
        'success': True,
        'message': 'Resume information saved successfully',
        'id': 1  # This would typically be the ID from your database
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 