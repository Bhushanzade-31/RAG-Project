from loader import data
# ---------- 2. Chunking ----------
from langchain_text_splitters import RecursiveCharacterTextSplitter

textsplitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=0,
    separators=["\n\n", "\n", " ", ""],
)
split_docs = textsplitter.split_documents(data)
print(f"Created {len(split_docs)} chunks")

if split_docs:
    print(f"Content: {split_docs[0].page_content[:100]}...")
    print(f"First chunk metadata: {split_docs[0].metadata}")
  