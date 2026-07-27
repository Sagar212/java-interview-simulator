import os

generators = [
    'generate_qa.py',
    'generate_page2.py',
    'generate_page3.py',
    'generate_page4.py'
]

# Create generate_page5.py by copying generate_page4.py and updating the title and input/output
with open('generate_page4.py', 'r', encoding='utf-8') as f:
    page4_content = f.read()

page5_content = page4_content.replace("'data/page4.json'", "'data/page5.json'")
page5_content = page5_content.replace("'page4.html'", "'page5.html'")
page5_content = page5_content.replace("'Java Interview Simulator - Page 4'", "'Java Interview Simulator - Page 5 (DataCamp)'")

with open('generate_page5.py', 'w', encoding='utf-8') as f:
    f.write(page5_content)

generators.append('generate_page5.py')

# Now update the navigation in all generators to include Page 5
for gen in generators:
    with open(gen, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add page 5 to the navigation menu
    old_nav = '''
    <nav style="text-align: center; margin-bottom: 20px;">
        <a href="index.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 1 (Basic)</a> |
        <a href="page2.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 2 (Master)</a> |
        <a href="page3.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 3 (Spring Boot)</a> |
        <a href="page4.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 4 (Deep Dive)</a>
    </nav>
'''
    new_nav = '''
    <nav style="text-align: center; margin-bottom: 20px;">
        <a href="index.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 1 (Basic)</a> |
        <a href="page2.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 2 (Master)</a> |
        <a href="page3.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 3 (Spring Boot)</a> |
        <a href="page4.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 4 (Deep Dive)</a> |
        <a href="page5.html" style="margin: 0 10px; color: var(--accent-color); text-decoration: none; font-weight: bold;">Page 5 (DataCamp)</a>
    </nav>
'''
    content = content.replace(old_nav, new_nav)
    
    with open(gen, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated generators with Page 5 navigation.")
