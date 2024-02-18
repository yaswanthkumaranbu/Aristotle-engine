from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
import json
from config import SECRET_KEY, ACCESS_KEY
app = FastAPI()
origins = ["*",
           'http://localhost',
           'http://localhost:8000']



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
#modelId = 'ai21.j2-mid-v1'
modelId = 'anthropic.claude-v2:1'
accept = 'application/json'
contentType = 'application/json'


@app.get("/bedrock/{prompt}")
def get_prompt(prompt: str):
    body = json.dumps({
    "prompt": "\n\nHuman: {}\n\nAssistant:".format(prompt),
    "max_tokens_to_sample": 300,
    "temperature": 0.5,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": [
      "\n\nHuman:"
    ],
    "anthropic_version": "bedrock-2023-05-31"
    })

    response = brt.invoke_model(
        body=body,
        modelId=modelId,
        accept=accept,
        contentType=contentType
    )
    response_body = json.loads(response.get('body').read())
    return response_body
