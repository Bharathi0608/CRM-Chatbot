# CRM-Chatbot (SQL AI Chatbot)

This project is an AI-powered CRM text-to-SQL chatbot. It allows users to ask natural language questions about CRM data and automatically generates PostgreSQL/SQLite queries, executes them, and translates the result back into a natural language response.

The project is split into two parts:
- **Backend:** A FastAPI server powered by LangChain and Groq LLM API.
- **Frontend:** A React web application built with Vite.

## 🖥️ Application Preview

<p align="center">
  <img src="frontend/src/assets/CRM%20AI%20Assistant.png"
     alt="CRM AI Assistant Dashboard"
     width="100%">
</p>

> **CRM AI Assistant** — Ask questions about your CRM data using natural language. The AI converts user questions into SQL, queries the PostgreSQL database, and explains the results.

```text
crm-sql-chatbot/
│
├── backend/            # FastAPI python backend
│   ├── main.py         # FastAPI application and endpoints
│   ├── sql_chatbot.py  # LangChain integration, SQL generation and validation
│   ├── database.py     # Database connection and tools
│   └── ...
│
├── frontend/           # React frontend built with Vite
│   ├── src/            # React components and styles
│   ├── package.json    # Node dependencies and scripts
│   └── ...
│
└── data/               # Data directory
    └── accounts.csv    # Source data for the database
```

## Setup Instructions

### 1. Backend Setup

The backend requires Python and relies on a virtual environment.

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (if not already done):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install fastapi uvicorn langchain langchain-groq langchain-community python-dotenv pydantic
   ```
   *(Note: Ensure you have `langchain_community` installed if you encounter `ModuleNotFoundError: No module named 'langchain_community'`)*

4. Create a `.env` file in the `backend/` directory with your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://127.0.0.1:8000`.

### 2. Frontend Setup

The frontend is a React app using Vite.

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend will be accessible (usually at `http://localhost:5173`).

## Usage

Once both the backend and frontend servers are running, open your browser to the frontend's local URL. You can type natural language questions like:
- "How many accounts are there?"
- "Show me the top 5 accounts by revenue."
- "What is the average revenue?"

The AI will parse your question, query the CRM database safely (read-only SELECT queries), and return the results as a chat message.
