import streamlit as st
import os
import tempfile
from processor import extract_audio, transcribe_audio, translate_text

st.set_page_config(page_title="Reel Translator", layout="wide")

st.title("🎬 Reel Translator")
st.markdown("Translate short-form video content maintaining vibe and timing!")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    inference_engine = st.radio(
        "Inference Engine",
        ["Local LM Studio", "WebGPU"],
        help="Select the backend for the LLM."
    )

    default_base_url = "http://localhost:1234/v1" if inference_engine == "Local LM Studio" else "http://localhost:8080/v1"

    api_base = st.text_input("API Base URL", value=default_base_url)
    model_name = st.text_input("Model Name", value="gemma-4b-it")

    st.divider()

    languages = ["English", "Hindi", "Tamil"]
    source_lang = st.selectbox("Source Language", ["Auto"] + languages)
    target_lang = st.selectbox("Target Language", languages, index=1)

# Main UI
uploaded_file = st.file_uploader("Upload a Video (.mp4, .mov)", type=["mp4", "mov"])

if uploaded_file is not None:
    # Display the video
    st.video(uploaded_file)

    if st.button("🚀 Process Reel", type="primary"):
        with st.spinner("Processing video..."):
            # Save uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                temp_video.write(uploaded_file.read())
                video_path = temp_video.name

            audio_path = video_path.replace('.mp4', '.wav').replace('.mov', '.wav')

            # Step 1: Extract Audio
            st.info("🎵 Extracting audio...")
            extraction_success = extract_audio(video_path, audio_path)

            if not extraction_success:
                st.error("Failed to extract audio. Ensure ffmpeg is installed and the video is valid.")
                os.remove(video_path)
                st.stop()

            # Step 2: Transcribe
            st.info("✍️ Transcribing audio using local Whisper...")
            transcript, raw_text = transcribe_audio(audio_path, source_lang)

            if not transcript:
                st.error("Failed to transcribe audio.")
                os.remove(video_path)
                os.remove(audio_path)
                st.stop()

            # Step 3: Translate
            st.info(f"🌍 Translating to {target_lang} using Gemma 4...")
            translated_text = translate_text(
                transcript=transcript,
                source_lang=source_lang,
                target_lang=target_lang,
                api_base=api_base,
                model_name=model_name
            )

            # Clean up temp files
            try:
                os.remove(video_path)
                os.remove(audio_path)
            except:
                pass

            st.success("✅ Processing complete!")

            # Display results side-by-side
            st.subheader("Results")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📝 Original Transcript")
                st.text_area("Source Text", value=transcript, height=400, disabled=True)

            with col2:
                st.markdown(f"### 🌐 Translated Localized Content ({target_lang})")
                st.text_area("Translated Text", value=translated_text, height=400, disabled=False)
