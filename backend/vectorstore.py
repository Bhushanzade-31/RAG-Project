#VectorStore
from embedding import embedding_manager
from chunking import split_docs
import os
import time
import uuid
from typing import List, Any

import numpy as np
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

load_dotenv()


class VectorStore:
    def __init__(self, collection_name: str = "movies_collection", db_name: str = "movies_db",
                 index_name: str = "movies_vector_index"):
        self.collection_name = collection_name
        self.db_name = db_name
        self.index_name = index_name
        self.client = None
        self.collection = None
        self._initialize_mongo_client()

    def _initialize_mongo_client(self):
        try:
            mongo_uri = os.getenv("MONGODB_URI")
            if not mongo_uri:
                raise ValueError("MONGODB_URI is not set (put your Atlas connection string in .env)")

            self.client = MongoClient(mongo_uri)
            self.client.admin.command("ping")

            self.collection = self.client[self.db_name][self.collection_name]
            print(f"MongoDB client initialized. Collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count_documents({})}")
        except Exception as e:
            print(f"Error initializing MongoDB client: {e}")
            raise

    def _ensure_vector_index(self, dimensions: int):
        """Create the Atlas vector search index (cosine) if it doesn't exist."""
        existing = [idx["name"] for idx in self.collection.list_search_indexes()]
        if self.index_name in existing:
            return

        model = SearchIndexModel(
            name=self.index_name,
            type="vectorSearch",
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "numDimensions": dimensions,
                        "similarity": "cosine",
                    }
                ]
            },
        )
        self.collection.create_search_index(model=model)
        print(f"Creating vector index '{self.index_name}' (may take ~1 minute)...")

        while True:
            idx = next(iter(self.collection.list_search_indexes(self.index_name)), None)
            if idx and idx.get("queryable"):
                break
            time.sleep(5)
        print("Vector index is ready.")

    @staticmethod
    def _clean_metadata(meta: dict) -> dict:
        """Keep only simple values (str, int, float, bool)."""
        cleaned = {}
        for k, v in meta.items():
            if isinstance(v, (str, int, float, bool)):
                cleaned[k] = v
            elif v is not None:
                cleaned[k] = str(v)
        return cleaned

    def add_documents(self, documents: List[Any], embeddings: np.ndarray):
        if len(documents) != len(embeddings):
            raise ValueError("Documents and embeddings must have the same length.")
        print(f"Adding {len(documents)} documents to the collection.")

        records = []

        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            meta = self._clean_metadata(dict(doc.metadata))
            meta["content_length"] = len(doc.page_content)

            records.append({
                "_id": f"doc_{uuid.uuid4().hex[:8]}_{i}",
                "text": doc.page_content,
                "metadata": meta,
                "embedding": emb.tolist(),
            })

        batch_size = 500

        try:
            for start in range(0, len(records), batch_size):
                end = start + batch_size
                self.collection.insert_many(records[start:end])
                print(f"Added {min(end, len(records))}/{len(records)}")
            print(f"Total documents in collection: {self.collection.count_documents({})}")
        except Exception as e:
            print(f"Error adding documents to collection: {e}")
            raise


vectorstore = VectorStore()

# Fill the DB only the first time (collection empty), so reruns don't duplicate data
if vectorstore.collection.count_documents({}) == 0:
    chunks = split_docs
    print("length of chunks:", len(chunks))

    texts = [doc.page_content for doc in chunks]
    embeddings = embedding_manager.generate_embeddings(texts)

    vectorstore.add_documents(chunks, embeddings)
    vectorstore._ensure_vector_index(len(embeddings[0]))
else:
    # data already there: just make sure the index exists too
    sample = vectorstore.collection.find_one({}, {"embedding": 1})
    vectorstore._ensure_vector_index(len(sample["embedding"]))