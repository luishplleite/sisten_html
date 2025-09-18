#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
from urllib.parse import urlparse

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add headers to prevent caching issues in Replit iframe
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        # Allow iframe embedding for Replit preview
        self.send_header('X-Frame-Options', 'ALLOWALL')
        # Add CORS headers for API endpoints
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Handle API endpoints
        if self.path == '/api/supabase-url':
            self.send_json_response(os.getenv('SUPABASE_URL', ''))
            return
        elif self.path == '/api/supabase-key':
            self.send_json_response(os.getenv('SUPABASE_ANON_KEY', ''))
            return
        elif self.path == '/api/supabase-config':
            config = {
                'url': os.getenv('SUPABASE_URL', ''),
                'key': os.getenv('SUPABASE_ANON_KEY', '')
            }
            self.send_json_response(config)
            return
        
        # Handle file routing
        if self.path == '/':
            # Default to task manager dashboard
            self.path = '/teste.html'
        elif self.path == '/portfolio':
            # Portfolio page
            self.path = '/index.html'
        
        return super().do_GET()
    
    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200)
        self.end_headers()
    
    def send_json_response(self, data):
        """Send a JSON response"""
        response = json.dumps(data)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

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
