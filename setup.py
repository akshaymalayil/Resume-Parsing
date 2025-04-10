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
import sys

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
    nltk.download('wordnet')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

    # Install SpaCy model
    logger.info("Installing SpaCy model...")
    try:
        import spacy
        if not spacy.util.is_package("en_core_web_sm"):
            logger.info("Downloading SpaCy English model...")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        else:
            logger.info("SpaCy English model already installed.")
    except Exception as e:
        logger.error(f"Error installing SpaCy model: {e}")
        logger.info("Please run: python -m spacy download en_core_web_sm")

if __name__ == "__main__":
    try:
        logger.info("Setting up environment for resume parser...")
        setup_environment()
        logger.info("Setup completed successfully!")
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1) 