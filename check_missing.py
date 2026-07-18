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

normalized_json = [normalize(q) for q in json_questions]

missing = []
for line in dump_lines:
    norm_line = normalize(line)
    # Check if the line is a substring of any JSON question or vice-versa
    found = False
    for j_norm in normalized_json:
        if norm_line in j_norm or j_norm in norm_line:
            found = True
            break
        # Do a partial overlap check (if they share 70% of words)
        words_line = set(re.findall(r'\w+', line.lower()))
        words_json = set(re.findall(r'\w+', [q for q in json_questions if normalize(q) == j_norm][0].lower()))
        if len(words_line) > 3 and len(words_json) > 3:
            overlap = len(words_line.intersection(words_json))
            if overlap / len(words_line) > 0.7:
                found = True
                break
    
    if not found:
        missing.append(line)

print("MISSING QUESTIONS:")
for m in missing:
    print(m)
