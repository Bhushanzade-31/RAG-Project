# PeopleDesk – HR Knowledge Assistant 🤖

PeopleDesk is an AI-powered HR chatbot that answers employee questions in natural language using **Retrieval-Augmented Generation (RAG)**. It retrieves relevant information from HR datasets using a vector database and generates context-aware responses.

## 🚀 Tech Stack

- **Frontend:** React.js, Vite, CSS
- **Backend:** Python, FastAPI
- **AI:** RAG, LLM, Text Embeddings
- **Database:** Vector Database
- **Dataset:** HRDataset_v14.csv

## ✨ Features

- AI-powered HR question answering.
- RAG-based document retrieval.
- Semantic search using vector embeddings.
- Interactive chat interface.
- Chat history and copy answers.
- Adjustable document retrieval (`top_k`).
- Responsive design.

## 📂 Project Structure

```text
PeopleDesk/
├── backend/
│   ├── HRDataset_v14.csv
│   ├── HRDataset_v14_short.csv
│   ├── loader.py
│   ├── vectorstore.py
│   ├── retriever.py
│   ├── llm.py
│   ├── rag.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── vite.config.js
│   └── package.json
│
└── README.md
```

## ⚙️ Installation & Setup

**Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## 🔄 How It Works

1. User asks an HR-related question.
2. FastAPI receives the question.
3. RAG retrieves relevant HR information from the vector database.
4. LLM generates an answer using the retrieved context.
5. React displays the response.

## 👨‍💻 Author

**Bhushan Prabhakar Zade**

GitHub: [Bhushanzade-31](https://github.com/Bhushanzade-31)

---

⭐ **PeopleDesk – Making HR Information Accessible Through AI.**
