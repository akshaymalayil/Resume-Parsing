#!/usr/bin/env python
"""
Setup script for the resume parser
- Downloads required NLTK data
- Installs SpaCy models
- Creates necessary directories
"""
import os
import nltk
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_environment():
    # Create uploads directory
    logger.info("Creating uploads directory...")
    os.makedirs('uploads', exist_ok=True)
    
    # Download NLTK data
    logger.info("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    
    # Install SpaCy model
    logger.info("Installing SpaCy model...")
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            logger.info("SpaCy model already installed.")
        except OSError:
            logger.info("Downloading SpaCy model...")
            subprocess.check_call(["python", "-m", "spacy", "download", "en_core_web_sm"])
    except ImportError:
        logger.error("SpaCy not installed. Please install requirements first.")
    
    logger.info("Setup complete!")

if __name__ == "__main__":
    logger.info("Starting setup...")
    setup_environment() 