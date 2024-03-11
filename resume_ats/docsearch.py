# Make sure to install the required libraries
# pip install openai streamlit pandas docx2txt

import streamlit as st
from openai import OpenAI  # Change the import statement
import pandas as pd
import docx2txt
import os

# Set OpenAI API key
client = OpenAI(  # Adjust this line accordingly
    api_key=os.getenv("OPENAI_API_KEY")  # Ensure OPENAI_API_KEY is set in your environment
)

# Function to search documents
def search_documents(query, documents):
    responses = []

    for file_uploader in documents:
        file_name = file_uploader.name
        try:
            file_content = file_uploader.read().decode("utf-8")
        except UnicodeDecodeError:
            # If decoding as utf-8 fails, try with errors ignored
            file_content = file_uploader.read().decode("utf-8", errors="ignore")

        # Use OpenAI to generate responses based on the query and document content
        user_message = f"Search the document for '{query}':\n{file_content}"
        response = client.ChatCompletion.create(  # Adjust this line accordingly
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
        )

        responses.append(response.choices[0].message["content"].strip())

    return responses

# Main Streamlit app
def main():
    st.title("Document Search Chat Bot")

    # Upload documents
    st.sidebar.header("Upload Documents")
    uploaded_files = st.sidebar.file_uploader("Upload documents", type=["pdf", "docx", "xlsx"], accept_multiple_files=True)

    # User input
    query = st.text_input("Ask a query:")

    # Search button
    if st.button("Search"):
        if uploaded_files:
            st.write("Searching in the following documents:")
            st.write([file_uploader.name for file_uploader in uploaded_files])

            # Search documents and display results
            results = search_documents(query, uploaded_files)
            st.header("Search Results")
            for result in results:
                st.write(result)

if __name__ == "__main__":
    main()
