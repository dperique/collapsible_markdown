#!/usr/bin/env python3

import http.server
import socketserver
import markdown
import os
import signal
import sys
import threading
from typing import Optional
from types import FrameType
from html_templates.html_templates import get_html_template

PORTS: list[int] = [8001, 8002, 8003]
httpd: Optional[socketserver.TCPServer] = None

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.endswith(".md"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file_path = self.path[1:]
            with open(file_path, 'r') as file:
                markdown_content = file.read()

                # Handle fenced code blocks and syntax highlighting for
                # examples in the markdown files.
                html_content = markdown.markdown(
                    markdown_content,
                    extensions=['fenced_code', 'codehilite']
                )

            html_template = get_html_template(html_content)
            self.wfile.write(html_template.encode('utf-8'))
        else:
            super().do_GET()

def signal_handler(sig: int, frame: Optional[FrameType]) -> None:
    print('Shutting down the server...')
    if httpd:
        httpd.shutdown()
    sys.exit(0)

# Attempt to run the server on the specified port.
# Return True if the server is successfully started, False otherwise.
def run_server(port: int) -> bool:
    global httpd
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving at port {port}")
            httpd.serve_forever()
    except OSError as e:
        print(f"Port {port} is unavailable ({e}), trying next port.")
        return False
    return True

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    # Strobe through the specified ports until one is available to
    # avoid having to deal with leaked ports during debugging.
    for port in PORTS:
        server_thread = threading.Thread(target=run_server, args=(port,))
        server_thread.start()
        server_thread.join()
        if httpd:
            break
    else:
        print("All specified ports are unavailable.")
        sys.exit(1)
