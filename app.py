import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re
import time
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="YouTube Transcription Assistant",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"

# Define CSS for light and dark themes
light_css = """
:root {
    --background-color: white;
    --text-color: black;
    --card-background: #f8f9fa;
    --header-gradient-start: #ff4b4b;
    --header-gradient-end: #ff9e43;
    --sub-header-color: #888888;
    --transcript-bg: #f0f2f6;
    --notes-bg: #ffffff;
    --notes-border: #4CAF50;
    --btn-primary-bg: #4CAF50;
    --btn-primary-text: white;
    --btn-secondary-bg: #ff9e43;
    --btn-secondary-text: white;
    --timestamp-color: #2196F3;
    --progress-color: #4CAF50;
    --video-info-bg: #fafafa;
    --yt-red: #FF0000;
    --tag-bg: #f0f2f6;
    --footer-color: #888888;
    --highlight-bg: #fff3cd;
    --shadow-color: rgba(0,0,0,0.1);
}
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, var(--header-gradient-start), var(--header-gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-header {
    font-size: 1.1rem;
    color: var(--sub-header-color);
    margin-bottom: 2rem;
}
.stButton > button {
    background-color: var(--btn-primary-bg);
    color: var(--btn-primary-text);
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px var(--shadow-color);
}
.card {
    padding: 1.5rem;
    border-radius: 0.5rem;
    background-color: var(--card-background);
    box-shadow: 0 2px 5px var(--shadow-color);
    margin-bottom: 1rem;
}
.transcript-area {
    max-height: 300px;
    overflow-y: auto;
    padding: 1rem;
    background-color: var(--transcript-bg);
    border-radius: 0.5rem;
    font-family: monospace;
}
.notes-container {
    padding: 1.5rem;
    border-radius: 0.5rem;
    background-color: var(--notes-bg);
    border-left: 4px solid var(--notes-border);
    box-shadow: 0 2px 8px var(--shadow-color);
}
.btn-primary {
    background-color: var(--btn-primary-bg);
    color: var(--btn-primary-text);
}
.btn-secondary {
    background-color: var(--btn-secondary-bg);
    color: var(--btn-secondary-text);
}
.timestamp {
    color: var(--timestamp-color);
    font-weight: bold;
}
.stProgress > div > div > div > div {
    background-color: var(--progress-color);
}
.video-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background-color: var(--video-info-bg);
    border-radius: 0.5rem;
}
.yt-red {
    color: var(--yt-red);
    font-weight: bold;
}
.tag {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    margin-right: 0.5rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: 500;
    background-color: var(--tag-bg);
}
.sidebar-content {
    padding: 1rem;
}
.footer {
    margin-top: 3rem;
    text-align: center;
    font-size: 0.8rem;
    color: var(--footer-color);
}
.highlight {
    background-color: var(--highlight-bg);
    padding: 0.25rem;
}
"""

dark_css = """
:root {
    --background-color: #121212;
    --text-color: #e0e0e0;
    --card-background: #1e1e1e;
    --header-gradient-start: #ff4b4b;
    --header-gradient-end: #ff9e43;
    --sub-header-color: #aaaaaa;
    --transcript-bg: #2a2a2a;
    --notes-bg: #1e1e1e;
    --notes-border: #4CAF50;
    --btn-primary-bg: #4CAF50;
    --btn-primary-text: white;
    --btn-secondary-bg: #ff9e43;
    --btn-secondary-text: white;
    --timestamp-color: #2196F3;
    --progress-color: #4CAF50;
    --video-info-bg: #2a2a2a;
    --yt-red: #FF0000;
    --tag-bg: #3a3a3a;
    --footer-color: #aaaaaa;
    --highlight-bg: #3a3a3a;
    --shadow-color: rgba(255,255,255,0.05);
}
.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, var(--header-gradient-start), var(--header-gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-header {
    font-size: 1.1rem;
    color: var(--sub-header-color);
    margin-bottom: 2rem;
}
.stButton > button {
    background-color: var(--btn-primary-bg);
    color: var(--btn-primary-text);
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px var(--shadow-color);
}
.card {
    padding: 1.5rem;
    border-radius: 0.5rem;
    background-color: var(--card-background);
    box-shadow: 0 2px 5px var(--shadow-color);
    margin-bottom: 1rem;
}
.transcript-area {
    max-height: 300px;
    overflow-y: auto;
    padding: 1rem;
    background-color: var(--transcript-bg);
    border-radius: 0.5rem;
    font-family: monospace;
}
.notes-container {
    padding: 1.5rem;
    border-radius: 0.5rem;
    background-color: var(--notes-bg);
    border-left: 4px solid var(--notes-border);
    box-shadow: 0 2px 8px var(--shadow-color);
}
.btn-primary {
    background-color: var(--btn-primary-bg);
    color: var(--btn-primary-text);
}
.btn-secondary {
    background-color: var(--btn-secondary-bg);
    color: var(--btn-secondary-text);
}
.timestamp {
    color: var(--timestamp-color);
    font-weight: bold;
}
.stProgress > div > div > div > div {
    background-color: var(--progress-color);
}
.video-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background-color: var(--video-info-bg);
    border-radius: 0.5rem;
}
.yt-red {
    color: var(--yt-red);
    font-weight: bold;
}
.tag {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    margin-right: 0.5rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: 500;
    background-color: var(--tag-bg);
}
.sidebar-content {
    padding: 1rem;
}
.footer {
    margin-top: 3rem;
    text-align: center;
    font-size: 0.8rem;
    color: var(--footer-color);
}
.highlight {
    background-color: var(--highlight-bg);
    padding: 0.25rem;
}
"""

