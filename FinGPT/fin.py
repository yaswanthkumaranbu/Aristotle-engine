# app.py
from flask import Flask, request, jsonify
import requests
import PyPDF2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask application



API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def read_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

def answer_question(question, context):
    output = query({
        "inputs": {
            "question": question,
            "context": context
        }
    })
    return output

def get_answer_text(pdf_text, start, end):
    return pdf_text[start:end]

@app.route('/api/answer', methods=['POST'])
def handle_question():
    data = request.get_json()
    print("Received data:", data)
    question = data['question']
    pdf_file = 'ifrs-16-leases.pdf'
    pdf_text = read_pdf(pdf_file)
    output = answer_question(question, pdf_text)
    
    print("Response from Hugging Face API:", output)
    
    # Check if 'start' and 'end' keys exist in the output
    if 'start' in output and 'end' in output:
        answer_text = get_answer_text(pdf_text, output['start'], output['end'])
        print("Answer text:", answer_text)
        return jsonify({'answer': answer_text})
    else:
        return jsonify({'error': 'Answer not found'}), 500


if __name__ == '__main__':
    app.run(debug=True)