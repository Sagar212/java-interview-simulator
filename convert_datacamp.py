import sys
import re
from bs4 import BeautifulSoup

def clean_text(text):
    return text.replace('\xa0', ' ').strip()

html_file = 'Top Java Interview Questions & Answers For All Levels 2026 _ DataCamp.html'
txt_file = 'datacamp_questions.txt'

with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

with open(txt_file, 'w', encoding='utf-8') as out:
    cat_idx = 1
    
    # We will iterate over all elements.
    # When we hit an H2, it's a category.
    # When we hit an H3, it's a question.
    # Everything after an H3 until the next H2 or H3 is part of the answer.
    
    body = soup.find('body')
    if body:
        # Get all text blocks preserving some structure
        # Better: iterate through descendants
        
        main_content = soup.find_all(['h2', 'h3'])
        
        for heading in main_content:
            if heading.name == 'h2':
                text = clean_text(heading.get_text())
                if text.lower() in ['explore with ai', 'tl;dr', 'conclusion', 'learn java essentials']:
                    continue
                out.write(f"======\n{cat_idx}) {text}\n======\n\n")
                cat_idx += 1
            elif heading.name == 'h3':
                q_text = clean_text(heading.get_text())
                # Remove leading numbers like "1. " if present to keep it clean, but keep it for now
                out.write(f"Q: {q_text}\n")
                
                # Gather answer
                curr = heading.next_sibling
                while curr and curr.name not in ['h2', 'h3']:
                    if curr.name:
                        if curr.name == 'pre' or (curr.name == 'div' and 'code' in curr.get('class', [])):
                            code_text = clean_text(curr.get_text())
                            if code_text:
                                out.write("Java Template\n")
                                out.write(code_text + "\n")
                                out.write("End Template\n")
                        else:
                            p_text = clean_text(curr.get_text())
                            if p_text and not p_text.startswith("Powered By"):
                                out.write(f"A: {p_text}\n")
                    curr = curr.next_sibling
                out.write("\n")

print(f"Created {txt_file}")
