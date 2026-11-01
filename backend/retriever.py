from vectorstore import vectorstore
from embedding import embedding_manager
# RAG retriver
from typing import List, Dict, Any


class RAGRetriever:
    def __init__(self, vectorstore, embedding_manager):
        self.vectorstore = vectorstore
        self.embedding_manager = embedding_manager

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Dict[str, Any]]:
        print(f"Retrieving documents for query: '{query}' "
              f"with top_k={top_k} and score_threshold={score_threshold}")

        # Generate query embedding
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]

        try:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": self.vectorstore.index_name,
                        "path": "embedding",
                        "queryVector": query_embedding.tolist(),
                        "numCandidates": max(100, top_k * 20),
                        "limit": top_k,
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "text": 1,
                        "metadata": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
            ]
            results = list(self.vectorstore.collection.aggregate(pipeline))

            retrieved_docs = []

            for doc in results:
                # Atlas cosine score is normalised to (1 + cos) / 2, so convert back
                similarity_score = 2 * doc["score"] - 1
                distance = 1 - similarity_score  # cosine distance, same as Chroma

                if similarity_score >= score_threshold:
                    retrieved_docs.append({
                        "id": doc["_id"],
                        "content": doc["text"],
                        "metadata": doc["metadata"],
                        "distance": distance,
                        "similarity_score": similarity_score,
                    })

            if retrieved_docs:
                # Contiguous ranks after filtering
                for rank, d in enumerate(retrieved_docs, start=1):
                    d["rank"] = rank
                print(f"Retrieved {len(retrieved_docs)} documents after applying score threshold.")
            else:
                print("No documents found in the results.")

            return retrieved_docs

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []


rag_retriever = RAGRetriever(vectorstore, embedding_manager)