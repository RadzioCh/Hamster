from mistralai import Mistral
import sys
import os
import time
from dotenv import load_dotenv

class MistralCall():

    def MistralDialog(self, messagesBox, modelName, apiKey):
        # time.sleep(1)

        api_key = apiKey
        model = modelName 
        # "mistral-large-latest"
        client = Mistral(api_key=api_key)
        
        chat_response = client.chat.complete(
            model=model,
            messages=messagesBox
        )

        # print('\nMISTRAl',chat_response.choices[0].message.content)
        response = {
            "role": "assistant",
            "content": chat_response.choices[0].message.content,
        }

        return response
    
    def MistralMaind(self, contentBox):
        # time.sleep(1)

        load_dotenv()
        api_key = os.getenv("MISTRAL_API_KEY")
        model = "mistral-large-latest"
        client = Mistral(api_key=api_key)
        
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": contentBox,
                },
            ]
        )

        # print('\nMISTRAl',chat_response.choices[0].message.content)
        return chat_response.choices[0].message.content
