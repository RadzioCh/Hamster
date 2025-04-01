from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment
from pydub.playback import play
import os
import io
import pyttsx3
import threading
from queue import Queue
import queue

# pakiet do pobrania -> https://aka.ms/vs/17/release/ =>  https://aka.ms/vs/17/release/vs_BuildTools.exe

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)  # Szybkość mowy (domyślnie 200, możesz zwiększyć)
        self.task_queue = Queue()
        self.running = True
        self.thread = threading.Thread(target=self._process_tasks)
        self.thread.start()


    def text_to_speech(self, text):
        language = detect(text)

        tts = gTTS(text=text, lang=language)
        # Zapisz dźwięk w pamięci zamiast do pliku
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)

        # Konwertuj na format AudioSegment i odtwórz
        audio_segment = AudioSegment.from_file(audio_file, format="mp3")
        faster_audio = audio_segment.speedup(playback_speed=1.6)
        play(faster_audio)

    def _process_tasks(self):
        while self.running:
            try:
                text = self.task_queue.get(timeout=1)
                self.engine.say(text)
                self.engine.runAndWait()
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Błąd odtwarzania: {e}")

    def speak(self, text):
        if self.running:
            self.task_queue.put(text)

    def stop(self):
        self.running = False
        self.thread.join()