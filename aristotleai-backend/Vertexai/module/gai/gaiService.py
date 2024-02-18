
from google.oauth2.service_account import Credentials
from  google.auth.transport.requests import Request

# Path to API key file
key_path=".\module\gai\key.json"
credentials = Credentials.from_service_account_file(
    key_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'])


if credentials.expired:
    credentials.refresh(Request())

# project and data credentials
PROJECT_ID = 'elite-name-414210'
REGION = 'us-central1'
location="global"

#Configure/ Authenticate Vertex Ai with the service account api key
import vertexai
vertexai.init(project = PROJECT_ID, location = REGION, credentials = credentials)


from vertexai.language_models import TextGenerationModel, GroundingSource
# Configure the model parameters

# Select the model
model = TextGenerationModel.from_pretrained("text-bison")

class GaiService:
    # @handle_function_errors
    def test_fun(self, request):
        return ''

    def chat_with_gai(_self,prompt, session_tokens=None):
        # prompt = """
        # tell me a motivation story
        # """
        parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.9,
        "grounding_source":GroundingSource.VertexAISearch(data_store_id="hybrid-pdf-store_1705518048191",location=location),
        "top_p": 1,
        }
        print(prompt)
        completion = model.predict(
        f"""you are a model named HRAI dealing with company-related information and being used by professionals to get data, hence try answering in a genuine way.
        Now answer the following quries accordingly.
        {prompt}""",
        **parameters)
        print(completion.text)

        return completion.text
    
    #
    def chat_with_gai_hybrid(_self,prompt, session_tokens=None):
        # prompt = """
        # tell me a motivation story 
        # """
        parameters = {
            "candidate_count": 1,
            "max_output_tokens": 1024,
            "temperature": 0.9,
            "grounding_source":GroundingSource.VertexAISearch(data_store_id="website_1705205155526",location=location),
            "top_p": 1,
        }
        print(prompt)
        completion = model.predict(
        f"""{prompt}""",
        **parameters)
        print(completion.text)

        return completion.text