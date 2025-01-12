
from GeminiCall import GeminiCall
from dotenv import load_dotenv
import os


load_dotenv()
modelKey = os.getenv('GEMINI_API_KEY')
geminiCall = GeminiCall(modelKey)

messagesBox = [{
      "role": "user",
      "parts": [
        "Jesteś pomocnym Chomikiem. Twoja rola to pomagać w zrozumieniu problemów.",
      ],
    }]

while True:
    prompt = input("Pytanie: ")

    messagesBox.append({"role": "user", "parts": [prompt],})

    responseGemini = geminiCall.GeminiDialog(messagesBox, prompt)
    print("GEMINI: ", responseGemini)
    messagesBox.append({"role": "model", "parts": [responseGemini], })

    print("\033[94m" + str(messagesBox) + "\033[0m")

# prompt = "Ile nóg mają mrówki?"
# responseGemini = geminiCall.GeminiDialog(messagesBox, prompt)
# print(responseGemini)