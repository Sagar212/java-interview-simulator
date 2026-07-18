import http.server
import socketserver
import json
import subprocess
import tempfile
import os
import glob
import re

PORT = 8081
DIRECTORY = "java_problems"

class InterviewHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/java-scanner.html'
            return super().do_GET()
        
        elif self.path == '/api/files':
            if not os.path.exists(DIRECTORY):
                os.makedirs(DIRECTORY)
                
            java_files = glob.glob(os.path.join(DIRECTORY, "*.java"))
            files_data = []
            
            for file_path in java_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    filename = os.path.basename(file_path)
                    files_data.append({
                        "filename": filename,
                        "code": content
                    })
                    
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(files_data).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                code = data.get('code', '')
                
                class_match = re.search(r'public\s+class\s+([A-Za-z0-9_]+)', code)
                class_name = class_match.group(1) if class_match else "Main"
                
                # Strip public from classes/interfaces to bypass Java's single-file public constraints
                code = re.sub(r'public\s+(class|interface|enum|record)\s+', r'\1 ', code)
                
                with tempfile.TemporaryDirectory() as temp_dir:
                    java_file = os.path.join(temp_dir, f"{class_name}.java")
                    with open(java_file, "w", encoding='utf-8') as f:
                        f.write(code)
                    
                    compile_process = subprocess.run(
                        ['javac', f"{class_name}.java"], 
                        cwd=temp_dir, 
                        capture_output=True, 
                        text=True
                    )
                    
                    if compile_process.returncode != 0:
                        response_data = {
                            "status": "error",
                            "type": "compile",
                            "output": compile_process.stderr
                        }
                    else:
                        run_process = subprocess.run(
                            ['java', class_name], 
                            cwd=temp_dir, 
                            capture_output=True, 
                            text=True,
                            timeout=5 
                        )
                        if run_process.returncode != 0:
                            response_data = {
                                "status": "error",
                                "type": "run",
                                "output": run_process.stderr
                            }
                        else:
                            response_data = {
                                "status": "success",
                                "output": run_process.stdout
                            }
            except subprocess.TimeoutExpired:
                response_data = {
                    "status": "error",
                    "type": "timeout",
                    "output": "Execution timed out after 5 seconds."
                }
            except Exception as e:
                response_data = {
                    "status": "error",
                    "type": "server",
                    "output": str(e)
                }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), InterviewHandler) as httpd:
        print(f"Directory Scanner Server listening on http://localhost:{PORT}")
        httpd.serve_forever()
