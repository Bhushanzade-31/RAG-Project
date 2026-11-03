
import numpy as np
from sentence_transformers import SentenceTransformer
import uuid
import chromadb
from chromadb.config import Settings
from typing import List , Dict , Any , Tuple
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None 
        self._load_model()

    def _load_model(self):
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model loaded successfully.: {self.model.get_embedding_dimension()}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if not self.model:
            raise ValueError("Model is not loaded.")
        print(f"Generating embeddings for {len(texts)} texts.")    
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        print(f"Generated embeddings shape: {embeddings.shape}")
        return embeddings
    
embedding_manager = EmbeddingManager()
embedding_manager
