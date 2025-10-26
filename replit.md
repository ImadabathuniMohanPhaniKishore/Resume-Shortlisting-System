# Intelligent Resume Shortlisting System

## Overview
A full-stack web application with user authentication that uses Natural Language Processing (NLP) and Machine Learning to automatically shortlist and rank resumes based on job descriptions. The system features secure user signup/login, analyzes resume content, extracts key information, and computes similarity scores using TF-IDF vectorization.

## Purpose
This application helps HR professionals and recruiters quickly identify the most relevant candidates by:
- Providing secure user authentication with signup and login
- Automatically parsing resume files (PDF and DOCX formats)
- Extracting candidate information (name, skills, experience)
- Computing similarity scores between resumes and job descriptions
- Ranking candidates by relevance
- Providing CSV export functionality for further processing
- Protecting user data with session-based authentication

## Technology Stack

### Backend
- **Flask** - Python web framework
- **Flask-Login** - User session management and authentication
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX file parsing
- **scikit-learn** - TF-IDF vectorization and similarity computation
- **NLTK** - Natural language processing and text preprocessing
- **pandas** - Data manipulation and CSV export
- **SQLite** - User database storage
- **Werkzeug** - Password hashing and security

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **Vanilla JavaScript** - Interactive functionality
- **Font Awesome** - Icons

## Project Structure
```
.
├── app.py                      # Main Flask application with auth routes
├── database.py                 # User model and SQLite database management
├── templates/
│   ├── index.html             # Main dashboard (protected)
│   ├── login.html             # User login page
│   └── signup.html            # User registration page
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── main.js            # Frontend JavaScript
├── uploads/                    # Temporary storage for uploaded resumes
├── sample_resumes/            # Sample resume files for testing
├── sample_job_description.txt # Sample job description
├── generate_samples.py        # Utility to generate sample resumes
└── users.db                   # SQLite database for user accounts (auto-created)
```

## Features

### Core Functionality
1. **User Authentication**: Secure signup and login with password hashing
2. **Session Management**: Flask-Login for persistent user sessions with "remember me" option
3. **Access Control**: Protected routes requiring authentication
4. **Multi-file Upload**: Supports uploading multiple resumes simultaneously (PDF and DOCX formats only)
5. **Drag-and-Drop Interface**: User-friendly file upload with drag-and-drop support
6. **NLP-Powered Matching**: Uses TF-IDF and cosine similarity for accurate matching
7. **Information Extraction**: Automatically extracts candidate name, skills, and experience
8. **Ranked Results**: Displays candidates sorted by relevance score
9. **CSV Export**: Download shortlisted candidates as a CSV file
10. **Responsive Design**: Mobile-friendly interface with Bootstrap

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

### Getting Started
1. **Create an Account**: Navigate to the signup page and register with your name, email, and password (minimum 8 characters)
2. **Login**: Use your credentials to log in (check "Remember Me" to stay logged in)
3. **Access Dashboard**: After login, you'll see the resume upload interface

### Testing with Sample Data
1. Log in to your account
2. Use the sample resumes located in `sample_resumes/` folder
3. Copy the job description from `sample_job_description.txt`
4. Upload the sample resumes through the web interface
5. Paste the job description into the text area
6. Click "Shortlist Resumes" to see results
7. Export results as CSV if needed
8. Logout when finished using the button in the navigation bar

### Expected Results
The sample resumes are designed to test different matching scenarios:
- **David Kim** & **John Smith**: High match (Python, Flask, AWS, ML skills)
- **Michael Chen**: Good match (Python, NLP, Data Science)
- **Sarah Johnson**: Medium match (JavaScript, React, but different backend)
- **Lisa Anderson**: Lower match (Java/Spring vs Python/Flask)
- **Emily Rodriguez**: Lower match (UI/UX focus)

## Recent Changes
- **October 26, 2025**: Initial project creation and authentication enhancement
  - Built Flask backend with resume parsing and NLP matching
  - Created responsive Bootstrap frontend
  - Added drag-and-drop file upload functionality
  - Implemented TF-IDF-based similarity scoring
  - Added CSV export feature
  - Generated 6 sample resumes for testing
  - Fixed file format support: Removed legacy .doc support to prevent parsing failures (only PDF and DOCX are supported)
  - **Added User Authentication System**:
    - Implemented Flask-Login for session management
    - Created SQLite database for user storage
    - Built signup page with email/password validation
    - Built login page with "remember me" functionality
    - Added password hashing with Werkzeug for security
    - Protected resume upload routes with @login_required
    - Added navigation bar with user info and logout button
    - Fixed database locking bug in user creation

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
- **Authentication**:
  - Passwords hashed using Werkzeug's secure password hashing
  - Flask-Login session management with secure cookies
  - Email validation and duplicate prevention
  - Password strength requirements (minimum 8 characters)
  - Protected routes with @login_required decorator
- **File Handling**:
  - File type validation (only PDF and DOCX allowed)
  - Secure filename handling with Werkzeug
  - File size limits (16MB max)
  - Temporary files are deleted after processing
- **Session Management**:
  - Session secret uses environment variable
  - Optional "remember me" with secure cookies

## Future Enhancements
- Analytics dashboard with processing statistics and top skills trends
- User profile management (change password, update info)
- Password reset functionality via email
- Admin panel for user management
- Resume upload history per user
- Advanced NLP with spaCy for better entity extraction
- Support for additional file formats (RTF, TXT)
- Batch processing improvements and job queue
- Resume comparison view to see side-by-side candidate profiles
- Custom skill taxonomy configuration
- Team/organization features for collaborative hiring
