import React, { useState } from "react";
import UploadBooks from "./components/UploadBooks.jsx";
import Chatbot from "./components/Chatbot.jsx";
import "./App.css";

function App() {
  // Store uploaded file status
  const [uploadMessage, setUploadMessage] = useState("");

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>AI Research Assistant</h1>
        <p>Upload books & papers, then ask questions using RAG</p>
      </header>

      {/* Upload PDF Section */}
      <UploadBooks setUploadMessage={setUploadMessage} />

      {/* Show upload status */}
      {uploadMessage && (
        <div className="upload-message">
          {uploadMessage}
        </div>
      )}

      {/* Chatbot Section */}
      <Chatbot />
    </div>
  );
}

export default App;