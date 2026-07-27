import json
import os

# Load the meticulously ordered master JSON
with open('data/page3.json', 'r', encoding='utf-8') as f:
    qa_list = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Java Interview Q&A & Scenario Simulator</title>
    
    <!-- Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Inter:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
    
    <!-- Syntax Highlighting (PrismJS) -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    
    <style>
        :root {
            --bg-primary: #121316;
            --bg-card: #1a1c23;
            --text-main: #e3e4e8;
            --text-theory: #cbd5e1;
            --accent: #00e676;
            --bg-code: #0f1115;
            
            --font-question: 'Inter', sans-serif;
            --font-theory: 'Merriweather', serif;
            --font-code: 'Fira Code', monospace;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            margin: 0;
            padding: 90px 20px 60px 20px; /* Increased top padding for fixed nav */
            font-family: var(--font-question);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            display: flex;
            justify-content: center;
        }

        /* Top Navigation Bar */
        .top-nav {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: var(--bg-card);
            padding: 15px 0;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .top-nav a {
            color: var(--text-theory);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            margin: 0 15px;
            padding: 8px 16px;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .top-nav a:hover {
            background-color: rgba(255,255,255,0.05);
            color: #ffffff;
        }

        .top-nav a.active {
            background-color: rgba(0, 230, 118, 0.1);
            color: var(--accent);
            border: 1px solid rgba(0, 230, 118, 0.2);
        }

        #app {
            width: 100%;
            max-width: 1000px;
        }

        header {
            margin-bottom: 50px;
            text-align: center;
        }

        h1 {
            font-family: var(--font-question);
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
        }

        .subtitle {
            font-family: var(--font-theory);
            font-size: 18px;
            color: var(--text-theory);
            line-height: 1.68;
        }

        .category-header {
            font-family: var(--font-question);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--accent);
            margin-top: 60px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 10px;
        }

        .qa-container {
            background-color: var(--bg-card);
            border-radius: 12px;
            padding: 40px 35px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .qa-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }

        .question {
            font-family: var(--font-question);
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
            margin: 0 0 25px 0;
            padding-left: 20px;
            border-left: 4px solid var(--accent);
            line-height: 1.4;
        }

        .theory {
            font-family: var(--font-theory);
            font-size: 18.5px;
            color: var(--text-theory);
            line-height: 1.7;
            margin: 0 0 20px 0;
        }
        
        .theory strong {
            color: #ffffff;
            font-weight: 700;
        }


        .table-responsive {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        table {

            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-family: var(--font-question);
            font-size: 16.5px;
            background-color: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        th, td {
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            line-height: 1.5;
        }
        
        th {
            background-color: rgba(0, 230, 118, 0.08);
            color: var(--accent);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 1px;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        tr:hover td {
            background-color: rgba(255, 255, 255, 0.03);
        }

        .recall-anchor {
            background-color: rgba(0, 230, 118, 0.06);
            border-left: 3px solid var(--accent);
            border-radius: 0 6px 6px 0;
            padding: 16px 20px;
            margin: 25px 0;
            font-family: var(--font-question);
            font-size: 15.5px;
            font-weight: 700;
            color: var(--accent);
            line-height: 1.5;
            position: relative;
        }

        .recall-anchor::before {
            content: '⚡ KEY RECALL';
            display: block;
            font-size: 11px;
            letter-spacing: 1.2px;
            opacity: 0.8;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        .code-container {
            background-color: var(--bg-code);
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0 0 0;
            overflow-x: auto;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        pre[class*="language-"] {
            margin: 0 !important;
            padding: 0 !important;
            background: transparent !important;
        }

        code[class*="language-"], pre[class*="language-"] {
            font-family: var(--font-code) !important;
            font-size: 15.5px !important;
            line-height: 1.5 !important;
            text-shadow: none !important;
        }
        
        p.theory code, td code, div.theory code {
            background: rgba(255,255,255,0.08);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: var(--font-code);
            font-size: 0.85em;
            color: #fff;
        }

        .run-btn {
            background-color: var(--accent);
            color: #121316;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-family: var(--font-question);
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .run-btn:hover {
            opacity: 0.9;
        }
        .run-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .console-output {
            background-color: #0d0d0d;
            border-left: 3px solid #666;
            padding: 12px;
            margin-top: 10px;
            font-family: var(--font-code);
            font-size: 14.5px;
            color: #00ff00;
            display: none;
            white-space: pre-wrap;
            overflow-x: auto;
            border-radius: 0 4px 4px 0;
        }
        .console-output.error {
            border-left-color: #ff4444;
            color: #ffaa00;
        }
    </style>
</head>
<body>
    <div class="top-nav">
        <a href="index.html">Page 1: Core Java Simulator</a>
        <a href="page2.html">Page 2: Spring & Master Q&A</a>
        <a href="page3.html" class="active">Page 3: Spring Boot Deep Dive</a>
        <a href="page4.html">Page 4: Scenario Deep Dives</a>
        <a href="page5.html">Page 5: DataCamp Q&A</a>
    </div>

    <div id="app">
        <header>
            <h1>Spring Boot Deep Dive</h1>
            <div class="subtitle">High-Retention Interview Preparation (In-Depth Edition)</div>
        </header>
        <main id="content-track"></main>
    </div>

    <!-- Syntax Highlighting Script -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-java.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>

    <script>
        const interviewData = JSON_PAYLOAD_HERE;

        document.addEventListener('DOMContentLoaded', () => {
            const track = document.getElementById('content-track');
            let currentContainer = null;

            interviewData.forEach(item => {
                if (item.type === 'category') {
                    const catEl = document.createElement('div');
                    catEl.className = 'category-header';
                    catEl.textContent = item.content;
                    track.appendChild(catEl);
                    currentContainer = null;
                    return;
                }

                if (item.type === 'question') {
                    currentContainer = document.createElement('div');
                    currentContainer.className = 'qa-container';
                    track.appendChild(currentContainer);

                    const qEl = document.createElement('h2');
                    qEl.className = 'question';
                    qEl.textContent = item.content;
                    currentContainer.appendChild(qEl);
                    return;
                }

                if (!currentContainer) {
                    currentContainer = document.createElement('div');
                    currentContainer.className = 'qa-container';
                    track.appendChild(currentContainer);
                }

                if (item.type === 'theory') {
                    const hookRegex = /\*\*(.*?)\*\*/g;
                    let theoryHTML = item.content;
                    let match;
                    const hooks = [];

                    while ((match = hookRegex.exec(item.content)) !== null) {
                        hooks.push(match[1]);
                    }

                    theoryHTML = theoryHTML.replace(/(?<!<[^>]*?)`([^`]+)`(?![^<]*?>)/g, '<code>$1</code>');
                    theoryHTML = theoryHTML.replace(hookRegex, '<strong>$1</strong>');

                    const tEl = document.createElement('div');
                    tEl.className = 'theory';

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
                    formattedHTML = formattedHTML.replace(/<\/div><br>/g, '</div>');

                    tEl.innerHTML = formattedHTML;
                    currentContainer.appendChild(tEl);

                    hooks.forEach(hookText => {
                        const anchorEl = document.createElement('aside');
                        anchorEl.className = 'recall-anchor';
                        anchorEl.textContent = hookText;
                        currentContainer.appendChild(anchorEl);
                    });
                }

                if (item.type === 'code') {
                    const codeBlock = document.createElement('div');
                    codeBlock.className = 'code-container';
                    
                    const pre = document.createElement('pre');
                    const code = document.createElement('code');
                    const lang = item.lang ? item.lang : 'java';
                    code.className = `language-${lang}`;
                    code.textContent = item.content;
                    
                    pre.appendChild(code);
                    codeBlock.appendChild(pre);
                    currentContainer.appendChild(codeBlock);

                    if (lang === 'java') {
                        const runBtn = document.createElement('button');
                        runBtn.className = 'run-btn';
                        runBtn.innerHTML = '▶ Run Code';
                        
                        const consoleOut = document.createElement('div');
                        consoleOut.className = 'console-output';
                        
                        runBtn.onclick = () => executeJava(item.content, runBtn, consoleOut);
                        
                        currentContainer.appendChild(runBtn);
                        currentContainer.appendChild(consoleOut);
                    }
                }
            });

            if (window.Prism) {
                Prism.highlightAll();
            }
        });

        async function executeJava(sourceCode, btn, consoleOut) {
            btn.disabled = true;
            btn.innerHTML = '⏳ Running...';
            consoleOut.style.display = 'block';
            consoleOut.className = 'console-output';
            consoleOut.textContent = 'Compiling and executing on cloud...';

            let codeToRun = sourceCode;
            if (!codeToRun.includes('public class') && !codeToRun.includes('static void main')) {
                codeToRun = `import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;
public class Main {
    public static void main(String[] args) throws Exception {
        ${sourceCode}
    }
}`;
            } else if (!codeToRun.includes('public class') && codeToRun.includes('class ')) {
                codeToRun = codeToRun.replace('class ', 'public class ');
            }

            try {
                const response = await fetch('http://localhost:8080/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code: codeToRun })
                });

                const result = await response.json();
                
                if (result.status === 'success') {
                    consoleOut.textContent = result.output || "Program finished with no output.";
                } else {
                    consoleOut.className = 'console-output error';
                    if (result.type === 'compile') {
                        consoleOut.textContent = "COMPILATION ERROR:\\n" + result.output;
                    } else if (result.type === 'run') {
                        consoleOut.textContent = "RUNTIME ERROR:\\n" + result.output;
                    } else {
                        consoleOut.textContent = "SERVER ERROR:\\n" + result.output;
                    }
                }
            } catch (err) {
                consoleOut.className = 'console-output error';
                consoleOut.textContent = "Network error: Make sure you are running 'python compiler_server.py' in the background!\\nDetails: " + err.message;
            } finally {
                btn.disabled = false;
                btn.innerHTML = '▶ Run Code';
            }
        }
    </script>
</body>
</html>
"""

# Replace payload
final_html = html_template.replace("JSON_PAYLOAD_HERE", json.dumps(qa_list, indent=4))

# Write final HTML
with open('page3.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
