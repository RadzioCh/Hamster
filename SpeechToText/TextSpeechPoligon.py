import sys
sys.path.append('C:\\Hamster\\SpeechToText')
from TextToSpeech import TextToSpeech
from SpeechToText import SpeechToText

import sounddevice as sd
# print(sd.query_devices())
# device_info = sd.query_devices(10, 'input')
# print(device_info)
# sys.exit(0)

# textToSpeech = TextToSpeech()
# textToSpeech.text_to_speech("Cześć nazywam się pająk.");


speechToText = SpeechToText()
# speechToText.start_speech()
speechToText.start_speech_to_text()

