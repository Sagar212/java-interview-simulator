import json
import re
import sys
import os

if len(sys.argv) != 3:
    print("Usage: python parse_master_txt.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.exists(input_file):
    print(f"Error: Input file {input_file} not found.")
    sys.exit(1)

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
current_content = []
is_code_block = False

def flush_content():
    global current_content, is_code_block
    if current_content:
        text = "\n".join(current_content).strip()
        if text:
            if is_code_block:
                output.append({"type": "code", "lang": "java", "content": text})
            else:
                output.append({"type": "theory", "content": text})
        current_content = []
    is_code_block = False

i = 0
while i < len(lines):
    line = lines[i].rstrip()
    
    # Check for category header
    if line.startswith("======") and i + 1 < len(lines) and (re.match(r'^\d+\)', lines[i+1].strip()) or re.match(r'^[A-Z]', lines[i+1].strip())):
        flush_content()
        i += 1
        category_name = lines[i].strip()
        output.append({"type": "category", "content": category_name})
        i += 1 # skip next ======
        i += 1
        continue
    
    # Check for Question
    if line.startswith("Q:") and (len(line) == 2 or line[2].isspace()):
        flush_content()
        q_content = line[2:].strip()
        if q_content:
            output.append({"type": "question", "content": q_content})
        i += 1
        continue
        
    # Check for Answer
    if line.startswith("A:") and (len(line) == 2 or line[2].isspace()):
        flush_content() # Just in case
        a_content = line[2:].strip()
        if a_content:
            current_content.append(a_content)
        i += 1
        continue
        
    # Check for Code Template
    if line.strip() == "Java Template":
        flush_content()
        is_code_block = True
        i += 1
        continue
        
    if line.strip() == "End Template":
        flush_content()
        i += 1
        continue
        
    if line.strip() != "" or current_content:
        if not (not current_content and line.strip() == ""):
             current_content.append(line)
        
    i += 1

flush_content()

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4)
print(f"Generated {output_file} from {input_file}")
