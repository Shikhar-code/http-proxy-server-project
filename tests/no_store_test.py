from http.server import HTTPServer, BaseHTTPRequestHandler
class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"This response must not be cached."

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)
        
server = HTTPServer(("127.0.0.1", 9003), TestHandler)
print("No-store test server running on port 9003")
server.serve_forever()