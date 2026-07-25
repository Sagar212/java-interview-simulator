import json
import re

with open('java_spring_interview_master.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
current_category = ""
current_block_type = "theory"
current_content = []

def flush_content():
    global current_content, current_block_type
    if current_content:
        text = "\n".join(current_content).strip()
        if text:
            if current_block_type == "code":
                output.append({"type": "code", "lang": "java", "content": text})
            else:
                output.append({"type": "theory", "content": text})
        current_content = []

i = 0
while i < len(lines):
    line = lines[i].rstrip()
    
    # Check for category header
    if line.startswith("======") and i + 1 < len(lines) and re.match(r'^\d+\)', lines[i+1].strip()):
        flush_content()
        i += 1
        category_name = lines[i].strip()
        output.append({"type": "category", "content": category_name})
        i += 1 # skip next ======
        current_block_type = "theory"
        i += 1
        continue
    
    # Check for sub-headings (Question or Java Template)
    if line.endswith("?") or line == "Constraint -> Pattern" or line == "Core Interview Answer" or line == "Memory Recall Table" or line == "Why It Works + Memory Pointer" or line == "Pain Points + Java Pitfalls" or line == "Follow-up Drills" or line == "Java Template":
        flush_content()
        if line == "Java Template":
            current_block_type = "code"
        else:
            output.append({"type": "question", "content": line})
            current_block_type = "theory"
        i += 1
        continue
        
    current_content.append(line)
    i += 1

flush_content()

with open('data/page2.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4)
print("Generated data/page2.json")
