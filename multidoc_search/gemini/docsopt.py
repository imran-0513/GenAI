import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import datetime

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_from_docx(docx_file):
    text = ""
    doc = Document(docx_file)
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

def get_text_from_excel(excel_file):
    text = ""
    xls = pd.ExcelFile(excel_file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        for _, row in df.iterrows():
            for cell in row:
                text += str(cell)
    return text

def get_text_chunks(text):
    max_chunk_size = 5000  # Adjust the chunk size as needed
    chunks = []
    for i in range(0, len(text), max_chunk_size):
        chunks.append(text[i:i + max_chunk_size])
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    answer the question as detailed as possible from the provided context, the document may have different 
    structures like receipts, different resume formats of the candidate so kindly go through the 
    documents from start to end and make sure to provide all the details,
    if the answer is not in the provided context just say, "answer is not available in the context", don't
    provide the wrong answer\n\n
    Context:\n{context}?\n
    Question:\n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question, uploaded_files):
    if not uploaded_files:
        st.error("Please upload at least one file.")
        return

    text = ""
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split('.')[-1]

        if file_extension == 'pdf':
            text += get_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            text += get_text_from_docx(uploaded_file)
        elif file_extension in ['xls', 'xlsx']:
            text += get_text_from_excel(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return

    text_chunks = get_text_chunks(text)
    get_vector_store(text_chunks)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.from_texts(text_chunks, embedding=embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    # Log the query and response to a text file
    log_interaction(user_question, response["output_text"])

    st.write("Reply: ", response["output_text"])

def log_interaction(query, response):
    log_file_path = "interaction_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file_path, "a") as log_file:
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Query: {query}\n")
        log_file.write(f"Response: {response}\n\n")

def main():
    st.set_page_config("Chat document")
    st.header("Chat with document using Gemini💁")

    user_question = st.text_input("Ask a Question from the Files")

    uploaded_files = st.file_uploader("Upload Files", type=['pdf', 'docx', 'xls', 'xlsx'], accept_multiple_files=True)

    if st.button("Submit & Process"):
        if user_question and uploaded_files:
            user_input(user_question, uploaded_files)
        else:
            st.error("Please provide both a question and upload files.")

if __name__ == "__main__":
    main()
