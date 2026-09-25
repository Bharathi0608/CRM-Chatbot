from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sql_chatbot import ask_crm


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="CRM AI SQL Chatbot",
    description="AI-powered CRM Text-to-SQL chatbot",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    question: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "CRM AI SQL Chatbot API is running"
    }


# ============================================================
# CHAT API
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:

        return {
            "success": False,
            "error": "Question cannot be empty."
        }

    try:

        result = ask_crm(question)

        return {
            "success": True,
            "question": result["question"],
            "sql": result["sql"],
            "result": result["result"],
            "answer": result["answer"]
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }