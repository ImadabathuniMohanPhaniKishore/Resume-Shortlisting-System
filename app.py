import os
import re
import io
import csv
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'doc'}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
        return ''

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX {file_path}: {str(e)}")
        return ''

def extract_text(file_path, filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['docx', 'doc']:
        return extract_text_from_docx(file_path)
    return ''

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line) > 2 and len(line.split()) <= 4:
            if not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum', 'phone', 'email', 'address']):
                words = line.split()
                if all(word[0].isupper() for word in words if word):
                    return line
    return "Unknown Candidate"

def extract_skills(text):
    common_skills = [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express',
        'html', 'css', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
        'machine learning', 'deep learning', 'nlp', 'data science', 'tensorflow', 'pytorch',
        'agile', 'scrum', 'rest api', 'microservices', 'devops', 'linux', 'unix',
        'excel', 'powerpoint', 'word', 'tableau', 'power bi', 'jira', 'confluence'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))[:10]

def extract_experience_years(text):
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
        r'experience\s*:?\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?\s*in\s*\w+'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            try:
                return int(matches[0])
            except:
                pass
    
    return None

def calculate_similarity(job_description, resume_texts):
    documents = [job_description] + resume_texts
    
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        stop_words='english'
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        job_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(job_vector, resume_vectors)[0]
        
        return similarities
    except Exception as e:
        logger.error(f"Error calculating similarity: {str(e)}")
        return [0.0] * len(resume_texts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resumes():
    try:
        if 'resumes' not in request.files:
            return jsonify({'error': 'No resume files uploaded'}), 400
        
        files = request.files.getlist('resumes')
        job_description = request.form.get('job_description', '').strip()
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files selected'}), 400
        
        results = []
        resume_texts = []
        resume_data = []
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                text = extract_text(file_path, filename)
                
                if text.strip():
                    resume_texts.append(preprocess_text(text))
                    resume_data.append({
                        'filename': filename,
                        'original_text': text,
                        'name': extract_name(text),
                        'skills': extract_skills(text),
                        'experience': extract_experience_years(text)
                    })
                
                try:
                    os.remove(file_path)
                except:
                    pass
        
        if not resume_texts:
            return jsonify({'error': 'No valid text extracted from resumes'}), 400
        
        similarities = calculate_similarity(job_description, resume_texts)
        
        for i, data in enumerate(resume_data):
            score = float(similarities[i]) * 100
            results.append({
                'name': data['name'],
                'filename': data['filename'],
                'score': round(score, 2),
                'skills': data['skills'],
                'experience': data['experience'],
                'match_percentage': round(score, 1)
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        for idx, result in enumerate(results, 1):
            result['rank'] = idx
        
        return jsonify({
            'success': True,
            'results': results,
            'total_resumes': len(results)
        })
    
    except Exception as e:
        logger.error(f"Error processing resumes: {str(e)}")
        return jsonify({'error': f'Error processing resumes: {str(e)}'}), 500

@app.route('/export', methods=['POST'])
def export_results():
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'No results to export'}), 400
        
        output = io.StringIO()
        fieldnames = ['Rank', 'Name', 'Filename', 'Match Score (%)', 'Skills', 'Experience (Years)']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Rank': result.get('rank', ''),
                'Name': result.get('name', ''),
                'Filename': result.get('filename', ''),
                'Match Score (%)': result.get('score', 0),
                'Skills': ', '.join(result.get('skills', [])),
                'Experience (Years)': result.get('experience', 'N/A') if result.get('experience') else 'N/A'
            })
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='shortlisted_candidates.csv'
        )
    
    except Exception as e:
        logger.error(f"Error exporting results: {str(e)}")
        return jsonify({'error': f'Error exporting results: {str(e)}'}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=False)
