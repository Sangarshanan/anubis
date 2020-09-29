"""Reverse Proxy."""
import logging
import http.server  
import socketserver
from socketserver import ThreadingMixIn
from requests import Session

from strategy import strategy

logger = logging.getLogger("anubis")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class Handler(http.server.BaseHTTPRequestHandler):
    session = Session()
    def do_GET(self):
        server = strategy.round_robin()
        print(server.url, "\n")
        resp = self.session.get(server.url, allow_redirects=True)
        self.send_response(resp.status_code)
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()
        self.wfile.write(resp.content)

    def do_POST(self):
        server = strategy.round_robin()
        print(server.url, "\n")
        resp = self.session.post(server.url,data={},allow_redirects=True)
        self.send_response(resp.status_code)
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()
        self.wfile.write(resp.content)
        self.resp = resp

class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
  """ Make our HTTP server multi-threaded """

def serve():
    httpd = ThreadedHTTPServer(('', 9000), Handler)
    httpd.serve_forever()

if __name__ == '__main__':
    serve()
