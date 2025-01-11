
from GeminiCall import GeminiCall

geminiCall = GeminiCall('AIzaSyBHCCbrfXSvgXH7aAQhJW1Ubvyl95epTwM')

messagesBox = [{
      "role": "user",
      "parts": [
        "Jesteś pomocnym Chomikiem. Twoja rola to pomagać w zrozumieniu problemów.",
      ],
    }]

prompt = "Ile nóg mają mrówki?"
responseGemini = geminiCall.GeminiDialog(messagesBox, prompt)

print(responseGemini)