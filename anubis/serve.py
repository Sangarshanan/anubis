from rproxy import create_proxyhandler, ThreadedHTTPServer
from strategy import Strategy


def serve(port=9000, how="round_robin"):
    """Serve the Balance."""
    server_address = ("0.0.0.0", port)
    server = getattr(Strategy, how)
    proxy_handler = create_proxyhandler(server)
    httpd = ThreadedHTTPServer(server_address, proxy_handler)
    print("🗿 Starting server, use <Ctrl-C> to stop 🗿")
    httpd.serve_forever()


if __name__ == "__main__":
    serve()
