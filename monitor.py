import json
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen

history = deque(maxlen=120)
lock = threading.Lock()

def probe():
    while True:
        start = time.monotonic()
        try:
            with urlopen("http://web/", timeout=3) as response:
                status = response.status
            ok = 200 <= status < 400
        except Exception:
            status, ok = None, False
        with lock:
            history.append({"timestamp": time.time(), "ok": ok, "status": status,
                            "latency_ms": round((time.monotonic()-start)*1000, 2)})
        time.sleep(5)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        with lock:
            samples = list(history)
        body = json.dumps({"samples": samples, "success_rate":
                           sum(s["ok"] for s in samples)/len(samples) if samples else None}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    threading.Thread(target=probe, daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
