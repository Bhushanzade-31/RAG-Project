from llm import llm
from rag import rag_simple
from retriever import rag_retriever


def main():
    query = "Which movies involve time travel?"

    # Inspect raw retrieval
    results = rag_retriever.retrieve(query, top_k=3)
    for r in results:
        print(
            r["rank"],
            r["metadata"].get("title"),
            round(r["distance"], 3),
            round(r["similarity_score"], 3),
        )

    # Full RAG answer
    print("\nAnswer:", rag_simple(query, rag_retriever, llm, top_k=3))


if __name__ == "__main__":
    main()