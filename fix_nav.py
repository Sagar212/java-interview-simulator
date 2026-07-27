import os
import re

generators = [
    'generate_qa.py',
    'generate_page2.py',
    'generate_page3.py',
    'generate_page4.py',
    'generate_page5.py'
]

for gen in generators:
    with open(gen, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's use regex to replace the top-nav div
    old_nav_pattern = r'<div class="top-nav">.*?</div>'
    
    new_nav = '''<div class="top-nav">
        <a href="index.html" class="{p1}">Page 1: Core Java Simulator</a>
        <a href="page2.html" class="{p2}">Page 2: Spring & Master Q&A</a>
        <a href="page3.html" class="{p3}">Page 3: Spring Boot Deep Dive</a>
        <a href="page4.html" class="{p4}">Page 4: Scenario Deep Dives</a>
        <a href="page5.html" class="{p5}">Page 5: DataCamp Q&A</a>
    </div>'''
    
    # We need to preserve the "active" class depending on the file
    p1 = 'active' if gen == 'generate_qa.py' else ''
    p2 = 'active' if gen == 'generate_page2.py' else ''
    p3 = 'active' if gen == 'generate_page3.py' else ''
    p4 = 'active' if gen == 'generate_page4.py' else ''
    p5 = 'active' if gen == 'generate_page5.py' else ''
    
    nav_to_insert = new_nav.format(p1=p1, p2=p2, p3=p3, p4=p4, p5=p5)
    
    # Clean up empty classes (class="")
    nav_to_insert = nav_to_insert.replace(' class=""', '')
    
    content = re.sub(old_nav_pattern, nav_to_insert, content, flags=re.DOTALL)
    
    with open(gen, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed top-nav in all generators.")
