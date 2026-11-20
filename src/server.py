"""A dependency-free web interface for the route planner.

Serves ``index.html`` and a single JSON endpoint:

    GET /api/route?from=PEK&to=BNA&metric=distance&k=3
"""

from __future__ import annotations

import json
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import networkx as nx

from src.path_finder import find_routes, network_summary

ROOT = Path(__file__).resolve().parent.parent


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, graph: nx.Graph, **kwargs):
        self.graph = graph
        super().__init__(*args, **kwargs)

    def log_message(self, fmt, *args):  # quieter console
        return

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            body = (ROOT / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if url.path == "/api/summary":
            self._json(network_summary(self.graph))
            return

        if url.path == "/api/route":
            params = parse_qs(url.query)
            origin = (params.get("from") or [""])[0].strip().upper()
            destination = (params.get("to") or [""])[0].strip().upper()
            metric = (params.get("metric") or ["distance"])[0]
            try:
                k = max(1, min(5, int((params.get("k") or ["1"])[0])))
            except ValueError:
                k = 1
            if not origin or not destination:
                self._json({"error": "give both from and to"}, 400)
                return
            try:
                routes = find_routes(self.graph, origin, destination,
                                     metric=metric, k=k)
            except KeyError as exc:
                self._json({"error": str(exc)}, 404)
                return
            except nx.NetworkXNoPath:
                self._json({"error": f"no route connects {origin} and {destination}"}, 404)
                return
            self._json({"routes": routes})
            return

        self._json({"error": "not found"}, 404)


def serve(graph: nx.Graph, port: int = 8000) -> None:
    handler = partial(Handler, graph=graph)
    server = HTTPServer(("127.0.0.1", port), handler)
    print(f"\nFlight planner running at http://127.0.0.1:{port}  (ctrl-c to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
