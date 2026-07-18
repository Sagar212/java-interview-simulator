import json
from generate_qa import qa_list

with open('data/part1.json', 'w', encoding='utf-8') as f:
    json.dump(qa_list, f, indent=4)
