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
        """Extract education details"""
        education_info = {
            "year_of_passing": "",
            "branch_of_engineering": "",
            "cgpa": ""
        }
        
        # Look for year of passing
        year_pattern = r'(?:passing|pass|passed|graduate|graduation|batch|year).{1,20}(20\d\d)'
        year_matches = re.findall(year_pattern, text.lower())
        if year_matches:
            education_info["year_of_passing"] = year_matches[0]
        
        # Look for branch/degree
        engineering_branches = [
            "computer science", "cs", "cse", "information technology", "it",
            "electronics", "electrical", "ece", "eee", "mechanical", "mech",
            "civil", "chemical", "biotech", "biotechnology"
        ]
        
        # Convert text to lowercase and search for branches
        text_lower = text.lower()
        for branch in engineering_branches:
            if branch in text_lower:
                # Try to get the full branch name
                branch_pattern = r'(?:b\.?tech|bachelor|engineering|b\.?e).{1,20}(' + branch + r')'
                branch_matches = re.findall(branch_pattern, text_lower)
                if branch_matches:
                    education_info["branch_of_engineering"] = branch_matches[0].title()
                else:
                    education_info["branch_of_engineering"] = branch.title()
                break
        
        # Look for CGPA or percentage
        cgpa_pattern = r'(?:cgpa|gpa).{1,5}(\d+\.\d+)'
        percentage_pattern = r'(\d{2}(?:\.\d+)?)%'
        
        cgpa_matches = re.findall(cgpa_pattern, text.lower())
        percentage_matches = re.findall(percentage_pattern, text)
        
        if cgpa_matches:
            education_info["cgpa"] = cgpa_matches[0]
        elif percentage_matches:
            # Convert percentage to CGPA (rough approximation)
            percentage = float(percentage_matches[0])
            if percentage > 0:
                # Using a simple conversion where 100% = 10 CGPA
                cgpa = min(10.0, percentage / 10.0)
                education_info["cgpa"] = f"{cgpa:.2f}"
        
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
        """Extract programming languages and technical skills"""
        programming_languages = [
            "python", "java", "javascript", "js", "c++", "c#", "ruby", "php", "swift",
            "golang", "go", "kotlin", "typescript", "scala", "perl", "rust", "html",
            "css", "sql", "nosql", "r", "matlab", "shell", "bash", "powershell"
        ]
        
        # Convert text to lowercase and tokenize
        text_lower = text.lower()
        words = word_tokenize(text_lower)
        
        # Find programming languages
        found_languages = []
        for lang in programming_languages:
            if lang in text_lower:
                # Check if it's a standalone word or part of a phrase
                lang_pattern = r'\b' + re.escape(lang) + r'\b'
                if re.search(lang_pattern, text_lower):
                    found_languages.append(lang.title())
        
        return found_languages

    def extract_projects(self, text):
        """Extract project domains and information"""
        project_domains = []
        
        # Common project domains
        domains = [
            "web", "mobile", "desktop", "android", "ios", "machine learning", "ml",
            "artificial intelligence", "ai", "data science", "blockchain", "cloud",
            "aws", "azure", "devops", "security", "game", "iot", "embedded"
        ]
        
        text_lower = text.lower()
        
        # Look for project sections
        project_section = re.search(r'(?:projects?|work experience).+?(?:education|skills|achievements|certifications|languages)', 
                                 text_lower, re.DOTALL)
        
        if project_section:
            project_text = project_section.group(0)
            
            # Find domains in the project section
            for domain in domains:
                if domain in project_text:
                    project_domains.append(domain.title())
        else:
            # If no project section found, search the entire text
            for domain in domains:
                if domain in text_lower:
                    project_domains.append(domain.title())
        
        return list(set(project_domains))  # Remove duplicates

    def extract_internships(self, text):
        """Extract number of internships"""
        text_lower = text.lower()
        
        # Look for internship mentions
        internship_matches = re.findall(r'internship|intern', text_lower)
        
        # Count unique internship entries
        # This is a rough approximation - would need more sophisticated parsing for accuracy
        count = min(len(internship_matches), 10)  # Cap at 10 to avoid false positives
        
        return count

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
                "programming_languages": self.extract_skills(text),
                "project_domains": self.extract_projects(text),
                "internships": self.extract_internships(text),
                "backlogs": self.extract_backlogs(text)
            }
            
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise 