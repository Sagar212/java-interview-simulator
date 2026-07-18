import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

new_questions = [
    {
        "type": "question",
        "content": "Stateless vs Stateful Architecture?"
    },
    {
        "type": "theory",
        "content": """<table>
    <tr><th>Feature</th><th>Stateless Architecture</th><th>Stateful Architecture</th></tr>
    <tr><td><strong>Definition</strong></td><td>The server does not store any client session data. Every single HTTP request contains all the information needed to process it independently.</td><td>The server explicitly remembers client data (session state) across multiple sequential requests.</td></tr>
    <tr><td><strong>Authentication</strong></td><td>Uses <strong>JWT (JSON Web Tokens)</strong>. The client passes the full token in the Authorization header on every request.</td><td>Uses <strong>Session IDs</strong>. The server stores the heavy session object in memory, and the client just sends a tiny tracking Cookie.</td></tr>
    <tr><td><strong>Scalability</strong></td><td>Extremely easy to scale horizontally. Because there is no state, a load balancer can route the user's next request to <em>any</em> available server instance.</td><td>Very difficult to scale. Requires configuring "Sticky Sessions" on the load balancer (forcing the user to hit the exact same server) or implementing an external distributed cache like Redis.</td></tr>
    <tr><td><strong>REST Compliance</strong></td><td>Strictly adheres to REST principles.</td><td>Violates strict REST principles.</td></tr>
</table>"""
    },
    {
        "type": "question",
        "content": "What is the difference between ROWNUM and ROWID in SQL?"
    },
    {
        "type": "theory",
        "content": "- **ROWID**: A highly specific, physical hexadecimal address representing the exact location of a row on the database disk. It is permanent and never changes as long as the row exists. Querying by ROWID is the absolute fastest way to access a row in Oracle.\n- **ROWNUM**: A temporary, logical pseudo-column that assigns sequential integers (1, 2, 3) to the rows *after* they are fetched from the table, but *before* the `ORDER BY` sorting is applied. It is primarily used to restrict result sets (e.g., `WHERE ROWNUM <= 10`)."
    },
    {
        "type": "question",
        "content": "How exactly do you call a Stored Procedure versus a Function in SQL?"
    },
    {
        "type": "theory",
        "content": "- **Calling a Function**: Because functions must return a single value and are forbidden from modifying database state, they are invoked directly inline within standard DML statements like `SELECT` or `WHERE`.\n`SELECT employee_name, calculate_tax(salary) FROM employees;`\n\n- **Calling a Procedure**: Because procedures can return zero values (or multiple `OUT` parameters) and are actively used to modify database state (`INSERT`/`UPDATE`), they **cannot** be used inside a `SELECT` statement. They must be explicitly invoked using the `CALL` or `EXEC` commands.\n`CALL update_department_salaries(10, 5000);`"
    },
    {
        "type": "category",
        "content": "Top-Tier Tech Questions (Morgan Stanley, Deloitte, Wipro)"
    },
    {
        "type": "question",
        "content": "Why is the String class heavily strictly Immutable in Java?"
    },
    {
        "type": "theory",
        "content": "This is an extremely common banking interview question. String is immutable for three critical reasons:\n1. **Security**: Strings are heavily used to store sensitive data like database URLs, usernames, and passwords. If String were mutable, a malicious thread could intercept and alter the string reference before it hits the database.\n2. **String Pool Caching**: Because Strings cannot change, Java can safely cache them in a special memory area called the String Constant Pool. If multiple variables contain the exact same text, they simply point to the exact same memory address, saving massive amounts of RAM.\n3. **Thread Safety**: Immutable objects are inherently completely thread-safe. Multiple threads can read a String simultaneously without requiring synchronized locks."
    },
    {
        "type": "question",
        "content": "ConcurrentHashMap vs Collections.synchronizedMap() - Why is one preferred?"
    },
    {
        "type": "theory",
        "content": "Both are thread-safe Maps, but their underlying architectures are vastly different:\n- **Collections.synchronizedMap()**: Uses **Object-Level Locking**. If Thread A is reading from the map, it locks the *entire* map. Thread B is completely blocked from reading or writing anything until Thread A finishes. Performance degrades heavily under load.\n- **ConcurrentHashMap**: Uses **Segment-Level Locking (Lock Stripping)**. It divides the map into segments (usually 16). Thread A can lock Segment 1 to perform an update, while Thread B can safely write to Segment 2 simultaneously without any blocking. Reads do not require locks at all. It is vastly superior for highly concurrent applications."
    },
    {
        "type": "question",
        "content": "Why use the ExecutorService framework instead of manually creating Threads?"
    },
    {
        "type": "theory",
        "content": "Manually doing `new Thread(() -> {}).start()` inside a web request loop is a massive anti-pattern.\n1. **Resource Exhaustion**: Threads are heavy OS-level objects. Spawning 10,000 unmanaged threads will crash the JVM with an `OutOfMemoryError`.\n2. **Context Switching Overhead**: The CPU spends more time switching between thousands of threads than actually executing logic.\n\nThe **ExecutorService** solves this by implementing a **Thread Pool**. It creates a fixed number of reusable threads (e.g., 50). When a task arrives, it is handed to an idle thread. When the task finishes, the thread doesn't die; it returns to the pool to process the next task, saving immense creation/destruction overhead."
    },
    {
        "type": "question",
        "content": "Fail-Fast vs Fail-Safe Iterators?"
    },
    {
        "type": "theory",
        "content": "- **Fail-Fast**: (e.g., `ArrayList`, `HashMap`). These iterate directly over the actual underlying collection. If Thread B attempts to structurally modify the collection (add or remove elements) while Thread A is currently iterating through it, the Iterator immediately aborts and throws a `ConcurrentModificationException`.\n- **Fail-Safe**: (e.g., `CopyOnWriteArrayList`, `ConcurrentHashMap`). These iterate over a **clone/snapshot** of the underlying collection. Therefore, if Thread B modifies the original collection during iteration, Thread A's iterator does not care and no exception is thrown."
    }
]

# Insert the new questions. 
# We'll put the architectural/DB questions before the new Top-Tier category, 
# and append the top-tier category at the end.

# Split the list
db_questions = new_questions[0:6]
top_tier_questions = new_questions[6:]

# Find DB category to insert DB questions
db_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Database & SQL' in item.get('content', ''):
        db_index = i
        break

if db_index != -1:
    master_data[db_index+1:db_index+1] = db_questions
else:
    master_data.append({"type": "category", "content": "Database Nuances"})
    master_data.extend(db_questions)

master_data.extend(top_tier_questions)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
