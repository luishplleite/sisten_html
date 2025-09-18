#!/usr/bin/env python3
import http.server
import socketserver
import os
from urllib.parse import urlparse

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add headers to prevent caching issues in Replit iframe
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        # Allow iframe embedding for Replit preview
        self.send_header('X-Frame-Options', 'ALLOWALL')
        super().end_headers()
    
    def do_GET(self):
        # Serve the main HTML file for root path
        if self.path == '/' or self.path == '/index.html':
            self.path = '/teste.html'
        return super().do_GET()

def run_server():
    PORT = 5000
    HOST = "0.0.0.0"
    
    print(f"Starting ResolvTask server on {HOST}:{PORT}")
    print(f"Access the application at: http://{HOST}:{PORT}")
    
    with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running at http://{HOST}:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_server()
