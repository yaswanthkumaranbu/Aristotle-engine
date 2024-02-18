import html
import os
import flask
import base64
from datetime import date
import googleapiclient.discovery
from googleapiclient.discovery import build
from transformers import BartForConditionalGeneration, BartTokenizer, pipeline
import torch
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from flask_cors import cross_origin

import pytz 
from flask_cors import CORS


app = flask.Flask(__name__)


CORS(app,support_credentials=True,origins="*")

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased')



def parse_sender_info(from_header):
    # Parse the 'From' header to extract sender's name and email
    # Assuming the format is "Sender Name <sender@example.com>"
    start_index = from_header.find('<')
    end_index = from_header.find('>')

    if start_index != -1 and end_index != -1:
        sender_name = from_header[:start_index].strip()
        sender_email = from_header[start_index + 1:end_index].strip()
    else:
        # If the format is not as expected, use the entire 'From' header as the email
        sender_name = ''
        sender_email = from_header.strip()

    return sender_name, sender_email
@app.route('/getGmail',methods=['POST'])
def getGmail():
    print("hi")
    messages = request.json.get('data')
    summaries = []

    # Initialize formatted_text with a default value
    formatted_text = None

    for msg in messages:
        if len(summaries)>9:
            break
        labels = msg['individualMessageData']['labelIds']
        subject = next((header['value'] for header in msg['individualMessageData']['payload']['headers'] if header['name'].lower() == 'subject'), '')
        from_header = next((header['value'] for header in msg['individualMessageData']['payload']['headers'] if header['name'].lower() == 'from'), '')

    # Parse the 'From' header to extract sender's name and email
        sender_name, sender_email = parse_sender_info(from_header)
        SenderName = sender_name.replace('"','')
        body = " "  # Initialize body variable
        date_header = next((header['value'] for header in msg['individualMessageData']['payload']['headers'] if header['name'].lower() == 'date'), '')
        date_header = date_header.replace('(UTC)', '').strip()   
        date_header = date_header.replace('(IST)', '').strip()          
        original_datetime = datetime.strptime(date_header, "%a, %d %b %Y %H:%M:%S %z")
        formatted_date = original_datetime.strftime("%b %d")
        print(formatted_date)
        
        if 'INBOX' in labels:
            if 'multipart' in msg['individualMessageData']['payload']['mimeType'].lower():
                for part in msg['individualMessageData']['payload']['parts']:
                    if part['mimeType'].lower() == 'text/plain':
                        body = base64.urlsafe_b64decode(part['body']['data']).decode()

                        print('- Subject:', subject)
                       
                        print('- Body:', body)

                        print('-----------------------------')

            else:
                
                body = base64.urlsafe_b64decode(part['body']['data']).decode()
                print('- Subject:', subject)
            
                print('- Body:', body)
                print('-----------------------------')

        # Move the following code inside the loop
        formatted_text = body.replace(r'\n', '\n').replace(r'\r', '\r').replace(r'\r\n', '\n') 
        formatted_text = html.unescape(formatted_text)

        if formatted_text:
            word_count = len(formatted_text.split())
            if word_count < 10:
                summary = body
            else:
                if word_count < 50:
                    summary = generate_summary(formatted_text, max_length=20)
                else:
                    summary = generate_summary(formatted_text, max_length=50)

            sentiment_result = sentiment_analyzer(summary)
            label = sentiment_result[0]['label']
            score = sentiment_result[0]['score']
            if sender_name=="":
                sender_name ="Unknown"
            if score >= 0.7:
                email_label = "Important"
            elif score >= 0.4:
                email_label = "Least Important"
            else:
                email_label = "Not Important"

            email_info = {
                'From': SenderName,
                'From email':sender_email,
                'Email Subject': subject,
                'Generated Summary': summary,
                'Sentiment Label': email_label,
                'Sentiment Score': score,
                'Date': "Nov 28"
            }
            summaries.append(email_info)
    return jsonify(summaries)


def generate_summary(email_text, max_length=20):
    inputs = tokenizer([email_text], return_tensors='pt', max_length=1024, truncation=True)

    with torch.no_grad():
        try:
            summary_ids = model.generate(**inputs, max_length=max_length)
        except ValueError:
            # Handle cases where min_length is greater than max_length
            summary_ids = model.generate(**inputs, max_length=max_length, min_length=20)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


if __name__ == '__main__':

  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  app.run('localhost', 8080, debug=False)
