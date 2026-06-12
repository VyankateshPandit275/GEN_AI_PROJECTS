import streamlit as st
import os
import time
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_classic.chains.retrieval import (
    create_retrieval_chain
)

from langchain_core.prompts import ChatPromptTemplate

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables from a .env file (like API keys)
load_dotenv()

# Retrieve API keys from environment variables
groq_api_key = os.getenv("GROQ_CLOUD_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Set the title of the Streamlit web application
st.title("Gemma Model Document Q&A")

# Initialize the Groq Language Model
# We are using the "llama-3.3-70b-versatile" model provided by Groq
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# Define the prompt template that tells the AI how to answer
# It forces the AI to only use the provided context to answer the question
prompt = ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.

Please provide the most accurate response based on the question.

<context>
{context}
</context>

Question:
{input}
"""
)

# Function to read PDFs, split text, create embeddings, and store them in a Vector Database
def vector_embedding():
    # Only initialize if vectors are not already in the session state
    if "vectors" not in st.session_state:

        # Step 1: Initialize the embedding model (converts text to numerical vectors)
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        # Step 2: Load all PDF documents from the "./us_census" folder
        st.session_state.loader = PyPDFDirectoryLoader(
            "./us_census"
        )

        # Read the documents
        st.session_state.docs = (
            st.session_state.loader.load()
        )

        # Step 3: Split the documents into smaller chunks
        # This helps the AI process information in bite-sized pieces without exceeding its limits
        st.session_state.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=1000,   # Each chunk will have up to 1000 characters
                chunk_overlap=200  # Overlap 200 characters between chunks to keep context intact
            )
        )

        # Apply the splitting process to our loaded documents
        st.session_state.final_documents = (
            st.session_state.text_splitter.split_documents(
                st.session_state.docs
            )
        )

        # Step 4: Create the Vector Database (FAISS)
        # It takes the text chunks and their corresponding numerical embeddings, allowing fast similarity searches
        st.session_state.vectors = FAISS.from_documents(
            st.session_state.final_documents,
            st.session_state.embeddings
        )

# Text input field for the user to type their question
prompt1 = st.text_input(
    "Enter Your Question From Documents"
)

# Button to trigger the document embedding process
if st.button("Documents Embedding"):
    vector_embedding()
    st.write("Vector Store DB Is Ready")

import time

# If the user has entered a question
if prompt1:

    # Make sure the documents have been embedded first
    if "vectors" not in st.session_state:
        st.warning(
            "Please click Documents Embedding first."
        )
        st.stop() # Stop execution if vectors are missing

    # Create a chain that takes a list of documents and formats them into a prompt for the LLM
    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    # Set up the retriever to find the most relevant document chunks based on the user's question
    # search_kwargs={"k": 4} means it will fetch the top 4 most similar chunks
    retriever = st.session_state.vectors.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Combine the retriever and the document chain into one seamless workflow
    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    # Track how long it takes to get the answer
    start = time.process_time()

    # Pass the user's question to the chain and get the response
    response = retrieval_chain.invoke(
        {"input": prompt1}
    )

    # Display the final answer on the web app
    st.write(response["answer"])

    print(
        "Response time :",
        time.process_time() - start
    )

    # Create an expandable section to show exactly which document chunks the AI used
    with st.expander(
        "Document Similarity Search"
    ):
        # Loop through each document chunk and display it
        for i, doc in enumerate(
            response["context"]
        ):
            st.write(doc.page_content)
            st.write(
                "--------------------------------"
            )