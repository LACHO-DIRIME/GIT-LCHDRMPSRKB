"""ELPULSAR — entry point · servidor HTTP · puerto 8741"""
from __future__ import annotations
import sys, json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, str(Path(__file__).parent))
from core.neural_net import build_graph
from core.resources import (get_all, create, verify, connect,
                             ResourceType, ResourceScope)
from tools.paper import render_html
from tools.key import index, summary
from tools.sprint import get_sprint

PORT = 8741

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        p = self.path
        if p == "/":
            b = (Path(__file__).parent/"ui"/"index.html").read_bytes()
            self._send(200, b, "text/html")
        elif p == "/api/graph":     self._json(build_graph())
        elif p == "/api/resources": self._json(get_all())
        elif p == "/api/key":       self._json(index())
        elif p == "/api/key/summary": self._json(summary())
        elif p == "/api/paper":
            self._send(200, render_html().encode(), "text/html")
        elif p == "/api/sprint":
            self._json(get_sprint())
        elif p == "/api/sync":
            from core.resources import sync_from_ledger
            self._json(sync_from_ledger())
        else: self._send(404, b"not found", "text/plain")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        p = self.path
        if p == "/api/resources":
            r = create(body["title"],
                ResourceType[body.get("type","DATA").upper()],
                ResourceScope[body.get("scope","PROPIO").upper()],
                content=body.get("content",""),
                cluster=body.get("cluster","#CORE"))
            self._json(r)
        elif p == "/api/verify":
            self._json({"ok": verify(body["id"])})
        elif p == "/api/connect":
            self._json(connect(body["source"], body["target"],
                               body.get("relation","DEPENDE_DE")))
        else: self._send(404, b"not found", "text/plain")

    def _json(self, data):
        b = json.dumps(data, ensure_ascii=False).encode()
        self._send(200, b, "application/json")

    def _send(self, code, body, ct):
        self.send_response(code)
        self.send_header("Content-Type", ct)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    from core.resources import sync_from_ledger
    r = sync_from_ledger()
    print(f"  ↳ sync: {r['crystals']} cristales · {r['tasks']} tareas")
    print(f"⚡ ELPULSAR → http://localhost:{PORT}")
    HTTPServer(("", PORT), Handler).serve_forever()
