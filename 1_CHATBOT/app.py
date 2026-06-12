# Import the load_dotenv function from the dotenv package to load variables from a .env file
from dotenv import load_dotenv

# Execute the load_dotenv() function to bring the environment variables (like API keys) into the script
load_dotenv() 

# Import the built-in warnings module to control warning messages in the console
import warnings

# Tell Python to ignore and suppress any warning messages so the console stays clean
warnings.filterwarnings('ignore')


# Import the streamlit library, which is used to build web applications easily, and give it an alias 'st'
import streamlit as st

# Import the built-in os module to interact with the operating system, like reading environment variables
import os

# Import the ChatGoogleGenerativeAI class from the Langchain Google GenAI package to use Google's Gemini models
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the Gemini AI model. We specify the model name ('gemini-2.5-flash'), grab the API key from the environment, and set temperature to 0.5 for balanced creativity
model = ChatGoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.5)


# Define a function named 'get_gemini_response' that takes one argument, 'question' (the user's input)
def get_gemini_response(question):
    # Call the model's invoke method and pass it the question to get the AI's response
    response = model.invoke(question)
    
    # Return only the text content of the AI's response, ignoring other metadata
    return response.content

# Configure the Streamlit web page settings, setting the browser tab title to "Q&A_DEMO"
st.set_page_config(page_title="Q&A_DEMO")

# Add a large header text to the top of the web application
st.header("Q&A Demo")

# Create a text input box on the web app where the user can type their question, and save it in the 'input' variable
input = st.text_input("Ask a Question ", key="input")

# Create a button labeled "Ask the question". When clicked, this variable 'submit' becomes True
submit = st.button("Ask the question")

# Check if the submit button has been clicked by the user
if submit:
    # If clicked, call our get_gemini_response function with the text the user typed
    response = get_gemini_response(input)
    
    # Display the AI's response text onto the web application screen
    st.write(response)
