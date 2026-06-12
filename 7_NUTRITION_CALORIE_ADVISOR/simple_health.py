import os
import base64
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# LangChain specific imports for Google Gemini and chaining
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# =========================================================
# STEP 1: Load environment variables
# =========================================================
# This loads the GOOGLE_API_KEY from your .env file
load_dotenv()

# =========================================================
# STEP 2: Setup the Streamlit Web Application Interface
# =========================================================

# Set the title of the web page tab
st.set_page_config(page_title="Simple Nutrition App")

# Add a big header to the page
st.header("🍎 Simple Gemini Nutrition & Health App")

# Add a text input box for the user to ask specific questions
user_prompt = st.text_input("Ask a question about the food (optional):", key="input")

# Add a file uploader button so the user can upload their food image
uploaded_file = st.file_uploader("Upload an image of your food...", type=["jpg", "jpeg", "png"])

# If the user has uploaded an image, display it on the screen
if uploaded_file is not None:
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(uploaded_file)
    # Show the image on the screen
    st.image(image, caption="Your Uploaded Image", width=600)

# Add a submit button
submit_button = st.button("Calculate Total Calories")

# =========================================================
# STEP 3: Handle the Submit Button Click (Using LangChain Chaining)
# =========================================================

# The code inside this 'if' block only runs when the button is clicked
if submit_button:
    
    # First check if the user actually uploaded an image
    if uploaded_file is not None:
        try:
            # Show a loading spinner while waiting for the AI response
            with st.spinner("Analyzing your food..."):
                
                # --- PREPARE THE IMAGE ---
                # Extract the raw bytes and the type (e.g., 'image/jpeg') of the image
                image_bytes = uploaded_file.getvalue()
                image_type = uploaded_file.type
                
                # Convert the raw image bytes into a base64 encoded string format.
                # This is the format the API needs to read the image.
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                image_url = f"data:{image_type};base64,{base64_image}"
                
                # --- INITIALIZE THE AI MODEL ---
                # We use "gemini-2.5-flash" as it's the recommended multimodal model
                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
                
                # --- SETUP THE LANGCHAIN PROMPT TEMPLATE ---
                system_instruction = """
                You are an expert nutritionist. Look at the food items in the image and 
                calculate the total calories. Provide details of every food item with 
                calories intake in the below format:

                1. Item 1 - no of calories
                2. Item 2 - no of calories
                ----
                """
                
                # ChatPromptTemplate allows us to define the structure and pass variables later
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", system_instruction),
                    ("human", [
                        {"type": "text", "text": "{user_input}"},
                        {"type": "image_url", "image_url": {"url": "{image_data}"}}
                    ])
                ])
                
                # --- CREATE THE LANGCHAIN PIPELINE (CHAIN) ---
                # This uses LCEL (LangChain Expression Language).
                # Flow: Prompt -> AI Model -> String Output Parser (to get just the text)
                chain = prompt_template | llm | StrOutputParser()
                
                # --- EXECUTE THE CHAIN ---
                # We pass the variables defined in our prompt template
                response_text = chain.invoke({
                    "user_input": user_prompt,
                    "image_data": image_url
                })
                
                # --- SHOW THE RESULTS ---
                # Display the extracted text content to the user
                st.subheader("Nutrition Analysis Results:")
                st.write(response_text)
                
        except Exception as e:
            # If something goes wrong, show a red error message
            st.error(f"An error occurred: {e}")
    else:
        # Warn the user if they click submit without uploading an image
        st.warning("Please upload an image first!")
