


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
import json

app = FastAPI()
origins = ["*", 'http://localhost', 'http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

brt = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2',
    aws_access_key_id='AKIAR2KLF3NUTMHQCEVZ',
    aws_secret_access_key='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'
    
)

modelId = 'anthropic.claude-v2:1'
accept = 'application/json'
contentType = 'application/json'

@app.get("/bedrock/{prompt}")
def get_prompt(prompt: str):
    try:
        payload = {
            "body": json.dumps({
                "prompt": "\n\nHuman: {}\n\nAssistant:".format(prompt),
                "max_tokens_to_sample": 300,
                "temperature": 0.5,
                "top_k": 250,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"],
                "anthropic_version": "bedrock-2023-05-31"
            }),
            "modelId": modelId,
            "accept": accept,
            "contentType": contentType
        }

        print("Request Body:", payload['body'])

        response = brt.invoke_model(**payload)

        response_body = json.loads(response.get('body').read().decode('utf-8'))
        print("Response Body:", response_body)

        return {"completion": response_body.get("completion", "")}

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
