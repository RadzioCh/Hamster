import os
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_LOG_SEVERITY_LEVEL"] = "ERROR"
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse

class GeminiCall:
    def __init__(self, api_key, model_name='gemini-1.5-flash-latest', temperature=1, top_p=0.95, top_k=40, max_output_tokens=8192, response_mime_type="text/plain"):
        """Inicjalizacja klucza API i modelu."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
                "response_mime_type": response_mime_type,
            }
        )

    def GeminiDialog(self, messagesBox, prompt):
        """
        Prowadzi dialog z modelem Gemini.

        Args:
          messagesBox: Lista historii konwersacji (messages).
          prompt: Wiadomość użytkownika.

        Returns:
            Tekst z odpowiedzi lub pusty string w przypadku braku odpowiedzi.
        """

        chat_session = self.model.start_chat(
            history=messagesBox,
        )
        
        response = chat_session.send_message(prompt)
        response_text = ""

        if response.candidates:
            first_candidate = response.candidates[0]
            if first_candidate.content.parts:
                response_text = first_candidate.content.parts[0].text

        return response_text