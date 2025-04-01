
### speech to TEXT

import speech_recognition as sr

# Inicjalizacja rozpoznawania mowy
recognizer = sr.Recognizer()

# Użycie mikrofonu do rozpoznania mowy 
with sr.Microphone() as source:
    print("Mów teraz...")
    recognizer.adjust_for_ambient_noise(source)  # Dopasowanie do szumów
    audio = recognizer.listen(source)  # Nagrywanie mowy

# Rozpoznawanie tekstu z mowy
try:
    text = recognizer.recognize_google(audio)  # Google Web Speech API
    print(f"Rozpoznany tekst: {text}")
except sr.UnknownValueError:
    print("Nie rozpoznano mowy")
except sr.RequestError:
    print("Błąd połączenia z API")



### ŁĄCZENIE


import speech_recognition as sr
from gtts import gTTS
import os

# Inicjalizacja rozpoznawania mowy
recognizer = sr.Recognizer()

# Nagrywanie mowy
with sr.Microphone() as source:
    print("Mów teraz...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

# Rozpoznawanie tekstu
try:
    text = recognizer.recognize_google(audio)
    print(f"Rozpoznany tekst: {text}")

    # Przekształcenie tekstu na mowę
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")  # Na Windowsie

except sr.UnknownValueError:
    print("Nie rozpoznano mowy")
except sr.RequestError:
    print("Błąd połączenia z API")
