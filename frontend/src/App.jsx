import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          question: userQuestion,
        }
      );

      const data = response.data;

      if (!data.success) {
        setMessages((prev) => [
          ...prev,
          {
            type: "error",
            text: data.error || "Something went wrong.",
          },
        ]);

        return;
      }

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          answer: data.answer,
          sql: data.sql,
          result: data.result,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          type: "error",
          text: "Unable to connect to the backend server. Make sure FastAPI is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };

  const useQuestion = (text) => {
    setQuestion(text);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="logo">
          <div className="logo-icon">🤖</div>

          <div>
            <h2>CRM AI</h2>
            <span>SQL Assistant</span>
          </div>
        </div>

        <button className="new-chat" onClick={clearChat}>
          + New Chat
        </button>

        <div className="sidebar-section">

          <p className="section-title">
            SUGGESTED QUESTIONS
          </p>

          <button
            onClick={() =>
              useQuestion("How many companies are in the database?")
            }
          >
            📊 Total companies
          </button>

          <button
            onClick={() =>
              useQuestion("Which company has the highest revenue?")
            }
          >
            💰 Highest revenue
          </button>

          <button
            onClick={() =>
              useQuestion("Which company has the most employees?")
            }
          >
            👥 Most employees
          </button>

          <button
            onClick={() =>
              useQuestion("Show the top 5 companies by revenue.")
            }
          >
            🏆 Top 5 companies
          </button>

          <button
            onClick={() =>
              useQuestion("How many companies are in each sector?")
            }
          >
            📈 Companies by sector
          </button>

        </div>

        <div className="database-card">
          <div className="status-dot"></div>

          <div>
            <strong>CRM Database</strong>
            <span>PostgreSQL • 85 records</span>
          </div>
        </div>

      </aside>


      {/* MAIN CONTENT */}
      <main className="main">

        {/* HEADER */}
        <header className="header">

          <div>
            <h1>CRM AI Assistant</h1>

            <p>
              Ask questions about your CRM data in natural language.
            </p>
          </div>

          <div className="connection">
            <span className="online-dot"></span>
            Connected
          </div>

        </header>


        {/* CHAT AREA */}
        <section className="chat-area">

          {messages.length === 0 && (

            <div className="welcome">

              <div className="welcome-icon">
                🤖
              </div>

              <h2>
                Ask anything about your CRM
              </h2>

              <p>
                Ask questions in natural language. The AI will
                generate SQL, query your CRM database, and explain
                the result.
              </p>

              <div className="examples">

                <button
                  onClick={() =>
                    useQuestion(
                      "How many companies are in the database?"
                    )
                  }
                >
                  How many companies are there?
                </button>

                <button
                  onClick={() =>
                    useQuestion(
                      "Which company has the highest revenue?"
                    )
                  }
                >
                  Highest revenue?
                </button>

                <button
                  onClick={() =>
                    useQuestion(
                      "Show the top 5 companies by revenue."
                    )
                  }
                >
                  Top 5 companies
                </button>

              </div>

            </div>

          )}


          {/* MESSAGES */}
          {messages.map((message, index) => (

            <div
              key={index}
              className={`message-row ${message.type}`}
            >

              {/* USER MESSAGE */}
              {message.type === "user" && (

                <div className="user-message">
                  {message.text}
                </div>

              )}


              {/* AI MESSAGE */}
              {message.type === "assistant" && (

                <div className="assistant-message">

                  <div className="assistant-title">
                    <span className="bot-icon">
                      🤖
                    </span>

                    CRM AI
                  </div>

                  <div className="answer markdown-content">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {message.answer}
                    </ReactMarkdown>
                  </div>

                  <details>
                    <summary>
                      View Generated SQL
                    </summary>

                    <pre>
                      {message.sql}
                    </pre>
                  </details>

                  <details>
                    <summary>
                      View Database Result
                    </summary>

                    <pre>
                      {message.result}
                    </pre>
                  </details>

                </div>

              )}


              {/* ERROR */}
              {message.type === "error" && (

                <div className="error-message">
                  ⚠️ {message.text}
                </div>

              )}

            </div>

          ))}


          {/* LOADING */}
          {loading && (

            <div className="message-row assistant">

              <div className="assistant-message">

                <div className="assistant-title">
                  <span className="bot-icon">
                    🤖
                  </span>

                  CRM AI
                </div>

                <div className="typing">
                  <span></span>
                  <span></span>
                  <span></span>

                  Thinking...
                </div>

              </div>

            </div>

          )}

        </section>


        {/* INPUT */}
        <div className="input-section">

          <div className="input-box">

            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask something about your CRM data..."
              rows="1"
              disabled={loading}
            />

            <button
              onClick={askQuestion}
              disabled={loading || !question.trim()}
              className="send-button"
            >
              {loading ? "..." : "➤"}
            </button>

          </div>

          <p className="input-hint">
            CRM AI converts natural-language questions into SQL.
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;