import json
import re

with open('JAVA & SPRING INTERVIEW MASTER QUES.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
current_content = []

def flush_theory():
    global current_content
    if current_content:
        text = "\n".join(current_content).strip()
        if text:
            output.append({"type": "theory", "content": text})
        current_content = []

i = 0
while i < len(lines):
    line = lines[i].rstrip()
    
    # Check for category header
    if line.startswith("======") and i + 1 < len(lines) and re.match(r'^\d+\)', lines[i+1].strip()):
        flush_theory()
        i += 1
        category_name = lines[i].strip()
        output.append({"type": "category", "content": category_name})
        i += 1 # skip next ======
        i += 1
        continue
    
    # Check for Question
    if line.startswith("Q: "):
        flush_theory()
        output.append({"type": "question", "content": line[3:].strip()})
        i += 1
        continue
        
    # Check for Answer
    if line.startswith("A: "):
        current_content.append(line[3:].strip())
        i += 1
        continue
        
    if line.strip() != "" or current_content:
        # Avoid leading empty lines in theory, but keep empty lines between paragraphs
        if not (not current_content and line.strip() == ""):
             current_content.append(line)
        
    i += 1

flush_theory()

with open('data/page2.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4)
print("Generated data/page2.json from JAVA & SPRING INTERVIEW MASTER QUES.txt")
