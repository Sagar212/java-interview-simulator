import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

# 1. Update HashMap Internals
for i in range(len(master_data)):
    if master_data[i].get('type') == 'question' and 'hashmap' in master_data[i].get('content', '').lower() and 'internal' in master_data[i].get('content', '').lower():
        if master_data[i+1].get('type') == 'theory':
            master_data[i+1]['content'] = """<p><strong>Step 1: Hashing & Indexing</strong></p>
<p>When you call <code>put(Key, Value)</code>, HashMap calculates the hash code of the Key using its <code>hashCode()</code> method. It then applies a secondary bitwise hash function (<code>(n - 1) & hash</code>) to determine the exact <strong>Bucket Index</strong> (the specific slot in its internal array) where the data should go.</p>

<p><strong>Step 2: Collision Handling</strong></p>
<p>If two different keys produce the exact same bucket index, a <strong>Collision</strong> occurs. Before Java 8, the HashMap simply stored these colliding entries in a standard <strong>LinkedList</strong> hanging off that specific bucket. However, if a massive amount of collisions occurred, searching that bucket degraded from an optimal O(1) to a terrible O(n) performance.</p>

<p><strong>Step 3: Java 8 Red-Black Tree Optimization</strong></p>
<p>To fix the O(n) worst-case performance, Java 8 introduced a massive architectural optimization: If the number of nodes in a single bucket's LinkedList crosses a threshold (specifically <strong>8 elements</strong>), the HashMap automatically transforms that LinkedList into a self-balancing <strong>Red-Black Tree</strong>. This drastically improves the worst-case search performance from O(n) to an extremely fast <strong>O(log n)</strong>.</p>

<p><strong>Step 4: Rehashing (Load Factor)</strong></p>
<p>When the HashMap becomes 75% full (triggered by the default <code>0.75 Load Factor</code>), it automatically doubles its internal array capacity (e.g., from 16 to 32 buckets). It must then painstakingly recalculate the hashes for every single existing element and redistribute them into the new larger array. This is an expensive operation, which is why explicitly initializing a HashMap with a known capacity is a high-performance best practice.</p>"""

# 2. Update Comparable vs Comparator
for i in range(len(master_data)):
    if master_data[i].get('type') == 'question' and 'comparable' in master_data[i].get('content', '').lower() and 'comparator' in master_data[i].get('content', '').lower():
        if master_data[i+1].get('type') == 'theory':
            master_data[i+1]['content'] = """<table>
    <tr><th>Feature</th><th>Comparable</th><th>Comparator</th></tr>
    <tr><td><strong>Package</strong></td><td><code>java.lang.Comparable</code></td><td><code>java.util.Comparator</code></td></tr>
    <tr><td><strong>Method</strong></td><td><code>public int compareTo(Object o)</code></td><td><code>public int compare(Object o1, Object o2)</code></td></tr>
    <tr><td><strong>Sorting Logic</strong></td><td>Provides the <strong>Natural/Default Sorting</strong> order.</td><td>Provides <strong>Custom/Multiple Sorting</strong> logic.</td></tr>
    <tr><td><strong>Class Modification</strong></td><td>Requires modifying the actual domain class itself (e.g., <code>class Employee implements Comparable</code>).</td><td>Does not touch the original class. You create separate external classes or use inline Lambdas.</td></tr>
    <tr><td><strong>Usage Example</strong></td><td><code>Collections.sort(employees);</code></td><td><code>Collections.sort(employees, new SalaryComparator());</code></td></tr>
</table>
<br>
<strong>Notes & Real-World Example:</strong>
<ul>
    <li>If you have an `Employee` class, you implement <strong>Comparable</strong> to sort them by their `employeeId` by default.</li>
    <li>If the HR department suddenly requests to see the list sorted by <em>Salary</em>, and then later sorted by <em>Age</em>, you cannot change the hardcoded `compareTo()` method. Instead, you use <strong>Comparator</strong> to create external, swappable sorting algorithms on the fly (e.g., <code>employees.sort(Comparator.comparing(Employee::getSalary));</code>).</li>
</ul>"""

# 3. Add CompletableFuture question
completable_future_q = [
    {
        "type": "question",
        "content": "How do you execute asynchronous threads using Java 8 CompletableFuture?"
    },
    {
        "type": "theory",
        "content": "Prior to Java 8, managing asynchronous threads using the standard `Future` interface was incredibly clunky because the operations were **blocking** (calling `.get()` froze the main thread completely) and they couldn't be chained together.\n\nJava 8 introduced `CompletableFuture`, which allows you to build massive, non-blocking asynchronous pipelines. You can use `supplyAsync()` to spawn a background task on a separate thread (pulled from the common `ForkJoinPool`), and instantly chain callbacks like `thenApply()` or `thenAccept()` that will asynchronously execute **only when** the background thread finishes."
    },
    {
        "type": "code",
        "lang": "java",
        "content": "CompletableFuture.supplyAsync(() -> {\n    // Task 1: Runs in a separate background thread\n    System.out.println(\"Fetching data in thread: \" + Thread.currentThread().getName());\n    return \"Order#123\";\n})\n.thenApply(orderId -> {\n    // Task 2: Chained non-blocking operation\n    return \"Processing \" + orderId;\n})\n.thenAccept(result -> {\n    // Task 3: Terminal consumer operation\n    System.out.println(\"Final Result: \" + result);\n});"
    }
]

# Insert CompletableFuture into Multithreading
thread_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Multithreading' in item.get('content', ''):
        thread_index = i
        break

if thread_index != -1:
    master_data[thread_index+1:thread_index+1] = completable_future_q
else:
    master_data.append({"type": "category", "content": "Modern Multithreading"})
    master_data.extend(completable_future_q)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
