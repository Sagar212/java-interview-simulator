import os

files = ['generate_qa.py', 'generate_page2.py', 'generate_page3.py']

for f_name in files:
    with open(f_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the newline logic to format ALL newlines as <br>, 
    # making bullet points and numbered lists actually break to a new line!
    # Also add bullet point styling for lines starting with '- '
    
    # We will replace this block:
    # let formattedHTML = theoryHTML.replace(/\\n\\n/g, '<br><br>');
    # with a better parser.
    
    better_parser = """
                    let formattedHTML = theoryHTML.replace(/\\n/g, '<br>');
                    // Highlight bullet points specifically
                    formattedHTML = formattedHTML.replace(/<br>- /g, '<br>• ');
                    """
    
    content = content.replace("let formattedHTML = theoryHTML.replace(/\\n\\n/g, '<br><br>');", better_parser)
    
    with open(f_name, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated formatting logic in all generators.")
