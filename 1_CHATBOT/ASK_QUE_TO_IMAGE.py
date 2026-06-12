from dotenv import load_dotenv
load_dotenv() 
import warnings
warnings.filterwarnings('ignore')
from PIL import Image

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')
def get_gemini_response(input ,image):
    if input!="":
        response = model.generate_content([input,image])
    else:
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title="Gemini Image Input")

st.header("Gemini Image Input")

input=st.text_input("Ask a Question ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

submit=st.button("Submit")

if submit:
    response=get_gemini_response(input, image)
    st.subheader("The Response is")
    st.text(response)