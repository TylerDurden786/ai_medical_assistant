# VoiceBot UI with Gradio
# Import necessary libraries for gradio
import os
import gradio as gr
from dotenv import load_dotenv

# Importing functions from the modules
from brain_of_doctor import encode_image, analyze_image_with_query
from voice_of_patient import record_audio, transcribe_with_groq
from voice_of_doctor import text_to_speech_with_gtts

# Specifying fine-tuned input prompt
system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Do not say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    """
    Processes audio and image inputs to generate a doctor's response.

    Args:
        audio_filepath (str): Path to the audio file for transcription.
        image_filepath (str): Path to the image file for analysis.

    Returns:
        tuple: (Transcribed text, Doctor's response, Path to saved speech)
    """
    load_dotenv()
    groq_api_key_value = os.environ.get("GROQ_API_KEY")

    speech_to_text_output = transcribe_with_groq(
        groq_api_key=groq_api_key_value,
        audio_filepath=audio_filepath,
        stt_model_par="whisper-large-v3"
    )

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    # Ensure output folder exists and save audio file
    output_audio_path = "../output_audio_files/doctor_response.mp3"
    
    output_audio_path = text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio_path)

    return speech_to_text_output, doctor_response, output_audio_path


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(None)
    ],
    title="AI Doctor with Vision and Voice"
    )

if __name__ == "__main__":
    iface.launch(debug=True)