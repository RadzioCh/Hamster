import os
from dotenv import load_dotenv
import json
from View.Window import Window
from Models.MistralCall import MistralCall
from Models.GeminiCall import GeminiCall

class Start():
    def __init__(self):
        self.current_text = None  # dodajemy zmienną instancji
        self.messagesBox = []
        self.model = None

    def envReed(self):
        print(f"Current model: {self.model}")
        load_dotenv()

        if self.model == "MISTRAL LARGE MODEL":
            modelKey = os.getenv('MISTRAL_API_KEY')
            modelSleep = os.getenv('MISTRAL_SLEEP')
            modelNameArray = json.loads(os.getenv('MISTRAL_MODELS'))
            modelName = modelNameArray['MISTRAL LARGE MODEL']
            modelCase = "MISTRAL"
        elif self.model == "GEMINI 1.5-FLASH-LASTEST":
            modelKey = os.getenv('GEMINI_API_KEY')
            modelSleep = os.getenv('GEMINI_SLEEP')
            modelNameArray = json.loads(os.getenv('GEMINI_MODELS'))
            modelName = modelNameArray['GEMINI 1.5-FLASH-LASTEST']
            modelCase = "GEMINI"
        else:
            return None

        return [modelKey, modelName, modelSleep, modelCase]

    def fire(self):
        def handle_send(text):
             self.current_text = text
             modelSettings = self.envReed()
             after_process = self.process(modelSettings)
             return after_process

        window = Window(on_send_callback=handle_send, start=self)
        window.WindowBox()

    def process(self, modelSettings):

        if modelSettings[3] == "MISTRAL":
            self.createDialog(modelSettings)
        elif modelSettings[3] == "GEMINI":
            self.geminiDialogGemini(modelSettings)
        else:
            print("ERROR")

        bigger_text = json.dumps(self.messagesBox)
        return bigger_text
    
    def createDialog(self, modelSettings):
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

    def geminiDialogGemini(self, modelSettings):
        modelKey = modelSettings[0]
        modelName = modelSettings[1]
        geminiCall = GeminiCall(modelKey, modelName)
        # self.messagesBox = [{
        #     "role": "user",
        #     "parts": [
        #         "Jesteś pomocnym Chomikiem. Twoja rola to pomagać w zrozumieniu problemów.",
        #     ],
        # }]
        self.messagesBox.append({"role": "user", "parts": [self.current_text],})
        responseGemini = geminiCall.GeminiDialog(self.messagesBox, self.current_text)
        self.messagesBox.append({"role": "model", "parts": [responseGemini], })

if __name__ == "__main__":
    start = Start()
    start.fire()