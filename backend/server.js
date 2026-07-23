const express = require("express");
const cors = require("cors");
const morgan = require("morgan");

// Import routes
const queryRoutes = require("./routes/query");
const uploadRoutes = require("./routes/upload");

// Import middleware
const logger = require("./middleware/logger");
const errorHandler = require("./middleware/errorHandler");

const app = express();
const PORT = 5000;

// Built-in middleware
app.use(cors());
app.use(express.json());
app.use(morgan("dev"));

// Custom logger middleware
app.use(logger);

// API routes
app.use("/query", queryRoutes);
app.use("/upload", uploadRoutes);

// Error handling middleware (must be last)
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});