import os
from dotenv import load_dotenv
import json
from View.Window import Window
from Models.MistralCall import MistralCall
from Models.GeminiCall import GeminiCall
from Database.DatabaseConnect import DatabaseConnect
from Entity.Models import Models
import sys
from Prompts.FirstPrompts import FirstPrompts


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
        firstPrompt = self.firstPrompt()
        if modelSettings[3] == "MISTRAL":
            if not self.messagesBox:
                self.messagesBox.append({"role": "user", "content": firstPrompt,})
            self.createDialog(modelSettings)
        elif modelSettings[3] == "GEMINI":

            if not self.messagesBox:
                self.messagesBox.append({"role": "user", "parts": [firstPrompt],})
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
        
        self.messagesBox.append({"role": "user", "parts": [self.current_text],})
        responseGemini = geminiCall.GeminiDialog(self.messagesBox, self.current_text)
        self.messagesBox.append({"role": "model", "parts": [responseGemini], })

        print("\033[94m" + str(self.messagesBox) + "\033[0m")

    def firstPrompt(self):
        firstPrompts = FirstPrompts()
        return firstPrompts.initPrompts()
    
    
        # databaseConnect = DatabaseConnect()
        # sessionDb = databaseConnect.DbConnect()
        # models = Models()
        # globals = models.createModels()

        # initial_prompts = globals.get('Initial_prompts')
        # result = sessionDb.query(initial_prompts).filter(initial_prompts.prompt_name == "basic").all()

        # current_datetime = datetime.now()
        # prompt = f"Today is {current_datetime}. "
        # for row in result:
        #     prompt += row.prompt+"\n"

        # sessionDb.commit()
        # sessionDb.close()

        # print(prompt)
        
        # return prompt

if __name__ == "__main__":
    start = Start()
    start.fire()