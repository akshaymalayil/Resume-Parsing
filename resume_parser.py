import PyPDF2
import re
import os
import nltk
from nltk.tokenize import word_tokenize
import string
import spacy
from pdfminer.high_level import extract_text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.info("Downloading SpaCy model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    def __init__(self, resume_path):
        self.resume_path = resume_path
        
    def extract_text_from_pdf(self):
        """Extract text from PDF file using multiple methods for better coverage"""
        # First try with pdfminer for better text extraction
        try:
            text = extract_text(self.resume_path)
            if text.strip():
                return text
        except Exception as e:
            logger.warning(f"pdfminer extraction failed: {str(e)}")
        
        # Fallback to PyPDF2
        try:
            text = ""
            with open(self.resume_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"PDF text extraction failed: {str(e)}")
            raise Exception("Could not extract text from the PDF. The file might be corrupted or password protected.")

    def extract_name(self, text):
        """Extract candidate name from resume"""
        # Use NLP to identify person names
        doc = nlp(text[:1000])  # Process first 1000 chars for efficiency
        names = []
        
        # Find all person named entities
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                names.append(ent.text)
        
        # Most likely the first person name is the candidate's name
        if names:
            return names[0]
        
        return ""

    def extract_email(self, text):
        """Extract email addresses from text"""
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""

    def extract_phone(self, text):
        """Extract phone numbers from text"""
        # Pattern for Indian phone numbers
        phone_pattern = r'(?:\+?(?:91)?[-\s]?)?(?:\d{10}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4})'
        phones = re.findall(phone_pattern, text)
        
        # Clean up the extracted phone
        if phones:
            phone = phones[0]
            # Remove any non-digit characters except for the '+' at the beginning
            clean_phone = re.sub(r'[^\d+]', '', phone)
            # Ensure it starts with country code if not already
            if not clean_phone.startswith('+'):
                if clean_phone.startswith('91'):
                    clean_phone = '+' + clean_phone
                else:
                    clean_phone = '+91' + clean_phone
            return clean_phone
        
        return ""

    def extract_education(self, text):
        """Extract education details including year of passing, branch, and CGPA"""
        education_info = {
            "year_of_passing": "",
            "branch_of_engineering": "",
            "cgpa": "",
            "backlogs": "0",
            "live_backlogs": "0"
        }
        
        # Look for year of passing
        year_pattern = r'(?:passing|pass|passed|graduate|graduation|batch|year).{1,20}(20\d\d)'
        year_matches = re.findall(year_pattern, text.lower())
        if year_matches:
            education_info["year_of_passing"] = year_matches[0]
        else:
            # Try a more general pattern for years
            year_pattern = r'(?:20\d\d)(?:\s*-\s*20\d\d)?'
            year_matches = re.findall(year_pattern, text)
            if year_matches:
                education_info["year_of_passing"] = year_matches[0].split('-')[-1].strip()
        
        # Look for branch/degree
        engineering_branches = [
            "computer science", "cs", "cse", "information technology", "it",
            "electronics", "electrical", "ece", "eee", "mechanical", "mech",
            "civil", "chemical", "biotech", "biotechnology", "ai", "artificial intelligence",
            "machine learning", "data science", "aerospace", "mining"
        ]
        
        # Convert text to lowercase and search for branches
        text_lower = text.lower()
        for branch in engineering_branches:
            if branch in text_lower:
                education_info["branch_of_engineering"] = branch
                break
        
        # Look for CGPA/percentage
        cgpa_pattern = r'(?:cgpa|gpa).{1,5}(\d+\.\d+|\d+)'
        percentage_pattern = r'(?:percentage|percent|\%).{1,5}(\d+\.\d+|\d+)'
        
        cgpa_matches = re.findall(cgpa_pattern, text_lower)
        if cgpa_matches:
            education_info["cgpa"] = cgpa_matches[0]
        else:
            percentage_matches = re.findall(percentage_pattern, text_lower)
            if percentage_matches:
                education_info["cgpa"] = percentage_matches[0] + "%"
        
        # Look for backlogs
        backlog_pattern = r'(?:backlog|back).{1,10}(\d+)'
        backlog_matches = re.findall(backlog_pattern, text_lower)
        if backlog_matches:
            education_info["backlogs"] = backlog_matches[0]
        
        # Look for live backlogs
        live_backlog_pattern = r'(?:live\s+backlog|active\s+backlog|current\s+backlog).{1,10}(\d+)'
        live_backlog_matches = re.findall(live_backlog_pattern, text_lower)
        if live_backlog_matches:
            education_info["live_backlogs"] = live_backlog_matches[0]
        
        return education_info

    def extract_gender(self, text):
        """Extract gender information"""
        text_lower = text.lower()
        male_pattern = r'\b(?:male|m)\b'
        female_pattern = r'\b(?:female|f)\b'
        
        if re.search(male_pattern, text_lower):
            return "Male"
        elif re.search(female_pattern, text_lower):
            return "Female"
        
        # Try to infer from pronouns (not very accurate)
        he_count = len(re.findall(r'\bhe\b|\bhim\b|\bhis\b', text_lower))
        she_count = len(re.findall(r'\bshe\b|\bher\b|\bhers\b', text_lower))
        
        if he_count > she_count:
            return "Male"
        elif she_count > he_count:
            return "Female"
        
        return ""

    def extract_skills(self, text):
        """Extract skills from resume"""
        # Common programming languages, frameworks, tools
        skills_list = [
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift",
            "typescript", "kotlin", "go", "rust", "scala", "perl", "r", "matlab",
            "react", "angular", "vue", "node.js", "express", "django", "flask",
            "spring", "hibernate", "laravel", "asp.net", "rails",
            "mysql", "postgresql", "mongodb", "oracle", "sql server", "sqlite",
            "redis", "cassandra", "elasticsearch", "aws", "azure", "gcp",
            "docker", "kubernetes", "jenkins", "gitlab", "github", "terraform",
            "ansible", "hadoop", "spark", "kafka", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "tableau", "power bi", "excel",
            "html", "css", "sass", "less", "bootstrap", "jquery", "rest api",
            "graphql", "git", "svn", "linux", "unix", "bash", "powershell",
            "agile", "scrum", "kanban", "jira", "confluence"
        ]
        
        # Find matches in text (case insensitive)
        text_lower = text.lower()
        found_skills = []
        
        for skill in skills_list:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill)
        
        return found_skills

    def extract_programming_languages(self, text):
        """Extract programming languages from resume"""
        languages = [
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift",
            "typescript", "kotlin", "go", "rust", "scala", "perl", "r", "matlab",
            "html", "css", "sql", "bash", "powershell", "c", "objective-c", "assembly",
            "cobol", "fortran", "haskell", "dart", "lua", "groovy", "vba",
            "abap", "pascal", "pl/sql", "ada", "d", "f#", "julia", "clojure"
        ]
        
        text_lower = text.lower()
        found_languages = []
        
        for lang in languages:
            if re.search(r'\b' + re.escape(lang) + r'\b', text_lower):
                found_languages.append(lang)
                
        return found_languages

    def extract_projects(self, text):
        """Extract project information from resume"""
        # Look for project sections
        project_section_pattern = r'(?:projects|project work|academic projects).{0,1000}'
        project_sections = re.findall(project_section_pattern, text.lower(), re.IGNORECASE | re.DOTALL)
        
        # Join all found sections
        project_text = ' '.join(project_sections)
        
        # If project text is too short, try looking for specific project indicators
        if len(project_text) < 50:
            project_patterns = [
                r'project(?:\s+title)?:\s*.{1,100}',
                r'developed\s+a\s+.{1,100}',
                r'implemented\s+a\s+.{1,100}',
                r'created\s+a\s+.{1,100}'
            ]
            
            extracted_projects = []
            for pattern in project_patterns:
                project_matches = re.findall(pattern, text.lower(), re.IGNORECASE)
                extracted_projects.extend(project_matches)
            
            project_text = ' '.join(extracted_projects)
        
        # Clean up the text
        project_text = project_text.strip()
        
        return project_text if project_text else ""

    def extract_internships(self, text):
        """Extract internship information from resume"""
        # Look for sections related to internships
        internship_section_pattern = r'(?:internship|internships|work experience|professional experience).{0,500}'
        internship_sections = re.findall(internship_section_pattern, text.lower(), re.IGNORECASE | re.DOTALL)
        
        # Join all found sections
        internship_text = ' '.join(internship_sections)
        
        # If internship text is too short, try a broader search
        if len(internship_text) < 50:
            company_pattern = r'(?:intern(?:ship)?(?:\sat)?|worked at).{1,50}(?:company|organization|firm|corporation|inc|ltd)?'
            company_mentions = re.findall(company_pattern, text.lower(), re.IGNORECASE)
            internship_text = ' '.join(company_mentions)
        
        # Clean up the text a bit
        internship_text = internship_text.strip()
        
        return internship_text if internship_text else ""

    def extract_backlogs(self, text):
        """Extract backlog information"""
        backlogs = {
            "total": 0,
            "live": 0
        }
        
        text_lower = text.lower()
        
        # Look for backlog mentions
        backlog_pattern = r'(\d+)\s*(?:backlog|arrear)'
        live_backlog_pattern = r'(\d+)\s*(?:live|current|active|pending)\s*(?:backlog|arrear)'
        
        backlog_matches = re.findall(backlog_pattern, text_lower)
        live_backlog_matches = re.findall(live_backlog_pattern, text_lower)
        
        if backlog_matches:
            backlogs["total"] = int(backlog_matches[0])
        
        if live_backlog_matches:
            backlogs["live"] = int(live_backlog_matches[0])
        
        return backlogs

    def parse(self):
        """Main method to parse resume and extract all information"""
        try:
            text = self.extract_text_from_pdf()
            
            # Extract all required information
            parsed_data = {
                "name": self.extract_name(text),
                "email": self.extract_email(text),
                "phone": self.extract_phone(text),
                "gender": self.extract_gender(text),
                "education": self.extract_education(text),
                "skills": self.extract_skills(text),
                "programming_languages": self.extract_programming_languages(text),
                "projects": self.extract_projects(text),
                "internships": self.extract_internships(text),
                "backlogs": self.extract_backlogs(text)
            }
            
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise 