import os

def update_nav(filepath, active_page):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the new nav HTML
    nav_html_1 = '<a href="index.html"' + (' class="active"' if active_page == 1 else '') + '>Page 1: Core Java Simulator</a>\n'
    nav_html_2 = '        <a href="page2.html"' + (' class="active"' if active_page == 2 else '') + '>Page 2: Spring & Master Q&A</a>\n'
    nav_html_3 = '        <a href="page3.html"' + (' class="active"' if active_page == 3 else '') + '>Page 3: Spring Boot Deep Dive</a>'
    
    new_nav = f'<div class="top-nav">\n        {nav_html_1}{nav_html_2}{nav_html_3}\n    </div>'
    
    import re
    # Replace the existing top-nav div
    new_content = re.sub(r'<div class="top-nav">.*?</div>', new_nav, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

update_nav('generate_qa.py', 1)
update_nav('generate_page2.py', 2)

# Create generate_page3.py based on generate_page2.py
with open('generate_page2.py', 'r', encoding='utf-8') as f:
    page3_content = f.read()

# Modify it to load page3.json, generate page3.html, and set active link correctly
page3_content = page3_content.replace("'data/page2.json'", "'data/page3.json'")
page3_content = page3_content.replace("'page2.html'", "'page3.html'")
# Update the nav block in page3
nav_html_1 = '<a href="index.html">Page 1: Core Java Simulator</a>\n'
nav_html_2 = '        <a href="page2.html">Page 2: Spring & Master Q&A</a>\n'
nav_html_3 = '        <a href="page3.html" class="active">Page 3: Spring Boot Deep Dive</a>'
new_nav = f'<div class="top-nav">\n        {nav_html_1}{nav_html_2}{nav_html_3}\n    </div>'
import re
page3_content = re.sub(r'<div class="top-nav">.*?</div>', new_nav, page3_content, flags=re.DOTALL)
page3_content = page3_content.replace("<h1>Java & Spring Master Q&A</h1>", "<h1>Spring Boot Deep Dive</h1>")
page3_content = page3_content.replace("Advanced Java & Spring Topics", "Advanced Spring Boot Internals")

with open('generate_page3.py', 'w', encoding='utf-8') as f:
    f.write(page3_content)

print("Navigation and generation scripts updated.")
