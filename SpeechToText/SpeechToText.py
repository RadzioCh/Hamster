import speech_recognition as sr
from langdetect import detect
import whisper
import time
import sounddevice as sd
import numpy as np
from queue import Queue
import queue
import threading
import wavio
import sys
import wave
import scipy.signal
from googletrans import Translator
from TextToSpeech import TextToSpeech

from gtts import gTTS

class SpeechToText:

    def __init__(self):
        # Ustawienia audio
        self.SAMPLE_RATE = 48000  # Częstotliwość próbkowania
        self.CHANNELS = 1  # Stereo
        self.BLOCK_SIZE = 1024  # Rozmiar bloku danych audio
        self.SEGMENT_DURATION = 5  # Czas przechwytywania w sekundach (możesz изменить)

        # Kolejka do przechowywania danych audio
        self.audio_queue = Queue()
        self.running = True  # Flaga do kontrolowania pętli
        self.translator = Translator()  # Inicjalizacja tłumacza
        self.tts = TextToSpeech()



    def start_speech(self):
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Mów teraz...")
            recognizer.adjust_for_ambient_noise(source)  # Dopasowanie do szumów
            audio = recognizer.listen(source)  # Nagrywanie mowy

        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Wykrywanie języka za pomocą Whisper
        model = whisper.load_model("base")
        result = model.transcribe("temp_audio.wav", task="transcribe", fp16=False)
        detected_language = result['language'] # Wykryty język
        print(f"Wykryty język: {detected_language}")

        # Rozpoznawanie tekstu z mowy
        try:
            text = recognizer.recognize_google(audio, language=detected_language)  # Google Web Speech API
            print(f"Rozpoznany tekst: {text}")
            return text
        except sr.UnknownValueError:
            print("Nie rozpoznano mowy")
        except sr.RequestError:
            print("Błąd połączenia z API")



    # Funkcja do przechwytywania dźwięku
    def audio_callback(self, indata, frames, time, status):
        """Przechwytuje dane audio i umieszcza je w kolejce."""
        if status:
            print(f"Status strumienia: {status}")
        self.audio_queue.put(indata.copy())

    # Funkcja do transkrypcji z Whisper
    def transcribe_audio(self, model):
        """Przetwarza dane audio z kolejki i generuje napisy."""
        print("Rozpoczęto transkrypcję...")
        audio_buffer = np.array([], dtype=np.float32)
        segment_samples = int(self.SAMPLE_RATE * self.SEGMENT_DURATION)  # Liczba próbek na segment

        # Zbieraj dane przez określony czas
        while self.running:
            try:
                # Pobierz dane z kolejki
                audio_chunk = self.audio_queue.get(timeout=2)
                # audio_buffer = np.concatenate((audio_buffer, audio_chunk.flatten()))
                if self.CHANNELS == 1:
                    audio_chunk = audio_chunk[:, 0]  # Bierzemy tylko jeden kanał
                audio_buffer = np.concatenate((audio_buffer, audio_chunk))
            
                # Jeśli zebrano wystarczająco danych na segment, transkrybuj
                if len(audio_buffer) >= segment_samples:
                    segment = audio_buffer[:segment_samples]  # Wyjmij segment
                    audio_buffer = audio_buffer[segment_samples:]  # Reszta zostaje w buforze
                    # print(f"Przetwarzam segment: {len(segment)} próbek")  # Debug
                    # Resampling do 16000 Hz
                    target_rate = 16000
                    audio_resampled = scipy.signal.resample(segment, int(len(segment) * target_rate / self.SAMPLE_RATE)).astype(np.float32)

                    # Normalizacja
                    audio_resampled = audio_resampled / np.max(np.abs(audio_resampled), initial=1)

                    # Transkrypcja
                    start_time = time.time()
                    result = model.transcribe(audio_resampled, task="transcribe", fp16=False) # , language="pl"
                    end_time = time.time()

                    translated_text = self.translator.translate(result['text'], dest='pl').text

                    print(f"Czas przetwarzania: {end_time - start_time:.2f} s")
                    # print(f"Wykryty język: {result['language']}")
                    # print(f"Tekst orginalny: {result['text']}")
                    # Tłumaczenie na polski tylko jeśli tekst nie jest pusty
                    if result['text'] and result['text'].strip():  # Sprawdzamy, czy tekst istnieje i nie jest pusty
                        try:
                            translated_text = self.translator.translate(result['text'], dest='pl').text
                            print(f"Tłumaczenie na polski: {translated_text}")

                            self.tts.speak(translated_text)
                            
                            # tts_thread = threading.Thread(target=self.tts.speak, args=(translated_text,))
                            # tts_thread.start()
                            # tts_thread.join()
                        except Exception as e:
                            print(f"Błąd tłumaczenia: {e}")
                    else:
                        print("Brak tekstu do tłumaczenia.")

                    

            except queue.Empty:
                print("Kolejka jest pusta.")
                time.sleep(0.1)
                continue  # Kontynuuj, jeśli kolejka jest pusta
            except Exception as e:
                print(f"Błąd w przetwarzaniu: {e}")

        self.tts.stop()  # Zatrzymujemy TTS po zakończeniu
        print("Zakończono przetwarzanie audio.")

    # Główna funkcja
    def start_speech_to_text(self):
        # Załaduj model Whisper

        model = whisper.load_model("base")  # Możesz użyć "base", "small", "medium", "large" dla lepszej jakości

        # Uruchom transkrypcję w osobnym wątku
        transcription_thread = threading.Thread(target=self.transcribe_audio, args=(model,))
        transcription_thread.start()

        # Uruchom przechwytywanie dźwięku
        print("Przechwytywanie dźwięku rozpoczęte...")
        stream = sd.InputStream(samplerate=self.SAMPLE_RATE, channels=self.CHANNELS, blocksize=self.BLOCK_SIZE, callback=self.audio_callback, device=10)
        
        try:
            with stream:
                # Działa, dopóki nie przerwiesz (np. Ctrl+C)
                while True:
                    time.sleep(1)  # Utrzymuj strumień aktywny
                    # print(f"Stan kolejki: {self.audio_queue.qsize()} elementów")
        except KeyboardInterrupt:
            print("Przerwano przez użytkownika.")
            self.running = False  # Zakończ przetwarzanie
        except Exception as e:
            print(f"Błąd strumienia: {e}")
            self.running = False

        # Poczekaj na zakończenie wątku
        transcription_thread.join()
        print("Zakończono.")

# if __name__ == "__main__":
#     start_speech_to_text()