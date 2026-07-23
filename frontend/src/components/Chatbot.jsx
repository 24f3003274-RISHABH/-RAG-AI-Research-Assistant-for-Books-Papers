import React, { useState } from "react";
import axios from "axios";
import Results from "./Results.jsx";

function Chatbot() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Send query to backend
  const handleSend = async () => {
    if (!query.trim()) return;

    // Add user message to chat
    const userMessage = { sender: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://localhost:5000/query",
        { query }
      );

      // Add AI response to chat
      const aiMessage = {
        sender: "ai",
        text: response.data.answer,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "Error: Unable to get response from the server.",
        },
      ]);
    } finally {
      setLoading(false);
      setQuery("");
    }
  };

  return (
    <div className="chat-container">
      <h2>Ask Questions</h2>

      {/* Chat Messages */}
      <div className="chat-box">
        {messages.map((msg, index) => (
          <Results key={index} message={msg} />
        ))}

        {/* Loading message */}
        {loading && (
          <div className="message ai">
            Thinking...
          </div>
        )}
      </div>

      {/* Input Section */}
      <div className="input-container">
        <input
          type="text"
          placeholder="Ask something from your books or papers..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />

        <button onClick={handleSend} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default Chatbot;