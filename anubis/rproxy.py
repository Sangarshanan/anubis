"""Reverse Proxy Based on https://github.com/MollardMichael/python-reverse-proxy."""

import sys
import requests
from urllib.parse import urlparse
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer


def create_proxyhandler(server):
    class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def __init__(self, *args, **kwargs):
            super(ProxyHTTPRequestHandler, self).__init__(*args, **kwargs)

        def do_HEAD(self):
            self.do_GET(body=False)

        def do_GET(self, body=True):
            domain = server().url
            hostname = urlparse(domain).netloc
            url = f"{domain}{self.path}"
            try:
                req_header = self.fetch_headers(hostname)
                resp = requests.get(url, headers=req_header)
                self.send_response(resp.status_code)
                self.send_resp_headers(resp)
                if body:
                    self.wfile.write(resp.content)
                return
            except Exception as e:
                self.send_error(404, str(e))

        def do_POST(self, body=True):
            domain = server().url
            hostname = urlparse(domain).netloc
            url = f"{domain}{self.path}"
            try:
                content_len = int(self.headers.get("content-length", 0))
                post_body = self.rfile.read(content_len)
                req_header = self.fetch_headers(hostname)

                resp = requests.post(url, data=post_body, headers=req_header)

                self.send_response(resp.status_code)
                self.send_resp_headers(resp)
                if body:
                    self.wfile.write(resp.content)
                return
            except Exception as e:
                self.send_error(404, str(e))

        def fetch_headers(self, hostname):
            proxy_header = dict(self.headers._headers)
            proxy_header["Host"] = hostname
            return proxy_header

        def send_resp_headers(self, resp):
            respheaders = resp.headers
            for key in respheaders:
                if key not in [
                    "Content-Encoding",
                    "Transfer-Encoding",
                    "content-encoding",
                    "transfer-encoding",
                    "content-length",
                    "Content-Length",
                ]:
                    self.send_header(key, respheaders[key])
            self.send_header("Content-Length", len(resp.content))
            self.end_headers()

    return ProxyHTTPRequestHandler


# Spin up Multiple threads to handle requests.


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
