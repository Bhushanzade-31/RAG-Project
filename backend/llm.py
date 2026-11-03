
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env from the backend directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Get API key
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found. Check your backend/.env file."
    )

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=google_api_key,
    temperature=0.1,
    max_output_tokens=1024,
)

# # Test connection
# response = llm.invoke("Explain RAG in simple words.")

# print("Gemini connected successfully!")
# print(response.content)
