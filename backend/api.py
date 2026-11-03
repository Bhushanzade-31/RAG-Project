# from fastapi import FastAPI, Query
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel
# from retriever import rag_retriever
# from llm import llm
# from rag import rag_simple

# app = FastAPI()


# class AskRequest(BaseModel):
#     question: str
#     top_k: int = 5


# PAGE = """
# <!DOCTYPE html>
# <html>
# <head><title>Movie RAG</title></head>
# <body style="font-family:sans-serif;max-width:600px;margin:40px auto">
#   <h2>Ask about movies</h2>
#   <input id="q" style="width:75%;padding:8px" placeholder="Search for movies...">
#   <button onclick="ask()" style="padding:8px">Ask</button>
#   <p id="out" style="white-space:pre-wrap"></p>
#   <script>
#     document.getElementById("q").addEventListener("keydown", e => { if (e.key === "Enter") ask(); });
#     async function ask() {
#       const q = document.getElementById("q").value.trim();
#       if (!q) return;
#       const out = document.getElementById("out");
#       out.textContent = "Thinking...";
#       const r = await fetch("/api/ask", {
#         method: "POST",
#         headers: {"Content-Type": "application/json"},
#         body: JSON.stringify({question: q})
#       });
#       const d = await r.json();
#       out.textContent = d.answer || JSON.stringify(d);
#     }
#   </script>
# </body>
# </html>
# """


# @app.get("/", response_class=HTMLResponse)
# def home():
#     return PAGE


# @app.get("/api/ask")
# def ask_get(q: str = Query(..., min_length=1), top_k: int = Query(5, ge=1, le=10)):
#     return {"answer": rag_simple(q, rag_retriever, llm, top_k=top_k)}


# @app.post("/api/ask")
# def ask_post(body: AskRequest):
#     return {"answer": rag_simple(body.question, rag_retriever, llm, top_k=body.top_k)}
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from retriever import rag_retriever
from llm import llm
from rag import rag_simple

app = FastAPI()

# Lets the React dev server (Vite) call this API directly.
# Not needed if you use the Vite proxy, but harmless to keep.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/api/ask")
def ask_get(q: str = Query(..., min_length=1), top_k: int = Query(5, ge=1, le=10)):
    return {"answer": rag_simple(q, rag_retriever, llm, top_k=top_k)}


@app.post("/api/ask")
def ask_post(body: AskRequest):
    return {"answer": rag_simple(body.question, rag_retriever, llm, top_k=body.top_k)}


# Serve the built React app (run `npm run build` and copy `dist` next to this file).
# This must stay at the bottom, after all /api routes.
DIST = Path(__file__).parent / "dist"
if DIST.exists():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="frontend")