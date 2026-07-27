import sys
from bs4 import BeautifulSoup

filename = 'Top Java Interview Questions & Answers For All Levels 2026 _ DataCamp.html'
with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

print("H2 tags:")
for h2 in soup.find_all('h2')[:10]:
    print("-", h2.get_text().strip())

print("\nH3 tags:")
for h3 in soup.find_all('h3')[:10]:
    print("-", h3.get_text().strip())
    
print("\nSample content:")
for h3 in soup.find_all('h3')[:2]:
    print("Q:", h3.get_text().strip())
    for elem in h3.find_next_siblings():
        if elem.name in ['h2', 'h3']:
            break
        print("A:", elem.get_text().strip())