# Apply the selected theme
if st.session_state.theme == "dark":
    st.markdown(f"<style>{dark_css}</style>", unsafe_allow_html=True)
else:
    st.markdown(f"<style>{light_css}</style>", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Error: Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# Improved prompt for better transcription
prompt = """You are a professional AI-powered YouTube video transcription assistant. Your task is to convert spoken content from YouTube videos into clear, accurate, and well-formatted text. 

Please provide the following in your response:

1. Title: Extract or infer the main title of the content
2. Summary: A concise summary of the main points (5-7 bullet points)
3. Detailed Notes: Organize the transcript into a structured format with:
   - Clear paragraphs for topic changes
   - Headings for major sections
   - Speaker labels if multiple speakers are present
   - Highlighted key points or important quotes
   - Any technical terms or specific concepts explained

4. Key Takeaways: The 3-5 most important lessons or insights from the video

Format the output in clean markdown with proper headings, bullet points, and spacing for readability.

Prioritize accuracy and readability while maintaining the original meaning and important details. Remove filler words and repetitive content only if they don't add value.
"""

# Function to extract video ID from various YouTube URL formats
def extract_video_id(youtube_url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

# Function to get YouTube video details
def get_video_details(video_id):
    try:
        return {
            "title": f"Video ID: {video_id}",
            "channel": "Unknown (API needed for channel info)"
        }
    except Exception as e:
        st.error(f"Error getting video details: {str(e)}")
        return {"title": "Unknown", "channel": "Unknown"}

# Function to extract transcript
def extract_transcript(video_id):
    try:
        progress_bar = st.progress(10)
        status_text = st.empty()
        status_text.text("Initiating transcript retrieval...")
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'en-GB', 'auto'])
        progress_bar.progress(40)
        status_text.text("Transcript retrieved! Processing text...")
        formatted_transcript = ""
        full_text = ""
        for i, entry in enumerate(transcript_data):
            timestamp = entry["start"]
            text = entry["text"]
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            if i % 5 == 0:
                formatted_transcript += f"\n<span class='timestamp'>[{minutes:02d}:{seconds:02d}]</span> "
            formatted_transcript += text + " "
            full_text += text + " "
        progress_bar.progress(70)
        status_text.text("Formatting complete!")
        time.sleep(0.5)
        progress_bar.progress(100)
        status_text.empty()
        return {
            "formatted": formatted_transcript.strip(),
            "full_text": full_text.strip(),
            "raw_data": transcript_data
        }
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None

