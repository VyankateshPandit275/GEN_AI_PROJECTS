"""
This application is an ATS (Applicant Tracking System) Resume Checker.
It allows a user to upload a resume (PDF format) and paste a Job Description. 
It uses Google's Gemini Vision AI to visually "read" the first page of the resume 
and evaluate it against the job description to provide feedback or a match percentage.

Below, we break down exactly what each section of the code is doing and WHY.
"""

# ---------------------------------------------------------
# 1. Loading Environment Variables
# ---------------------------------------------------------
from dotenv import load_dotenv

# We execute load_dotenv() to safely load our hidden API keys into the environment.
# This ensures our Google API key isn't exposed publicly in the code.
load_dotenv()

# ---------------------------------------------------------
# 2. Importing Required Libraries
# ---------------------------------------------------------
import base64                   # Used to encode the image into a string format that APIs can read
import streamlit as st          # The framework used to build our interactive web interface
import os                       # Used to read the API key from the environment variables
import io                       # Helps manage reading and writing files in system memory (Bytes)
from PIL import Image           # The Python Imaging Library, used to process image data
import pdf2image                # A library that specifically converts PDF files into Image files
import google.generativeai as genai  # The official Google SDK to communicate with Gemini AI

# Configure the genai library with our secret API key so Google knows we are authorized.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------------------------------------------------------
# 3. Setting up the AI (Gemini) Function
# ---------------------------------------------------------
def get_gemini_response(input, pdf_content, prompt):
    """
    This function talks directly to the Gemini Vision AI.
    It passes three things:
    1. The System instructions (input)
    2. The image of the resume (pdf_content)
    3. The job description the user pasted (prompt)
    """
    # Initialize the Vision model. We use 'gemini-pro-vision' because we are sending 
    # image data (the converted resume) and we need the AI to "look" at it.
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # We ask the model to generate content based on the combined list of inputs.
    response = model.generate_content([input, pdf_content[0], prompt])
    
    # We only care about the text response from the AI, so we extract and return it.
    return response.text

# ---------------------------------------------------------
# 4. Processing the Uploaded PDF File
# ---------------------------------------------------------
def input_pdf_setup(uploaded_file):
    """
    Since you upgraded to the 'gemini-2.5-flash' model, we no longer need to manually 
    convert the PDF into an image (which caused the Poppler error). 
    The new Flash models natively understand PDF files!
    """
    if uploaded_file is not None:
        # Read the raw bytes of the PDF directly
        bytes_data = uploaded_file.getvalue()

        # Package the raw PDF bytes into the exact format Gemini expects
        pdf_parts = [
            {
                "mime_type": "application/pdf",
                "data": bytes_data
            }
        ]
        return pdf_parts
    else:
        # Stop the script and throw an error if the user forgot to upload a file
        raise FileNotFoundError("No file uploaded")

# ---------------------------------------------------------
# 5. Building the Streamlit Web Interface
# ---------------------------------------------------------

# Set the title that appears on the browser tab
st.set_page_config(page_title="ATS Resume EXpert")

# Set the main visible header on the webpage
st.header("ATS Tracking System")

# Create a large text area for the HR manager/user to paste the Job Description
input_text = st.text_area("Job Description: ", key="input")

# Create a file uploader widget that only accepts PDFs
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

# If the user successfully uploads a file, display a confirmation message
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Create two buttons for the two different features of our application
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

# ---------------------------------------------------------
# 6. Defining the System Instructions (Prompts)
# ---------------------------------------------------------
# This prompt asks the AI to act like an HR Manager and write a qualitative review.
input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

# This prompt asks the AI to act like an ATS scanner software and output a quantitative match %.
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# ---------------------------------------------------------
# 7. Handling Button Clicks
# ---------------------------------------------------------

# If the user clicks the first button (Qualitative Review):
if submit1:
    if uploaded_file is not None:
        # Convert the PDF to an image part
        pdf_content = input_pdf_setup(uploaded_file)
        
        # Send the HR Prompt, the Resume Image, and the Job Description to Gemini
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        
        # Display the result
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

# If the user clicks the second button (Quantitative Percentage Match):
elif submit3:
    if uploaded_file is not None:
        # Convert the PDF to an image part
        pdf_content = input_pdf_setup(uploaded_file)
        
        # Send the ATS Scanner Prompt, the Resume Image, and the Job Description to Gemini
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        
        # Display the result
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
