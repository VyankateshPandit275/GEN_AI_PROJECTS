# Import load_dotenv to load environment variables (like secret API keys) from a .env file
from dotenv import load_dotenv

# Execute load_dotenv() so that variables from the .env file are loaded into the system environment
load_dotenv()

# Import the streamlit library to build the web application interface easily
import streamlit as st

# Import the os module to interact with the operating system (used to get the API key)
import os

# Import pathlib which helps deal with file paths (though not strictly used in this current script)
import pathlib

# Import textwrap to format text blocks nicely (also not strictly used, but good to have)
import textwrap

# Import the Image module from the Python Imaging Library (PIL) to handle image file processing
from PIL import Image

# Import the official Google Generative AI SDK to access Gemini models
import google.generativeai as genai

# Configure the genai library with our API key so Google knows we are authorized to use the model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Vision model. 'gemini-2.5-flash' is fast and supports reading images
model = genai.GenerativeModel('gemini-2.5-flash')

# Define a function to send the image and prompt to the Gemini model and get the text response
def get_gemini_response(input, image, prompt):
    # Call generate_content passing a list containing the system prompt, the image data, and the user's specific question
    response = model.generate_content([input, image[0], prompt])
    
    # Return the text portion of the AI's response
    return response.text

# Define a function to process the uploaded image file into the specific format that Gemini requires
def input_image_setup(uploaded_file):
    # Check if a file was actually uploaded
    if uploaded_file is not None:
        # Read the uploaded file into raw byte data
        bytes_data = uploaded_file.getvalue()
        
        # Package the byte data and the image type (like image/jpeg) into a dictionary format expected by Gemini
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # e.g., 'image/jpeg' or 'image/png'
                "data": bytes_data                # The raw image bytes
            }
        ]
        # Return this formatted image data
        return image_parts
    else:
        # If no file was uploaded, raise an error to stop execution
        raise FileNotFoundError("No File Uploaded")

# Set the configuration for the Streamlit web page, giving the browser tab a title
st.set_page_config(page_title="Multilanguage Invoice Extractor")

# Display a large header text at the top of the web application
st.header("Multilanguage Invoice Extractor")

# Create a text input box where the user can ask a specific question about the invoice
input_text = st.text_input("Input: ", key="input")

# Create a file uploader widget that only accepts JPG, JPEG, and PNG image files
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

# Initialize an empty variable to hold the image
image = ""

# Check if the user has uploaded a file
if uploaded_file is not None:
    # Open the uploaded file as a PIL Image object so Streamlit can display it
    image = Image.open(uploaded_file)
    
    # Display the image on the web page with a caption, stretching it to fit the width
    st.image(image, caption="Uploaded Image.", width='stretch')

# Create a button labeled "Tell me about the image" that sets 'submit' to True when clicked
submit = st.button("Tell me about the image")

# Define the "System Prompt" - this tells the AI how it should behave and what its role is
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

# Check if the user clicked the "Tell me about the image" button
if submit:
    # Step 1: Process the uploaded image using our setup function
    image_data = input_image_setup(uploaded_file)
    
    # Step 2: Pass the system prompt, the formatted image, and the user's question to the Gemini model
    response = get_gemini_response(input_prompt, image_data, input_text)
    
    # Step 3: Display a subheader on the web page for the results
    st.subheader("The Response is")
    
    # Step 4: Write the AI's response text onto the web page
    st.write(response)
