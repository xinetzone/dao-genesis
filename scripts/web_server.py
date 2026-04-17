import http.server
import socketserver
import json
import os
from pathlib import Path
import urllib.parse
import sys

# Import project tools
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import REVIEWS_DIR, CACHE_REVIEWS_DIR
from build_memory_cache import build_index
from manage_memory import load_record, save_record

PORT = 8000
WEB_DIR = Path(__file__).resolve().parents[1] / "web"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static files from WEB_DIR
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API: /api/index
        if parsed_path.path == '/api/index':
            index_file = CACHE_REVIEWS_DIR / "search_index.json"
            if not index_file.exists():
                build_index()
            
            if index_file.exists():
                self._set_headers()
                self.wfile.write(index_file.read_bytes())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Index not found"}).encode())
            return
            
        # API: /api/reviews/{id}
        elif parsed_path.path.startswith('/api/reviews/'):
            review_id = parsed_path.path.split('/')[-1]
            file_path = REVIEWS_DIR / f"{review_id}.json"
            
            if file_path.exists():
                self._set_headers()
                self.wfile.write(file_path.read_bytes())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Record not found"}).encode())
            return
            
        # Fallback to static files
        return super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Parse body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8')) if post_data else {}
        except Exception:
            body = {}

        # API: /api/reviews/{id}/archive
        if parsed_path.path.startswith('/api/reviews/') and parsed_path.path.endswith('/archive'):
            review_id = parsed_path.path.split('/')[-2]
            try:
                data = load_record(review_id, REVIEWS_DIR)
                data["status"] = "archived"
                save_record(review_id, data, REVIEWS_DIR)
                build_index() # Rebuild cache
                
                self._set_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        # API: /api/reviews/{id}/update
        elif parsed_path.path.startswith('/api/reviews/') and parsed_path.path.endswith('/update'):
            review_id = parsed_path.path.split('/')[-2]
            field = body.get("field")
            value = body.get("value")
            append = body.get("append", False)
            
            if not field or not value:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Missing field or value"}).encode())
                return
                
            try:
                data = load_record(review_id, REVIEWS_DIR)
                array_fields = {"participants", "decisions", "success_factors", "failure_reasons", "best_practices", "action_items"}
                
                if field in array_fields:
                    if field not in data or not isinstance(data[field], list):
                        data[field] = []
                    if append:
                        data[field].append(value)
                    else:
                        data[field] = [value]
                else:
                    if append:
                        raise ValueError(f"Cannot append to string field '{field}'")
                    data[field] = value
                    
                save_record(review_id, data, REVIEWS_DIR)
                build_index() # Rebuild cache
                
                self._set_headers()
                self.wfile.write(json.dumps({"success": True}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

def main():
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
