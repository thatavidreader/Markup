from http.server import HTTPServer
from markdown_converter import MarkdownHTTPRequestHandler

def run(server_class=HTTPServer, handler_class=MarkdownHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()