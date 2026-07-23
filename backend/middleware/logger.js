// Custom logger middleware
// Logs the request method and URL

const logger = (req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next(); // Pass control to the next middleware
};

module.exports = logger;