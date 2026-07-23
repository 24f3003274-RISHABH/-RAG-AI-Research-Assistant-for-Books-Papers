const express = require("express");
const { spawn } = require("child_process");
const path = require("path");

const router = express.Router();

// POST /query
router.post("/", (req, res) => {
  const { query } = req.body;

  if (!query) {
    return res.status(400).json({
      success: false,
      message: "Query is required",
    });
  }

  // Path to Python RAG script
  const pythonScript = path.join(
    __dirname,
    "../../rag_engine/main.py"
  );

  // Run Python script
  const pythonProcess = spawn("python", [pythonScript, query]);

  let result = "";
  let error = "";

  // Capture normal output
  pythonProcess.stdout.on("data", (data) => {
    result += data.toString();
  });

  // Capture warnings/errors
  pythonProcess.stderr.on("data", (data) => {
    error += data.toString();
    console.warn("Python stderr:", data.toString());
  });

  // When Python process finishes
  pythonProcess.on("close", (code) => {
    // Only fail if Python exits with non-zero code
    if (code !== 0) {
      return res.status(500).json({
        success: false,
        message: "Python RAG engine failed",
        error,
      });
    }

    // Success response
    res.json({
      success: true,
      answer: result,
      warning: error || null, // Send warnings separately
    });
  });
});

module.exports = router;