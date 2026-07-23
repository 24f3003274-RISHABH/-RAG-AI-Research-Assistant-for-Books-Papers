const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");

const router = express.Router();

// Configure Multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, "../uploads"));
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

const upload = multer({ storage });

// Upload route
router.post("/", upload.single("pdf"), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "No file uploaded",
      });
    }

    const sourcePath = req.file.path;
    const dataDir = path.join(__dirname, "../../rag_engine/data");

    // Create data directory if it doesn't exist
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }

    const destinationPath = path.join(
      dataDir,
      req.file.originalname
    );

    // Copy file to rag_engine/data
    fs.copyFileSync(sourcePath, destinationPath);

    // Delete temporary file
    fs.unlinkSync(sourcePath);

    console.log("PDF copied to:", destinationPath);

    // Rebuild FAISS index
    const pythonScript = path.join(
      __dirname,
      "../../rag_engine/main.py"
    );

    const pythonProcess = spawn("python", [
      pythonScript,
      "--build",
    ]);

    let pythonError = "";

    // Capture Python errors
    pythonProcess.stderr.on("data", (data) => {
      pythonError += data.toString();
      console.error("Python Error:", data.toString());
    });

    // Capture Python output
    pythonProcess.stdout.on("data", (data) => {
      console.log("Python Output:", data.toString());
    });

    pythonProcess.on("close", (code) => {
      console.log("Python process exited with code:", code);

      if (code !== 0) {
        return res.status(500).json({
          success: false,
          message: "Failed to rebuild FAISS index",
          error: pythonError,
        });
      }

      res.json({
        success: true,
        message: "PDF uploaded and FAISS index rebuilt successfully!",
      });
    });
  } catch (error) {
    console.error("Upload Error:", error);

    res.status(500).json({
      success: false,
      message: "File upload failed",
      error: error.message,
    });
  }
});

module.exports = router;