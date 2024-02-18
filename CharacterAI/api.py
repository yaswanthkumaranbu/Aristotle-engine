import boto3
import json

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2',
    aws_access_key_id= 'AKIAR2KLF3NUTMHQCEVZ',
    aws_secret_access_key='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'
)


input_data = {
  "modelId": "anthropic.claude-v2:1",
  "contentType": "application/json",
  "accept": "*/*",
  "body": {
    "prompt": "\n\nHuman: who is narendra modi\n\nAssistant:",
    "max_tokens_to_sample": 300,
    "temperature": 0.5,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": [
      "\n\nHuman:"
    ],
    "anthropic_version": "bedrock-2023-05-31"
  }
}

try:
    response = bedrock.invoke_model(
        body=json.dumps(input_data["body"]),
        modelId=input_data["modelId"],
        accept=input_data["accept"],
        contentType=input_data["contentType"]
    )

    response_body = json.loads(response['body'].read())

    # Print the response from the model
    print(response_body)

except Exception as e:
    print(f"Error invoking model: {e}")
