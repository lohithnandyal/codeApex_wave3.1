import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

from transcriber import transcribe_audio
from langchain_workflow import get_executive_summary, get_action_items, get_risk_analysis

# Load environment variables
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Multi-Modal Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
st.markdown("""
<style>
    /* Main overall background and text color to support sleek look */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #4CAF50 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Upload Box */
    .uploadedFile {
        border-radius: 10px;
        background-color: #1e242d;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }

    /* Output boxes styling */
    .output-box {
        background-color: #1a1e26;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #4CAF50;
        margin-top: 20px;
    }

    /* Sidebar Tweaks */
    [data-testid="stSidebar"] {
        background-color: #12161c;
        border-right: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062634.png", width=100) # placeholder icon
    st.title("⚙️ Configuration")
    st.markdown("Ensure your API keys are set. You can override `.env` keys here.")
    
    assembly_key = st.text_input("AssemblyAI API Key", value=os.getenv("ASSEMBLYAI_API_KEY", ""), type="password")
    groq_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")

    if assembly_key:
        os.environ["ASSEMBLYAI_API_KEY"] = assembly_key
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    st.markdown("---")
    st.markdown("**About**")
    st.caption("This assistant turns raw meeting recordings into actionable intelligence.")

# --- Main Interaction Logic ---
st.title("🎙️ Multi-Modal Meeting Assistant")
st.markdown("> Upload a recorded meeting file and the system will transcribe, summarize, extract action items, and analyze risks.")

uploaded_file = st.file_uploader("Upload Audio/Video Recording", type=["mp3", "mp4", "wav", "m4a"])

if uploaded_file is not None:
    st.markdown(f"<div class='uploadedFile'><strong>File Selected:</strong> {uploaded_file.name}</div>", unsafe_allow_html=True)
    st.audio(uploaded_file, format='audio/mp3') # preview the audio

    if st.button("Process Meeting", type="primary", use_container_width=True):
        if not os.environ.get("ASSEMBLYAI_API_KEY") or not os.environ.get("GROQ_API_KEY"):
            st.error("⚠️ API Keys are missing. Please provide them in the sidebar configuration.")
            st.stop()
            
        # Write uploaded file to a temporary location for AssemblyAI
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            with st.spinner("🎧 Transcribing audio and identifying speakers..."):
                transcript = transcribe_audio(tmp_file_path)
            st.success("Transcription complete!")
            
            # --- Output Tabs ---
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Transcript", "📊 Executive Summary", "✅ Action Items", "⚠️ Risk Analysis"])
            
            with tab1:
                st.markdown("<div class='output-box'>", unsafe_allow_html=True)
                st.subheader("Diarized Transcript")
                st.text_area("Full meeting text", transcript, height=300, disabled=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with tab2:
                with st.spinner("Generating executive summary..."):
                    summary = get_executive_summary(transcript)
                st.markdown("<div class='output-box'>", unsafe_allow_html=True)
                st.subheader("Executive Summary")
                st.markdown(summary)
                st.markdown("</div>", unsafe_allow_html=True)

            with tab3:
                with st.spinner("Extracting action items..."):
                    action_items = get_action_items(transcript)
                st.markdown("<div class='output-box'>", unsafe_allow_html=True)
                st.subheader("Action Items")
                st.json(action_items) # Display the returned JSON cleanly
                st.markdown("</div>", unsafe_allow_html=True)

            with tab4:
                with st.spinner("Analyzing risks and blockers..."):
                    risk_analysis = get_risk_analysis(transcript)
                st.markdown("<div class='output-box'>", unsafe_allow_html=True)
                st.subheader("Risk Analysis")
                st.markdown(risk_analysis)
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Cleanup temp file
            os.remove(tmp_file_path)

        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
            if os.path.exists(tmp_file_path):
                 os.remove(tmp_file_path)
