import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Debug tool: Show available Gemini models (for debugging)
if st.checkbox("Show available Gemini models (for debugging)"):
    try:
        st.subheader("🔍 Available Gemini Models")
        for model in genai.list_models():
            st.write(f"**{model.name}** — supports: {model.supported_generation_methods}")
    except Exception as e:
        st.error(f"Error listing models: {e}")

# Summarization prompt
prompt = """
You are a YouTube video summarizer. You will get the transcript text of a YouTube video, 
and your task is to summarize the entire video into important points in under 250 words.
Here is the transcript:
"""

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[-1].split("&")[0]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except Exception as e:
        return f"Error extracting transcript: {e}"

# Function to generate summary from Gemini
def generate_gemini_content(transcript_text, prompt):
    try:
        # Use the correct model name from the available models
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")# Changed model name here
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

# Streamlit UI
st.title("🎥 YouTube Transcript to Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

# Show thumbnail if link is provided
if youtube_link:
    try:
        video_id = youtube_link.split("v=")[-1].split("&")[0]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except:
        st.warning("Invalid YouTube link format.")

# Button action
if st.button("Get Detailed Notes"):
    with st.spinner("Fetching transcript and generating summary..."):
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text.startswith("Error"):
            st.error(transcript_text)
        else:
            summary = generate_gemini_content(transcript_text, prompt)
            if summary.startswith("Error"):
                st.error(summary)
            else:
                st.markdown("## 📝 Detailed Notes:")
                st.write(summary)
