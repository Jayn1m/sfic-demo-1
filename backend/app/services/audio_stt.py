import os
import shutil
import tempfile
import subprocess
from google import genai
from google.genai import types

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key.strip() and api_key != "your_gemini_api_key_here":
        try:
            return genai.Client(api_key=api_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini Client: {e}")
            return None
    return None

def convert_to_wav(input_path: str, output_path: str) -> bool:
    """
    Use ffmpeg to convert any audio format (webm, ogg, mp4) to standard wav/mp3.
    """
    try:
        cmd = ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception as e:
        print(f"FFmpeg conversion notice: {e}")
        return False

async def transcribe_gujarati_audio(audio_bytes: bytes, original_filename: str = "voice.webm") -> dict:
    """
    Transcribe Gujarati citizen voice note to text using Gemini Multimodal Audio API.
    Provides intelligent fallback if API key is not configured.
    """
    client = get_gemini_client()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{original_filename}") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        if client:
            try:
                # Direct upload to Gemini File API or inline multimodal
                uploaded_file = client.files.upload(file=tmp_path)
                prompt = (
                    "You are a Gujarati Speech-to-Text transcription and extraction assistant for Gujarat government citizens. "
                    "Listen to this audio recording carefully. The speaker is speaking in Gujarati. "
                    "1. Accurately transcribe the spoken Gujarati words into Gujarati script (ગુજરાતી લિપિ). "
                    "2. Return JSON strictly in this format: "
                    "{\"transcript_gu\": \"transcribed gujarati text\", \"summary_en\": \"short english summary\"}"
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[uploaded_file, prompt],
                    config={"response_mime_type": "application/json"}
                )
                import json
                data = json.loads(response.text)
                return {
                    "transcript_gu": data.get("transcript_gu", ""),
                    "summary_en": data.get("summary_en", ""),
                    "is_simulated": False
                }
            except Exception as e:
                print(f"Gemini Audio STT error: {e}")
                return {
                    "transcript_gu": "",
                    "summary_en": "",
                    "error": f"Audio processing error: {str(e)}",
                    "is_simulated": False
                }

        # If no client or API key is not configured
        return {
            "transcript_gu": "",
            "summary_en": "",
            "error": "Gemini API key is not configured in backend/.env. Use browser microphone speech recognition directly.",
            "is_simulated": False
        }
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

