import streamlit as st
import os
from dotenv import load_dotenv

import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv() ##load all the nevironment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

def extract_video_id(url):
    """Helper to extract standard 11-char video ID from various YouTube URL formats"""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url.split("=")[1] if "=" in url else url

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        
        # Try the standard get_transcript method first
        if hasattr(YouTubeTranscriptApi, 'get_transcript'):
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        else:
            # Fallback for older youtube-transcript-api versions (instance methods)
            api = YouTubeTranscriptApi()
            try:
                transcript_list = api.list(video_id)
                try:
                    transcript_obj = transcript_list.find_transcript(['en'])
                except:
                    for t in transcript_list:
                        transcript_obj = t
                        break
                transcript_text = transcript_obj.fetch()
            except AttributeError:
                # If list() returns something without find_transcript, try fetch() directly
                transcript_text = api.fetch(video_id)

        transcript = ""
        for i in transcript_text:
            if isinstance(i, dict):
                transcript += " " + i["text"]
            else:
                transcript += " " + i.text

        return transcript

    except Exception as e:
        return f"ERROR: Could not retrieve transcript. (Details: {str(e)})"
    
## getting the summary based on Prompt using Google Gemini
def generate_google_content(transcript_text, system_prompt):
    # Initialize the generative model
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # Generate content natively
    response = model.generate_content(system_prompt + "\n\nHere is the transcript:\n" + transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter (Google Gemini)")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = extract_video_id(youtube_link)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except Exception:
        st.error("Please enter a valid YouTube URL.")

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        if transcript_text.startswith("ERROR:"):
            st.error(transcript_text)
        else:
            with st.spinner("Generating summary using Google Gemini..."):
                try:
                    summary = generate_google_content(transcript_text, prompt)
                    st.markdown("## Detailed Notes:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Google Generation Error: {e}")