# Function to generate content using Gemini
def generate_gemini_content(transcript_text, prompt, max_retries=3):
    retry_count = 0
    progress_bar = st.progress(0)
    status_text = st.empty()
    while retry_count < max_retries:
        try:
            status_text.text("Initializing AI analysis...")
            progress_bar.progress(10)
            model = genai.GenerativeModel("gemini-2.0-flash")
            max_length = 30000
            if len(transcript_text) > max_length:
                st.warning(f"Transcript is very long ({len(transcript_text)} chars). Processing first {max_length} chars.")
                transcript_text = transcript_text[:max_length] + "... [Truncated]"
            progress_bar.progress(30)
            status_text.text("Processing transcript with AI...")
            full_prompt = f"{prompt}\n\nTRANSCRIPT:\n{transcript_text}"
            response = model.generate_content(full_prompt)
            progress_bar.progress(90)
            status_text.text("Finalizing notes...")
            time.sleep(0.5)
            progress_bar.progress(100)
            status_text.empty()
            return response.text
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                status_text.text(f"Retrying AI processing ({retry_count}/{max_retries})...")
                progress_bar.progress(30 * retry_count)
                time.sleep(2)
            else:
                st.error(f"Failed to process with AI after {max_retries} attempts: {str(e)}")
                status_text.empty()
                progress_bar.empty()
                return None

# Function to save to history
def save_to_history(video_id, video_title, notes):
    try:
        if 'history' not in st.session_state:
            st.session_state.history = pd.DataFrame(columns=['timestamp', 'video_id', 'title', 'notes'])
        new_entry = pd.DataFrame({
            'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'video_id': [video_id],
            'title': [video_title],
            'notes': [notes]
        })
        st.session_state.history = pd.concat([new_entry, st.session_state.history]).reset_index(drop=True)
        if len(st.session_state.history) > 20:
            st.session_state.history = st.session_state.history.iloc[:20]
        return True
    except Exception as e:
        st.error(f"Failed to save to history: {str(e)}")
        return False

def reset_text():
    st.session_state.text = ""
# Sidebar navigation
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/color/96/000000/youtube-play.png", width=80)
    st.markdown("<h2>YouTube Transcription Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p>Transform YouTube content into well-structured notes</p>", unsafe_allow_html=True)
    st.markdown("---")
    nav_option = st.radio("Navigation", 
                         ["✏️ Generate Notes", "📚 Recent History", "ℹ️ About"])
    st.markdown("---")
    with st.expander("💡 Quick Tips", expanded=False):
        st.markdown("""
        - Videos must have available captions
        - Educational content works best
        - Try different videos if one fails
        - You can manually paste transcripts
        """)
    with st.expander("🎬 Example Videos", expanded=False):
        st.markdown("""
        Try these videos with good transcripts:
        - [TED Talk: The Power of Vulnerability](https://www.youtube.com/watch?v=iCvmsMzlF7o)
        - [Khan Academy: Introduction to Limits](https://www.youtube.com/watch?v=riXcZT2ICjA)
        - [Crash Course: History of Science](https://www.youtube.com/watch?v=YvtCLceNf30)
        """)
    st.markdown("</div>", unsafe_allow_html=True)

# Main content area
st.markdown(f'<div class="{st.session_state.theme}">', unsafe_allow_html=True)

import streamlit as st

# Initialize session state variables if they don't exist
if 'youtube_link' not in st.session_state:
    st.session_state.youtube_link = ""

def clear_input():
    """Function to clear the YouTube link input field"""
    st.session_state.youtube_link = ""

