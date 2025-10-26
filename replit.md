# Intelligent Resume Shortlisting System

## Overview
A full-stack web application that uses Natural Language Processing (NLP) and Machine Learning to automatically shortlist and rank resumes based on job descriptions. The system analyzes resume content, extracts key information, and computes similarity scores using TF-IDF vectorization.

## Purpose
This application helps HR professionals and recruiters quickly identify the most relevant candidates by:
- Automatically parsing resume files (PDF and DOCX formats)
- Extracting candidate information (name, skills, experience)
- Computing similarity scores between resumes and job descriptions
- Ranking candidates by relevance
- Providing CSV export functionality for further processing

## Technology Stack

### Backend
- **Flask** - Python web framework
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX file parsing
- **scikit-learn** - TF-IDF vectorization and similarity computation
- **NLTK** - Natural language processing and text preprocessing
- **pandas** - Data manipulation and CSV export

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **Vanilla JavaScript** - Interactive functionality
- **Font Awesome** - Icons

## Project Structure
```
.
├── app.py                      # Main Flask application
├── templates/
│   └── index.html             # Frontend template
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── main.js            # Frontend JavaScript
├── uploads/                    # Temporary storage for uploaded resumes
├── sample_resumes/            # Sample resume files for testing
├── sample_job_description.txt # Sample job description
└── generate_samples.py        # Utility to generate sample resumes
```

## Features

### Core Functionality
1. **Multi-file Upload**: Supports uploading multiple resumes simultaneously (PDF and DOCX formats only)
2. **Drag-and-Drop Interface**: User-friendly file upload with drag-and-drop support
3. **NLP-Powered Matching**: Uses TF-IDF and cosine similarity for accurate matching
4. **Information Extraction**: Automatically extracts candidate name, skills, and experience
5. **Ranked Results**: Displays candidates sorted by relevance score
6. **CSV Export**: Download shortlisted candidates as a CSV file
7. **Responsive Design**: Mobile-friendly interface with Bootstrap

### Technical Features
- Text preprocessing with NLTK (tokenization, stopword removal)
- TF-IDF vectorization with n-gram support (1-2 grams)
- Cosine similarity scoring
- Secure file handling with Werkzeug
- Real-time progress indicators
- File validation and error handling
- Supported file formats: PDF (via PyPDF2) and DOCX (via python-docx)

## How to Use

### Running the Application
The Flask server runs on port 5000. Access the application at the provided URL.

### Testing with Sample Data
1. Use the sample resumes located in `sample_resumes/` folder
2. Copy the job description from `sample_job_description.txt`
3. Upload the sample resumes through the web interface
4. Paste the job description into the text area
5. Click "Shortlist Resumes" to see results

### Expected Results
The sample resumes are designed to test different matching scenarios:
- **David Kim** & **John Smith**: High match (Python, Flask, AWS, ML skills)
- **Michael Chen**: Good match (Python, NLP, Data Science)
- **Sarah Johnson**: Medium match (JavaScript, React, but different backend)
- **Lisa Anderson**: Lower match (Java/Spring vs Python/Flask)
- **Emily Rodriguez**: Lower match (UI/UX focus)

## Recent Changes
- **October 26, 2025**: Initial project creation
  - Built Flask backend with resume parsing and NLP matching
  - Created responsive Bootstrap frontend
  - Added drag-and-drop file upload functionality
  - Implemented TF-IDF-based similarity scoring
  - Added CSV export feature
  - Generated 6 sample resumes for testing
  - Fixed file format support: Removed legacy .doc support to prevent parsing failures (only PDF and DOCX are supported)

## Architecture Notes

### NLP Pipeline
1. **Text Extraction**: PyPDF2/python-docx extract raw text from files
2. **Preprocessing**: Convert to lowercase, remove special characters, normalize whitespace
3. **Vectorization**: TF-IDF with 500 max features and 1-2 word n-grams
4. **Similarity**: Cosine similarity between job description and resume vectors
5. **Ranking**: Sort candidates by similarity score (0-100%)

### Information Extraction
- **Name**: Extracted from first few lines using heuristics (capitalized words)
- **Skills**: Pattern matching against common technical skills database
- **Experience**: Regex patterns to find years of experience mentions

## Security Considerations
- File type validation (only PDF and DOCX allowed)
- Secure filename handling with Werkzeug
- File size limits (16MB max)
- Temporary files are deleted after processing
- Session secret uses environment variable

## Future Enhancements
- SQLite database for storing upload history and results
- User authentication for HR users
- Analytics dashboard with processing statistics
- Advanced NLP with spaCy for better entity extraction
- Support for additional file formats
- Batch processing improvements
- Resume comparison view
- Custom skill taxonomy configuration
