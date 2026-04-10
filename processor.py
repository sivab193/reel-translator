import os
from moviepy import VideoFileClip
import whisper
from openai import OpenAI

def extract_audio(video_path, audio_path):
    """Extracts audio from a video file and saves it to audio_path."""
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, logger=None)
        return True
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False

def transcribe_audio(audio_path, language=None):
    """Transcribes audio using local Whisper model."""
    try:
        # Using base model for speed/memory efficiency on local CPU/MPS
        model = whisper.load_model("base")

        # We allow language to be passed but whisper can also detect it
        options = {}
        if language and language != "Auto":
            # Map full language name to language code if needed, Whisper generally handles it
            options["language"] = language

        result = model.transcribe(audio_path, **options)

        # Format the result with timestamps
        formatted_transcript = ""
        for segment in result["segments"]:
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            formatted_transcript += f"[{start} --> {end}] {text}\n"

        return formatted_transcript, result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None, None

def format_timestamp(seconds):
    """Helper to format seconds into mm:ss.ms"""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:05.2f}"

def translate_text(transcript, source_lang, target_lang, api_base, model_name):
    """Translates text using local Gemma model via OpenAI API."""
    try:
        client = OpenAI(
            base_url=api_base,
            api_key="lm-studio" # API key is required but can be anything for local
        )

        system_prompt = f"""You are an expert cultural translator specializing in short-form video content (Reels/TikToks).
Your task is to translate the following transcript from {source_lang} to {target_lang}.

Important Instructions:
1. Identify any slang, memes, or cultural references in the source text.
2. Provide a translation that maintains the "vibe", tone, and pacing of a short-form video.
3. Keep the timestamps exactly as they appear in the original transcript.
4. Output ONLY the translated, timestamped transcript. Do not include introductory text or explanations.
"""

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate this transcript:\n\n{transcript}"}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error translating text: {e}")
        return f"Error: {e}"
