def rag_simple(query, retriever, llm, top_k=3):
    # retrieve relevant documents
    results = retriever.retrieve(query, top_k=top_k)
    context = "\n\n".join(doc["content"] for doc in results) if results else ""
    if not context:
        return "No relevant content found in the results"

    prompt = f"""Use only the following context to answer the question concisely.
If the context does not contain the answer, say so.

Context:
{context}

Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    return response.content
