let selectedFiles = [];
let resultsData = [];

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('resumeFiles');
const fileList = document.getElementById('fileList');
const uploadForm = document.getElementById('uploadForm');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const uploadSection = document.getElementById('uploadSection');
const resultsBody = document.getElementById('resultsBody');
const exportBtn = document.getElementById('exportBtn');
const newSearchBtn = document.getElementById('newSearchBtn');

uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
});

fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
});

function handleFiles(files) {
    const validFiles = files.filter(file => {
        const ext = file.name.split('.').pop().toLowerCase();
        return ['pdf', 'docx', 'doc'].includes(ext);
    });

    if (validFiles.length === 0) {
        alert('Please select valid resume files (PDF or DOCX)');
        return;
    }

    selectedFiles = [...selectedFiles, ...validFiles];
    displayFileList();
}

function displayFileList() {
    if (selectedFiles.length === 0) {
        fileList.innerHTML = '';
        return;
    }

    fileList.innerHTML = '<div class="mb-2"><strong>Selected Files:</strong></div>';
    
    selectedFiles.forEach((file, index) => {
        const fileSize = (file.size / 1024).toFixed(2);
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div>
                <i class="fas fa-file-pdf text-danger me-2"></i>
                <span class="file-name">${file.name}</span>
                <span class="file-size">(${fileSize} KB)</span>
            </div>
            <i class="fas fa-times-circle remove-file" onclick="removeFile(${index})"></i>
        `;
        fileList.appendChild(fileItem);
    });
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFileList();
    
    const dt = new DataTransfer();
    selectedFiles.forEach(file => dt.items.add(file));
    fileInput.files = dt.files;
}

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (selectedFiles.length === 0) {
        alert('Please upload at least one resume');
        return;
    }

    const jobDescription = document.getElementById('jobDescription').value.trim();
    if (!jobDescription) {
        alert('Please enter a job description');
        return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('resumes', file);
    });
    formData.append('job_description', jobDescription);

    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            resultsData = data.results;
            displayResults(data.results);
        } else {
            alert(data.error || 'Error processing resumes');
            uploadSection.style.display = 'block';
            loadingSection.style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing resumes');
        uploadSection.style.display = 'block';
        loadingSection.style.display = 'none';
    }
});

function displayResults(results) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    resultsBody.innerHTML = '';

    results.forEach((result, index) => {
        const row = document.createElement('tr');
        
        let rankClass = 'rank-other';
        if (result.rank === 1) rankClass = 'rank-1';
        else if (result.rank === 2) rankClass = 'rank-2';
        else if (result.rank === 3) rankClass = 'rank-3';

        let scoreClass = 'score-low';
        if (result.score >= 70) scoreClass = 'score-high';
        else if (result.score >= 40) scoreClass = 'score-medium';

        const skillsHtml = result.skills && result.skills.length > 0
            ? result.skills.slice(0, 5).map(skill => 
                `<span class="skill-tag">${skill}</span>`
              ).join('')
            : '<span class="text-muted">N/A</span>';

        const experienceText = result.experience 
            ? `${result.experience} years` 
            : '<span class="text-muted">N/A</span>';

        row.innerHTML = `
            <td class="text-center">
                <span class="rank-badge ${rankClass}">${result.rank}</span>
            </td>
            <td>
                <strong>${result.name}</strong>
            </td>
            <td>
                <small class="text-muted">
                    <i class="fas fa-file me-1"></i>${result.filename}
                </small>
            </td>
            <td class="text-center">
                <span class="score-badge ${scoreClass}">
                    ${result.score}%
                </span>
            </td>
            <td>${skillsHtml}</td>
            <td class="text-center">${experienceText}</td>
        `;

        resultsBody.appendChild(row);
    });

    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

exportBtn.addEventListener('click', async () => {
    if (resultsData.length === 0) {
        alert('No results to export');
        return;
    }

    try {
        const response = await fetch('/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ results: resultsData })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'shortlisted_candidates.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } else {
            alert('Error exporting results');
        }
    } catch (error) {
        console.error('Export error:', error);
        alert('Error exporting results');
    }
});

newSearchBtn.addEventListener('click', () => {
    selectedFiles = [];
    resultsData = [];
    uploadForm.reset();
    fileList.innerHTML = '';
    resultsSection.style.display = 'none';
    uploadSection.style.display = 'block';
    uploadSection.scrollIntoView({ behavior: 'smooth' });
});