if nav_option == "✏️ Generate Notes":
    st.markdown("<h1 class=main-header>YouTube Transcription Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p>Transform YouTube videos into comprehensive notes with AI</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 20])
    with col1:
        st.markdown("<h3>▶️</h3>", unsafe_allow_html=True)
    with col2:
        youtube_link = st.text_input(
            "",
            placeholder="Paste YouTube video URL here...",
            label_visibility="collapsed",
            key="youtube_link"  # Add a key to link with session state
        )
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        process_button = st.button("✨ Generate Notes", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🔄 Clear Input", on_click=clear_input, use_container_width=True)
    with col3:
        st.markdown("")
    st.markdown("</div>", unsafe_allow_html=True)
    if youtube_link and process_button:
        video_id = extract_video_id(youtube_link)
        if not video_id:
            st.error("Invalid YouTube URL. Please enter a valid YouTube video link.")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"""
                <div style="position: relative; text-align: center;">
                    <img src="https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" style="width: 100%; border-radius: 10px;">
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                        <a href="https://www.youtube.com/watch?v={video_id}" target="_blank">
                            <img src="https://img.icons8.com/fluency/96/000000/youtube-play.png" style="width: 60px;">
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                video_details = get_video_details(video_id)
                st.markdown(f"#### {video_details['title']}")
                st.markdown(f"Channel: {video_details['channel']}")
                st.markdown("""
                <div style="margin-top: 10px;">
                    <span class="tag">Educational</span>
                    <span class="tag">English</span>
                    <span class="tag">Transcript Available</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            with st.spinner(""):
                transcript_data = extract_transcript(video_id)
            if transcript_data:
                with st.expander("📋 Raw Transcript", expanded=False):
                    st.markdown(f"<div class='transcript-area'>{transcript_data['formatted']}</div>", unsafe_allow_html=True)
                notes = generate_gemini_content(transcript_data["full_text"], prompt)
                if notes:
                    st.success("✅ Notes generated successfully!")
                    save_to_history(video_id, video_details["title"], notes)
                    
                    st.markdown(notes)
                    st.markdown("</div>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            label="📥 Download as Markdown",
                            data=notes,
                            file_name=f"notes_{video_id}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
    with st.expander("⌨️ Process Transcript Manually", expanded=False):
        
        st.markdown("Use this option if automatic transcript fetching fails.")
        manual_transcript = st.text_area("Paste your transcript here:", height=200)
        col1, col2 = st.columns([1, 4])
        with col1:
            manual_process = st.button("Process Transcript", use_container_width=True)
        if manual_transcript and manual_process:
            notes = generate_gemini_content(manual_transcript, prompt)
            if notes:
                st.success("✅ Notes generated successfully!")
                st.markdown("---", unsafe_allow_html=True)
                st.markdown(notes)
                st.markdown("</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Notes",
                    data=notes,
                    file_name="manual_transcript_notes.md",
                    mime="text/markdown"
                )
        st.markdown("</div>", unsafe_allow_html=True)

elif nav_option == "📚 Recent History":
    st.markdown("<h1 class='main-header'>Recent Notes History</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Access your previously generated notes</p>", unsafe_allow_html=True)
    if 'history' in st.session_state and not st.session_state.history.empty:
        for index, row in st.session_state.history.iterrows():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 4])
            with col1:
                video_id = row['video_id']
                st.image(f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg", 
                        use_container_width=True)
            with col2:
                st.markdown(f"#### {row['title']}")
                st.markdown(f"<small>Generated on {row['timestamp']}</small>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    view_button = st.button(f"👁️ View Notes #{index}", key=f"view_{index}")
                with col2:
                    st.download_button(
                        label=f"📥 Download #{index}",
                        data=row['notes'],
                        file_name=f"notes_{video_id}.md",
                        mime="text/markdown",
                        key=f"dl_{index}"
                    )
            st.markdown("</div>", unsafe_allow_html=True)
            if view_button:
                st.markdown("<div class='notes-container'>", unsafe_allow_html=True)
                st.markdown(row['notes'])
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center; padding: 50px 0;'>", unsafe_allow_html=True)
        st.image("https://img.icons8.com/ios/100/000000/empty-box.png", width=80)
        st.markdown("#### No history yet")
        st.markdown("Generate notes from YouTube videos to see them here")
        st.markdown("</div>", unsafe_allow_html=True)

elif nav_option == "ℹ️ About":
    st.markdown("<h1 class='main-header'>About YouTube Transcription Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
    <h3>How it works</h3>
    <p>YouTube Notes AI converts video content into comprehensive notes by:</p>
    <ol>
        <li>Extracting the video transcript using YouTube's API</li>
        <li>Processing the raw transcript with Google's Gemini AI</li>
        <li>Organizing the information into structured notes with key points</li>
        <li>Presenting the results in an easy-to-read format</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
    <h3>Best uses</h3>
    <p>This tool is particularly helpful for:</p>
    <ul>
        <li>Students studying educational content</li>
        <li>Researchers collecting information from video lectures</li>
        <li>Content creators summarizing video research</li>
        <li>Anyone who wants to extract key information from videos</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h3>Features</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
        <h4>🔍 Smart Extraction</h4>
        <p>Automatically extracts and processes video transcripts with minimal effort</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='card'>
        <h4>📊 Structured Output</h4>
        <p>Organizes information into clear sections with headings and key points</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card'>
        <h4>💾 History Tracking</h4>
        <p>Saves your generated notes for easy reference later</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='card'>
        <h4>📱 Responsive Design</h4>
        <p>Works seamlessly across desktop and mobile devices</p>
        </div>
        """, unsafe_allow_html=True)

