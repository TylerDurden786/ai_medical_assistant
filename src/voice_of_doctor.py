import os
import platform
import subprocess
from gtts import gTTS
import pygame

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    output_filepath_mp3 = os.path.splitext(output_filepath)[0] + ".mp3"  # change to mp3
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath_mp3)  # save as mp3
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath_mp3])
        elif os_name == "Windows":  # Windows
            pygame.mixer.init()
            pygame.mixer.music.load(output_filepath_mp3)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath_mp3])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")