import React from "react";

function Results({ message }) {
  return (
    <div className={`message ${message.sender}`}>
      <strong>
        {message.sender === "user" ? "You:" : "AI:"}
      </strong>

      <p>{message.text}</p>
    </div>
  );
}

export default Results;