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

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_docx_text(docx_docs):
    text = ""
    for docx in docx_docs:
        doc = Document(docx)
        for paragraph in doc.paragraphs:
            text += paragraph.text
    return text

def get_excel_text(excel_docs):
    text = ""
    for excel in excel_docs:
        xls = pd.ExcelFile(excel)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            for _, row in df.iterrows():
                for cell in row:
                    text += str(cell)
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
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

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    # Log the query and response to a text file
    log_interaction(user_question, response["output_text"])

    print(response)
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

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload PDF Files", accept_multiple_files=True, type='pdf')
        docx_docs = st.file_uploader("Upload DOCX Files", accept_multiple_files=True, type='docx')
        excel_docs = st.file_uploader("Upload Excel Files", accept_multiple_files=True, type='xlsx')

        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = ""
                if pdf_docs:
                    raw_text += get_pdf_text(pdf_docs)
                if docx_docs:
                    raw_text += get_docx_text(docx_docs)
                if excel_docs:
                    raw_text += get_excel_text(excel_docs)

                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()
