from dotenv import load_dotenv
import io
import base64
# from uu import decode as uu_decode

from urllib import response  # Updated import
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

poppler_path = r'C:\\Users\\Imran.Munshi\\Downloads\\Release-23.11.0-0\\poppler-23.11.0\\Library\bin'
os.environ["PATH"] += os.pathsep + poppler_path

# print(os.environ["PATH"])

import pdf2image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemeni_respone(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

    # Check if 'parts' is available, if not, use the full lookup
    if hasattr(result, 'parts'):
        text_content = result.parts[0].text
    else:
        # Adjust the index based on your response structure
        text_content = result.candidates[0].content.parts[0].text

    return text_content


def input_pdf_setup(upload_file):
    if upload_file is not None:
    ## convert pdf to image
        images = pdf2image.convert_from_bytes(upload_file.read())

        first_page = images[0]
        ## covert to bytes
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr,format='JPEG')
        image_byte_arr = image_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(image_byte_arr).decode() ## encode to base64

            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    


######### streamlit app
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text =st.text_area("Job Despcription: ",key="input")
upload_file = st.file_uploader("Upload your resume(PDF).....",type=["pdf"])

if input_text is None:
    st.write("Please provide the Job description")


elif upload_file is not None:
    st.write("PDF Uploaded successfully")


submit1 = st.button("Tell me about the resume")
# submit2 = st.button("How can i improve my skills")
submit3 = st.button("Percentage match")


input_prompt1 = """
You are an experienced Technical Human Resource Manager in the field of data science,fullstack web development,
big data engineering,Data analyst, devops, your task is to review the provided resume against the job description
for these profiles. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science,fullstack web development,
big data engineering,Data analyst, devops and ATS functionality, your task is to evluate the uploaded resume 
against the provided job description. give me the percentage of match if the resume matches the job description.
First the output should come as percentage and then keywords missing as per the job descriptions provided
in the input and check each keyword as skill and compare with the input job description with resume uploaded and provide 
skills or keyword that are not matching with input job description and last final thoughts if the resume is good match or not after comparing the uploaded resume 
with Job description provided in the input and in input if we dont provide any job description details it
should not provide any thoughts and percentage if the job description is empty .
"""


if submit1:
        if upload_file is not None:  # Check if file is uploaded
            if input_text.strip():  # Check if job description is not empty or just whitespace
                pdf_content = input_pdf_setup(upload_file)
                response = get_gemeni_respone(input_prompt2, pdf_content, input_text)
                st.subheader("The response is ")
                st.write(response)
            else:
                st.write("Please input the job description")
        else:
            st.write("No file uploaded. Please upload a resume.")
        




 