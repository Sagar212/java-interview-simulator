import json
import re

with open('append.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# We will use regex to find all objects
# Pattern: \{ type: "([^"]+)",(?: lang: "([^"]+)",)? content: (?:`([^`]+)`|"([^"]+)") \}
# Group 1: type
# Group 2: lang (optional)
# Group 3: content inside backticks
# Group 4: content inside quotes

pattern = r'\{\s*type:\s*"([^"]+)",(?:\s*lang:\s*"([^"]+)",)?\s*content:\s*(?:`([^`]+)`|"([^"\\]*(?:\\.[^"\\]*)*)")\s*\}'

matches = re.finditer(pattern, content)

new_items = []
for match in matches:
    obj_type = match.group(1)
    obj_lang = match.group(2)
    
    # Content is either in backticks (group 3) or double quotes (group 4)
    obj_content = match.group(3)
    if obj_content is None:
        obj_content = match.group(4)
        # unescape quotes and newlines if it was in double quotes
        obj_content = obj_content.encode('utf-8').decode('unicode_escape')

    item = {
        "type": obj_type,
        "content": obj_content
    }
    if obj_lang:
        item["lang"] = obj_lang
        
    new_items.append(item)

print(f"Extracted {len(new_items)} items from append.txt")

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

master_data.extend(new_items)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
