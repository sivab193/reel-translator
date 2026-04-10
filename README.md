# 🎬 Reel Translator

A local-first Streamlit application for translating short-form video content (Reels/TikToks). It extracts audio, transcribes it locally using Whisper, and translates it using a local LLM (like Gemma 4) via LM Studio or WebGPU, maintaining the vibe and timestamps of the original video.

Currently supports **English, Hindi, and Tamil**.

---

## 🛠️ Mac Mini Setup Guide

This application is specifically designed to leverage your Mac Mini's unified memory for extremely fast, private processing.

### 1. Prerequisites
- **Python 3.10+** installed on your Mac.
- **FFmpeg**: Required for audio extraction. Install it via Homebrew:
  ```bash
  brew install ffmpeg
  ```

### 2. Install Dependencies
Navigate to this directory in your terminal and install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Local LLM Configuration (LM Studio)
To translate the text entirely locally:
1. Open [LM Studio](https://lmstudio.ai/).
2. Load your model (e.g., **Gemma 4 4B Instruct**).
3. Navigate to the **Local Server** tab (the `<->` icon) and click **Start Server**.
4. **Important**: Ensure Cross-Origin Resource Sharing (CORS) is enabled in the LM Studio server settings if you encounter connection issues.
5. The default base URL expected by the app is `http://localhost:1234/v1`.

### 4. Running the App
Start the Streamlit interface using:
```bash
streamlit run app.py
```
This will open the app in your default web browser (usually at `http://localhost:8501`).

---

## 🌍 How to Share Your App (Deploying vs. Tunneling)

### Why not Vercel?
You might be tempted to deploy this to Vercel, but **Vercel is not suitable for this application** for a few reasons:
1. **Serverless Limitations**: Streamlit requires a persistent, long-running server via WebSockets. Vercel functions are stateless and timeout quickly.
2. **Local Hardware**: The magic of this app is that it uses your Mac Mini's M-series unified memory for heavy LLM inference and Whisper transcription (`ffmpeg` and CPU/GPU requirements). If deployed to Vercel, the cloud server would not be able to talk to your local LM Studio (`localhost:1234`), and the video data would leave your machine.

### The Best Way to Share: `ngrok`
To share your local app securely with friends or colleagues so they can use it over the internet while relying on your Mac's processing power:

1. Install `ngrok` via Homebrew:
   ```bash
   brew install ngrok/ngrok/ngrok
   ```
2. Make sure your Streamlit app is running (`streamlit run app.py` on port `8501`).
3. In a new terminal tab, start a tunnel:
   ```bash
   ngrok http 8501
   ```
4. `ngrok` will provide a public URL (e.g., `https://1234-abcd.ngrok-free.app`). Send this URL to anyone! They will see the Streamlit UI, and when they process a video, the transcription and translation will happen securely on your Mac Mini.