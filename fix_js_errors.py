import os

files = ['generate_qa.py', 'generate_page2.py', 'generate_page3.py', 'generate_page4.py']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix the JS syntax errors caused by unescaped newlines in the generator scripts
    content = content.replace("theoryHTML.split('\n');", "theoryHTML.split('\\\\n');")
    content = content.replace("'<div class=\"table-responsive\"><table>\n';", "'<div class=\"table-responsive\"><table>\\\\n';")
    content = content.replace("'</tr>\n';", "'</tr>\\\\n';")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Fixed JS syntax errors in generator scripts.")
