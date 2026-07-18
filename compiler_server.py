import http.server
import socketserver
import json
import subprocess
import tempfile
import os
import re

PORT = 8080

class CompilerHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                code = data.get('code', '')
                
                # Dynamically extract the public class name from the code
                class_match = re.search(r'public\s+class\s+([A-Za-z0-9_]+)', code)
                class_name = class_match.group(1) if class_match else "Main"
                
                # Strip 'public' from all class/interface/enum declarations to prevent Java from complaining 
                # about filename mismatches or multiple public classes in a single file.
                code = re.sub(r'public\s+(class|interface|enum|record)\s+', r'\1 ', code)
                
                # Create a temporary directory to compile and run
                with tempfile.TemporaryDirectory() as temp_dir:
                    java_file = os.path.join(temp_dir, f"{class_name}.java")
                    with open(java_file, "w", encoding='utf-8') as f:
                        f.write(code)
                    
                    # Compile
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
                        # Run
                        run_process = subprocess.run(
                            ['java', class_name], 
                            cwd=temp_dir, 
                            capture_output=True, 
                            text=True,
                            timeout=5 # 5 seconds max execution
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
    with socketserver.TCPServer(("", PORT), CompilerHandler) as httpd:
        print(f"Java Compiler Server listening on port {PORT}")
        httpd.serve_forever()
