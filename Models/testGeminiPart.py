import google.generativeai as genai
import base64
from dotenv import load_dotenv
import os
import sys

messagesBox = []

def geminiCall(messagesBox, prompt, is_image=False, image_path=None):
    load_dotenv()
    modelKey = os.getenv('GEMINI_API_KEY')

    # Ustawienie swojego klucza API
    genai.configure(api_key=modelKey)
    model = genai.GenerativeModel(
                model_name='gemini-1.5-flash-latest'
            )
    chat_session = model.start_chat(
        history=messagesBox,
    )

    if is_image:
        # Jeśli to obraz, konwertujemy go na base64
        if image_path:
            with open(image_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            # Dodajemy obraz do wiadomości
            prompt = f"{{'image': '{encoded_image}', 'question': '{prompt}'}}"

    response = chat_session.send_message(prompt)
    response_text = ""

    if response.candidates:
        first_candidate = response.candidates[0]
        if first_candidate.content.parts:
            response_text = first_candidate.content.parts[0].text

    return response_text


prompt = "Ile nóg ma pies?"
messagesBox.append({"role": "user", "parts": [prompt],})
response = geminiCall(messagesBox, prompt)
print(response)

image_path = "mapa.png"  # Zamień na rzeczywistą ścieżkę do obrazu
messagesBox.append({"role": "user", "parts": ["Here is an image input"],})
response_image = geminiCall(messagesBox, "Opisz ten obraz w paru zdaniach", True, image_path)
print("Response for image:", response_image)

sys.exit()


def send_request(input_data, input_type='text'):
    # Jeśli dane to obraz, konwertujemy obraz na base64
    if input_type == 'image':
        with open(input_data, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        prompt = f"{{'image': '{encoded_image}'}}"
    elif input_type == 'text':
        # Zbuduj zapytanie z tekstem
        prompt = input_data

    # Wykonaj zapytanie do modelu
    response = genai.generate_text(prompt)
    return response

# Przykładowe użycie:
input_text = "Opisz cechy psa."
input_image_path = "path_to_image.jpg"

# Przekazanie zapytania tekstowego
response_text = send_request(input_text, 'text')
print(response_text)

# Przekazanie obrazu
# response_image = send_request(input_image_path, 'image')
# print(response_image)