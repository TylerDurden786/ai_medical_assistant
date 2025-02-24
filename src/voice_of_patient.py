# Step1: Setup Audio recorder (ffmpeg & portaudio)
# Import necessary libraries for audio recording
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def record_audio(file_path: str, timeout=20, phrase_time_limit=None):
    """
    Objective: 
        To record audio from the microphone and save it as an MP3 file.

    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Maximum time to wait for a phrase to start (in seconds).
        phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()

    try:
        # Ensure that the microphone is properly opened and closed.
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            # Adjusts the recognizer for any background noise present in the microphone
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Save the recorded audio directly as a WAV file
            with open(file_path, "wb") as f:
                f.write(audio_data.get_wav_data())

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Step2: Setup Speech to text–STT–model for transcription
# Import necessary libraries for speech to text
import os
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"


def transcribe_with_groq(stt_model_par, audio_filepath, groq_api_key):
    client = Groq(api_key=groq_api_key)

    audio_file = open(audio_filepath, "rb")
    transcription = client.audio.transcriptions.create(
        model=stt_model_par,
        file=audio_file,
        language="en"
    )

    return transcription.text
