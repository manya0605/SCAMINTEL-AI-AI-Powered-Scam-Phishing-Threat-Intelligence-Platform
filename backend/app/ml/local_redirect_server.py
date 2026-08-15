from http.server import HTTPServer, BaseHTTPRequestHandler


class RedirectHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/redirect/3":
            self.send_response(302)
            self.send_header("Location", "/redirect/2")
            self.end_headers()

        elif self.path == "/redirect/2":
            self.send_response(302)
            self.send_header("Location", "/redirect/1")
            self.end_headers()

        elif self.path == "/redirect/1":
            self.send_response(302)
            self.send_header("Location", "/final")
            self.end_headers()

        elif self.path == "/final":
            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/plain"
            )
            self.end_headers()

            self.wfile.write(
                b"Final destination reached."
            )

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


server = HTTPServer(
    ("127.0.0.1", 8080),
    RedirectHandler
)

print("=" * 60)
print("SCAMINTEL LOCAL REDIRECT TEST SERVER")
print("=" * 60)
print()
print("Server running at:")
print("http://127.0.0.1:8080")
print()
print("Test URL:")
print("http://127.0.0.1:8080/redirect/3")
print()
print("Press CTRL+C to stop the server.")
print("=" * 60)

server.serve_forever()