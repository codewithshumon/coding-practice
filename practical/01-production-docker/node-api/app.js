const http = require("http");

const PORT = process.env.PORT || 3000;
let isShuttingDown = false;

const server = http.createServer((req, res) => {
  if (req.url === "/health") {
    const status = isShuttingDown ? 503 : 200;
    res.writeHead(status, { "Content-Type": "application/json" });
    return res.end(
      JSON.stringify({
        status: isShuttingDown ? "shutting_down" : "ok",
        uptime: Math.floor(process.uptime()),
        pid: process.pid,
      })
    );
  }

  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(
    JSON.stringify({
      service: "prod-api-demo",
      environment: process.env.NODE_ENV || "development",
      hostname: require("os").hostname(),
    })
  );
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Server listening on port ${PORT} (pid=${process.pid})`);
});

// Graceful shutdown: stop accepting new connections, finish in-flight requests
function shutdown(signal) {
  console.log(`Received ${signal}. Starting graceful shutdown...`);
  isShuttingDown = true;

  server.close(() => {
    console.log("All connections closed. Exiting cleanly.");
    process.exit(0);
  });

  // Force exit if connections hang longer than 10s
  setTimeout(() => {
    console.error("Forced shutdown after timeout.");
    process.exit(1);
  }, 10000).unref();
}

process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));
