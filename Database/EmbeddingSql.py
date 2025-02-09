from sentence_transformers import SentenceTransformer

class EmbeddingSql():

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Ładowanie modelu

    def get_embedding_to_text(self, text):
        vector = self.model.encode(text).tolist()
        return f"[{','.join(map(str, vector))}]"  # Konwersja na format tekstowy
    
