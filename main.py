from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Missing resume file or job description"}), 400

    resume_file = request.files['resume']
    job_desc = request.form['job_description']

    # Read resume text (simple plain-text read)
    resume_text = resume_file.read().decode(errors='ignore')

    # Call OpenAI API to tailor the resume
    prompt = f"""
You are a resume expert. Rewrite and tailor the following resume text to match the job description below.

Job Description:
{job_desc}

Original Resume:
{resume_text}

Tailored Resume:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )

        tailored_resume = response['choices'][0]['message']['content'].strip()
        match_score = 90  # dummy match score for now

        return jsonify({
            "match_score": match_score,
            "tailored_resume": tailored_resume
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
