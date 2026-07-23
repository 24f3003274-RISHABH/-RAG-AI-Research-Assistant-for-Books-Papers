import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function Results({ message }) {
  return (
    <div className={`message ${message.sender}`}>
      <strong className="sender">
        {message.sender === "user" ? "You:" : "AI:"}
      </strong>

      {/* Render Markdown properly */}
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {message.text}
      </ReactMarkdown>
    </div>
  );
}

export default Results;