from gtts import gTTS
import os
import threading

def speak(text):
    def run_in_thread():
        tts = gTTS(text=text, lang='en', slow=False)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_name = "texto.mp3"
        file_path = os.path.join(current_dir, file_name)
        tts.save(file_path)
        os.system(f"mpg321 {file_path}")

    t = threading.Thread(target=run_in_thread)
    t.start()
