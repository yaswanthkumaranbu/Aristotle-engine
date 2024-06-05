import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import requests
import PyPDF2

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
    if 'start' in output and 'end' in output:
        return output
    else:
        return {'start': 0, 'end': 0}


def get_answer_text(pdf_text, start, end):
    return pdf_text[start:end]

def get_pdf_text(pdf_docs):
    """
    Extract text from PDF files.

    Args:
        pdf_docs (List[BytesIO]): List of uploaded PDF files.

    Returns:
        str: Combined text extracted from all PDFs.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """
    Split text into chunks.

    Args:
        text (str): Text to be split.

    Returns:
        List[str]: List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """
    Generate and save FAISS vector store from text chunks.

    Args:
        text_chunks (List[str]): List of text chunks.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    """
    Load and return a conversational chain.

    Returns:
        ChatGoogleGenerativeAI: Loaded conversational chain.
    """
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, pdf_text):
    """
    Process user input and generate a response.

    Args:
        user_question (str): User's question.
        pdf_text (str): Text extracted from PDF files.
    """
    try:
        # Query conversational AI
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain()
        conversational_response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        
        # Query PDF-based answer
        pdf_response = answer_question(user_question, pdf_text)
        
        # Combine responses
        combined_response = {
            "conversational_ai": conversational_response["output_text"],
            "pdf_context": get_answer_text(pdf_text, pdf_response['start'], pdf_response['end'])
        }
        
        st.write("Maxwell Suite:") #gemini
        st.write(combined_response["conversational_ai"])
        
        st.write("Kruskal Suite:") #roberta
        st.write(combined_response["pdf_context"])
    

    
    except Exception as ex:
        # Handle other exceptions
        st.error("An error occurred: {}".format(ex))
        print("Error:", ex)



def main():
    # Set Streamlit page configuration
    st.set_page_config("ChimeraAI", page_icon='chimeraAI/chimera-logo.jpg')
    
    # Display ChimeraAI header
    st.write("<p style='font-size: 40px'>chimeraAI</p>", unsafe_allow_html=True)
    st.write("---")
    st.write("<p style='font-size: 35px'>www.chimeratechnologies.com</p>", unsafe_allow_html=True)
    st.write("###")
    
    # Sidebar section for file uploading
    with st.sidebar:
        st.title("Files Section")
        pdf_docs = st.file_uploader("Upload your pdf files", accept_multiple_files=True)
        
        
        # Try-except block for handling errors during learning process
        try:
            if st.button("Learn Me"):
                if pdf_docs:
                    with st.spinner("Learning..."):
                        raw_text = get_pdf_text(pdf_docs)
                        # print(raw_text)
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.success("Done")
                else:
                    st.write("Please choose the file...")
        
        except Exception as e:
            # Display error message if learning process fails
            st.write("This file is not suitable for learning! Please try with a different file...")
            print(e)

    # User input section
    user_question = st.text_input("Query me !!!")
    st.write("---")

    # Process user input if provided
    if user_question and pdf_docs:
        pdf_text = get_pdf_text(pdf_docs)
        user_input(user_question, pdf_text)

if __name__ == "__main__":
    main()
