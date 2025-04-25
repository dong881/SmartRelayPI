#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
from datetime import datetime
import urllib.parse
import requests
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock data
relay_status = "關閉"  # Initial state
logs = [
    {"timestamp": "2025-03-14 15:30:45", "status": "開啟"},
    {"timestamp": "2025-03-14 15:35:22", "status": "關閉"},
    {"timestamp": "2025-03-14 16:10:05", "status": "開啟"},
    {"timestamp": "2025-03-14 16:45:18", "status": "關閉"}
]

class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle CDN requests (for SweetAlert2)
        if self.path.startswith("/cdnjs.cloudflare.com/"):
            url = "https://" + self.path[1:]
            logger.info(f"Proxying CDN request: {url}")
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    logger.error(f"CDN returned non-200 status: {response.status_code} for URL: {url}")
                
                self.send_response(response.status_code)
                for header, value in response.headers.items():
                    if header.lower() in ('content-type', 'content-length', 'cache-control'):
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.content)
                logger.info(f"Successfully proxied CDN resource: {url}")
                return
            except Exception as e:
                logger.error(f"Error fetching CDN resource: {e} for URL: {url}")
                self.send_error(500, f"Error fetching CDN resource: {str(e)}")
                return
        
        # Also handle cdn.jsdelivr.net as fallback for SweetAlert2
        elif self.path.startswith("/cdn.jsdelivr.net/"):
            url = "https://" + self.path[1:]
            logger.info(f"Proxying JSDelivr request: {url}")
            try:
                response = requests.get(url)
                self.send_response(response.status_code)
                for header, value in response.headers.items():
                    if header.lower() in ('content-type', 'content-length', 'cache-control'):
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.content)
                logger.info(f"Successfully proxied JSDelivr resource: {url}")
                return
            except Exception as e:
                logger.error(f"Error fetching JSDelivr resource: {e} for URL: {url}")
                self.send_error(500, f"Error fetching resource: {str(e)}")
                return
        
        # Serve API endpoints
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": relay_status})
            self.wfile.write(response.encode())
            return
        
        elif self.path == "/api/logs":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({"logs": logs})
            self.wfile.write(response.encode())
            return
        
        # Handle static files
        elif self.path.startswith("/static/"):
            file_path = self.path[1:]  # Remove leading slash
            if os.path.exists(file_path):
                self.send_response(200)
                if file_path.endswith('.css'):
                    self.send_header('Content-Type', 'text/css')
                elif file_path.endswith('.js'):
                    self.send_header('Content-Type', 'application/javascript')
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
                return
        
        # Special case for handling url_for in templates
        elif self.path.startswith("/url_for/"):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            if 'filename' in query:
                filename = query['filename'][0]
                file_path = f"static/{filename}"
                if os.path.exists(file_path):
                    self.send_response(200)
                    if file_path.endswith('.css'):
                        self.send_header('Content-Type', 'text/css')
                    elif file_path.endswith('.js'):
                        self.send_header('Content-Type', 'application/javascript')
                    self.end_headers()
                    with open(file_path, 'rb') as file:
                        self.wfile.write(file.read())
                    return
        
        # Serve index.html for root path
        elif self.path == "/" or self.path == "":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('templates/index.html', 'r', encoding='utf-8') as file:
                content = file.read()
                # Replace Flask's url_for with direct paths
                content = content.replace("{{ url_for('static', filename='style.css') }}", "/static/style.css")
                content = content.replace("{{ url_for('static', filename='script.js') }}", "/static/script.js")
                # Replace status variable
                content = content.replace("{{ status }}", relay_status)
                
                # Modify CDN paths to be proxied through our server
                content = re.sub(
                    r'href="https://cdnjs.cloudflare.com/(.+?)"', 
                    r'href="/cdnjs.cloudflare.com/\1"', 
                    content
                )
                content = re.sub(
                    r'src="https://cdnjs.cloudflare.com/(.+?)"', 
                    r'src="/cdnjs.cloudflare.com/\1"', 
                    content
                )
                
                # Also proxy jsdelivr CDN
                content = re.sub(
                    r'src="https://cdn.jsdelivr.net/(.+?)"', 
                    r'src="/cdn.jsdelivr.net/\1"', 
                    content
                )
                
                self.wfile.write(content.encode())
            return
            
        # Default handling for other paths
        return super().do_GET()
    
    def do_POST(self):
        # Handle relay control API
        if self.path == "/api/control":
            global relay_status
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            command = data.get('command')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if command == 'on':
                relay_status = "開啟"
                logs.insert(0, {"timestamp": timestamp, "status": "開啟"})
                response = {
                    "status": "success",
                    "message": "繼電器已開啟",
                    "timestamp": timestamp
                }
            elif command == 'off':
                relay_status = "關閉"
                logs.insert(0, {"timestamp": timestamp, "status": "關閉"})
                response = {
                    "status": "success",
                    "message": "繼電器已關閉",
                    "timestamp": timestamp
                }
            else:
                response = {
                    "status": "error",
                    "message": "無效的命令"
                }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Default handling for other POST requests
        return super().do_POST()

if __name__ == "__main__":
    PORT = 8000
    print(f"Preview server running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server.")
    
    # Install requests if not already installed
    try:
        import requests
    except ImportError:
        import subprocess
        print("Installing required package: requests")
        subprocess.check_call(["pip", "install", "requests"])
        print("Package 'requests' installed successfully")
        import requests
    
    # Test SweetAlert2 CDN access
    try:
        test_url = "https://cdnjs.cloudflare.com/ajax/libs/limonte-sweetalert2/11.7.5/sweetalert2.all.min.js"
        print(f"Testing CDN access to SweetAlert2...")
        response = requests.get(test_url)
        if response.status_code == 200:
            print("✓ SweetAlert2 CDN is accessible")
        else:
            print(f"✗ SweetAlert2 CDN returned status code: {response.status_code}")
            print("Trying alternative CDN...")
            alt_test_url = "https://cdn.jsdelivr.net/npm/sweetalert2@11"
            alt_response = requests.get(alt_test_url)
            if alt_response.status_code == 200:
                print("✓ Alternative SweetAlert2 CDN is accessible")
            else:
                print(f"✗ Alternative SweetAlert2 CDN returned status code: {alt_response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing SweetAlert2 CDN: {e}")
    
    with socketserver.TCPServer(("", PORT), PreviewHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
