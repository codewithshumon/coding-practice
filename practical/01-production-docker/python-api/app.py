from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import signal
import socket
import sys
import threading
import time

PORT = int(os.environ.get("PORT", "5000"))
START_TIME = time.time()
is_shutting_down = False


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 503 if is_shutting_down else 200
            body = {
                "status": "shutting_down" if is_shutting_down else "ok",
                "uptime": int(time.time() - START_TIME),
                "pid": os.getpid(),
            }
        else:
            status = 200
            body = {
                "service": "python-api",
                "language": "python",
                "environment": os.environ.get("ENV", "production"),
                "hostname": socket.gethostname(),
            }

        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        sys.stdout.write(f"[python-api] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()


server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)


def shutdown(signum, _frame):
    global is_shutting_down
    print(f"Received signal {signum}. Starting graceful shutdown...", flush=True)
    is_shutting_down = True
    threading.Thread(target=server.shutdown, daemon=True).start()


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

print(f"Python API listening on port {PORT} (pid={os.getpid()})", flush=True)
server.serve_forever()
server.server_close()
print("All connections closed. Exiting cleanly.", flush=True)
