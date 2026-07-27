import os
import re

with open('generate_qa.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS to include .table-responsive
css_addition = """
        .table-responsive {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        table {
"""
if ".table-responsive {" not in content:
    content = content.replace("        table {", css_addition)

# 2. Update JavaScript parsing logic
new_js_logic = """
                    let lines = theoryHTML.split('\\n');
                    let inTable = false;
                    let tableHTML = '';
                    let finalLines = [];

                    for (let i = 0; i < lines.length; i++) {
                        let line = lines[i].trim();
                        if (line.startsWith('|') && line.endsWith('|')) {
                            if (!inTable) {
                                inTable = true;
                                tableHTML = '<div class="table-responsive"><table>\\n';
                            }
                            
                            if (line.includes('---')) continue;
                            
                            let cells = line.split('|').slice(1, -1).map(c => c.trim());
                            let rowHTML = '<tr>';
                            cells.forEach(cell => {
                                if (tableHTML.indexOf('<tr>') === -1) {
                                    rowHTML += `<th>${cell}</th>`;
                                } else {
                                    rowHTML += `<td>${cell}</td>`;
                                }
                            });
                            rowHTML += '</tr>\\n';
                            tableHTML += rowHTML;
                        } else {
                            if (inTable) {
                                inTable = false;
                                tableHTML += '</table></div>';
                                finalLines.push(tableHTML);
                            }
                            finalLines.push(lines[i]);
                        }
                    }
                    if (inTable) {
                        tableHTML += '</table></div>';
                        finalLines.push(tableHTML);
                    }

                    let formattedHTML = finalLines.join('<br>');
                    formattedHTML = formattedHTML.replace(/<br>- /g, '<br>• ');
                    formattedHTML = formattedHTML.replace(/<br><div class="table-responsive">/g, '<div class="table-responsive">');
                    formattedHTML = formattedHTML.replace(/<\\/div><br>/g, '</div>');
"""

# Replace the existing formatting logic
# The old logic is between "theoryHTML.replace(hookRegex, '<strong>$1</strong>');" and "tEl.innerHTML = formattedHTML;"
old_logic_pattern = re.compile(r'const tEl = document\.createElement\(\'div\'\);.*?let formattedHTML = .*?;', re.DOTALL)

replacement = "const tEl = document.createElement('div');\n                    tEl.className = 'theory';\n" + new_js_logic

content = re.sub(old_logic_pattern, replacement, content)

# 3. Add Page 4 to Nav bar
nav_html = """<div class="top-nav">
        <a href="index.html"{p1}>Page 1: Core Java Simulator</a>
        <a href="page2.html"{p2}>Page 2: Spring & Master Q&A</a>
        <a href="page3.html"{p3}>Page 3: Spring Boot Deep Dive</a>
        <a href="page4.html"{p4}>Page 4: Scenario Deep Dives</a>
    </div>"""

def replace_nav(base_content, active_page):
    p1 = ' class="active"' if active_page == 1 else ''
    p2 = ' class="active"' if active_page == 2 else ''
    p3 = ' class="active"' if active_page == 3 else ''
    p4 = ' class="active"' if active_page == 4 else ''
    
    current_nav = nav_html.format(p1=p1, p2=p2, p3=p3, p4=p4)
    return re.sub(r'<div class="top-nav">.*?</div>', current_nav, base_content, flags=re.DOTALL)

# Write updated generate_qa.py
with open('generate_qa.py', 'w', encoding='utf-8') as f:
    f.write(replace_nav(content, 1))

# Write generate_page2.py
content2 = content.replace("'data/master.json'", "'data/page2.json'")
content2 = content2.replace("<h1>Java Scenario Simulator</h1>", "<h1>Java & Spring Master Q&A</h1>")
content2 = content2.replace("Interactive Q&A for Core Java", "Advanced Java & Spring Topics")
with open('generate_page2.py', 'w', encoding='utf-8') as f:
    f.write(replace_nav(content2, 2))

# Write generate_page3.py
content3 = content.replace("'data/master.json'", "'data/page3.json'")
content3 = content3.replace("<h1>Java Scenario Simulator</h1>", "<h1>Spring Boot Deep Dive</h1>")
content3 = content3.replace("Interactive Q&A for Core Java", "Advanced Spring Boot Internals")
with open('generate_page3.py', 'w', encoding='utf-8') as f:
    f.write(replace_nav(content3, 3))

# Write generate_page4.py
content4 = content.replace("'data/master.json'", "'data/page4.json'")
content4 = content4.replace("<h1>Java Scenario Simulator</h1>", "<h1>Scenario Deep Dives</h1>")
content4 = content4.replace("Interactive Q&A for Core Java", "Real-World Architecture & Debugging Scenarios")
with open('generate_page4.py', 'w', encoding='utf-8') as f:
    f.write(replace_nav(content4, 4))

print("All generator scripts updated with table support and new navigation.")
