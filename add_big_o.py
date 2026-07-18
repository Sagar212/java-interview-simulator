import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

big_o_questions = [
    {
        "type": "question",
        "content": "Explain Big O Time Complexity with a cheat sheet table and code examples."
    },
    {
        "type": "theory",
        "content": "Big O notation mathematically describes the worst-case execution time of an algorithm as the input size (`n`) grows to infinity.\n\n<table>\n<tr><th>Big O</th><th>Name</th><th>Performance</th><th>Example Data Structure Operation</th></tr>\n<tr><td><strong>O(1)</strong></td><td>Constant Time</td><td>Excellent (Instant)</td><td><code>HashMap.get()</code>, <code>Array[index]</code></td></tr>\n<tr><td><strong>O(log n)</strong></td><td>Logarithmic Time</td><td>Great (Divides data in half)</td><td>Binary Search, <code>TreeSet.contains()</code></td></tr>\n<tr><td><strong>O(n)</strong></td><td>Linear Time</td><td>Fair (Reads every element)</td><td><code>LinkedList.search()</code>, standard <code>for</code> loop</td></tr>\n<tr><td><strong>O(n log n)</strong></td><td>Linearithmic Time</td><td>Bad (for large sets)</td><td>Merge Sort, Quick Sort, <code>Collections.sort()</code></td></tr>\n<tr><td><strong>O(n²)</strong></td><td>Quadratic Time</td><td>Horrible (Nested loops)</td><td>Bubble Sort, Comparing every item against every other item</td></tr>\n</table>"
    },
    {
        "type": "code",
        "lang": "java",
        "content": "// 1. O(1) Constant Time (Instant lookup, no loops)\nint x = arr[0]; \nmap.get(\"key\");\n\n// 2. O(log n) Logarithmic Time (Binary Search - halving the array each step)\nwhile (low <= high) {\n    int mid = low + (high - low) / 2;\n    if (arr[mid] == target) return mid;\n    if (arr[mid] < target) low = mid + 1;\n    else high = mid - 1;\n}\n\n// 3. O(n) Linear Time (Iterating through everything exactly once)\nfor (int num : arr) {\n    if (num == target) return true;\n}\n\n// 4. O(n^2) Quadratic Time (Nested loops - Massive performance killer)\nfor (int i = 0; i < arr.length; i++) {\n    for (int j = 0; j < arr.length; j++) {\n        if (arr[i] == arr[j]) { /* do something */ }\n    }\n}"
    }
]

# Insert under Coding & Algorithms
algo_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Algorithms' in item.get('content', ''):
        algo_index = i
        break

if algo_index != -1:
    master_data[algo_index+1:algo_index+1] = big_o_questions
else:
    master_data.append({"type": "category", "content": "Algorithms & Complexity"})
    master_data.extend(big_o_questions)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
