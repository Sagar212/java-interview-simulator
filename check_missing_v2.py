import json
import glob
import re

# Load all questions from dump
with open('dump.txt', 'r', encoding='utf-8') as f:
    dump_lines = [line.strip() for line in f if line.strip()]

# Load all questions from JSON files
json_questions = []
for file_path in glob.glob('data/*.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            if item['type'] == 'question':
                json_questions.append(item['content'])

# Normalize for comparison
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

normalized_json = {normalize(q): q for q in json_questions}

def compute_similarity(s1, s2):
    w1 = set(re.findall(r'\w+', s1.lower()))
    w2 = set(re.findall(r'\w+', s2.lower()))
    if not w1 or not w2:
        return 0
    return len(w1.intersection(w2)) / max(len(w1), len(w2))

missing = []

for line in dump_lines:
    norm_line = normalize(line)
    
    # 1. Exact or substring match in normalized strings
    found = False
    for j_norm, original_q in normalized_json.items():
        if norm_line in j_norm or j_norm in norm_line:
            found = True
            break
            
    # 2. Keyword/Word overlap match
    if not found:
        best_match = None
        best_score = 0
        for j_norm, original_q in normalized_json.items():
            score = compute_similarity(line, original_q)
            if score > best_score:
                best_score = score
                best_match = original_q
                
        # If the best overlap is decent (e.g. 50%), consider it mapped
        if best_score > 0.45:
            found = True
            # print(f"Mapped via overlap ({best_score:.2f}):\n  DUMP: {line}\n  JSON: {best_match}\n")
            
    if not found:
        missing.append(line)

print("--- DEFINITELY MISSING ---")
for m in missing:
    print(m)
