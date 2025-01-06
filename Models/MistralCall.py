from mistralai import Mistral

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