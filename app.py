import os
from dotenv import load_dotenv
import json
from View.Window import Window
from Models.MistralCall import MistralCall

class Start():
    def __init__(self):
        self.current_text = None  # dodajemy zmienną instancji
        self.messagesBox = []
        self.model = None

    def envReed(self):
        load_dotenv()
        if self.model == "MISTRAL LARGE MODEL":
            modelKey = os.getenv('MISTRAL_API_KEY')
            modelSleep = os.getenv('MISTRAL_SLEEP')
            modelNameArray = json.loads(os.getenv('MISTRAL_MODELS'))
            modelName = modelNameArray['mistral-large-latest']
        elif self.model == "GEMINI":
            modelKey = os.getenv('GEMINI_API_KEY')
            modelSleep = os.getenv('GEMINI_SLEEP')
            modelNameArray = json.loads(os.getenv('GEMINI_MODELS'))
            modelName = modelNameArray['gemini-latest']
        else:
            return None

        return [modelKey, modelName, modelSleep]

    def fire(self):
        modelSettings = self.envReed()

        def handle_send(text):
             self.current_text = text
             after_process = self.process(modelSettings)
             return after_process

        window = Window(on_send_callback=handle_send)
        window.WindowBox()

    def process(self, modelSettings):

        toMessageBox = { 
            "role": "user",
            "content": self.current_text,
        }
        modelKey = modelSettings[0]
        modelName = modelSettings[1]
        mistral_call = MistralCall()
        
        self.messagesBox.append(toMessageBox)
        modelResponse = mistral_call.MistralDialog(self.messagesBox, modelName, modelKey)
        self.messagesBox.append(modelResponse)

        bigger_text = json.dumps(self.messagesBox)
        return bigger_text


if __name__ == "__main__":

    start = Start()
    start.fire()