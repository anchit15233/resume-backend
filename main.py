from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Missing resume file or job description"}), 400

    resume_file = request.files['resume']
    job_desc = request.form['job_description']

    match_score = 85
    tailored_resume = f"Tailored resume for job:\n{job_desc}\n\nFilename: {resume_file.filename}"

    return jsonify({
        "match_score": match_score,
        "tailored_resume": tailored_resume
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
