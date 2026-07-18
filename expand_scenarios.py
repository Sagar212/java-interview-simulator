import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

# 1. Expand "What is JWT?"
for i in range(len(master_data)):
    if master_data[i].get('type') == 'question' and 'jwt' in master_data[i].get('content', '').lower():
        if i + 1 < len(master_data) and master_data[i+1].get('type') == 'theory':
            master_data[i+1]['content'] = """<p><strong>JSON Web Token (JWT)</strong> is an open standard for securely transmitting information between parties as a JSON object. It is completely <strong>stateless</strong>, meaning the server does not need to store active sessions in its database (unlike traditional session cookies).</p>

<p><strong>The 3 Parts of a JWT:</strong></p>
<ol>
    <li><strong>Header:</strong> Specifies the token type (JWT) and the signing algorithm being used (e.g., HS256 or RS256).</li>
    <li><strong>Payload (Claims):</strong> Contains the actual data you want to transmit (e.g., <code>{"userId": 123, "role": "ADMIN", "exp": 1699999999}</code>). <em>Crucially, this is merely Base64 encoded, NOT encrypted! Anyone can easily decode and read this data, so never put passwords or sensitive information here.</em></li>
    <li><strong>Signature:</strong> The most critical security component. The server takes the Header, Payload, and its own secret Private Key, and hashes them together. When the client sends the token back on the next request, the server recalculates the signature. If a hacker maliciously altered the payload (e.g., changed "role" to "SUPERADMIN"), the signatures will immediately fail to match, and the server will instantly reject the token with a 401 Unauthorized error.</li>
</ol>"""

# 2. Add Bank Scenarios
bank_scenarios = [
    {
        "type": "question",
        "content": "Bank Scenario: How do you prevent 'Double Spending' when an impatient user clicks the 'Pay' button twice rapidly?"
    },
    {
        "type": "theory",
        "content": "Double spending is a critical issue in payment gateways. If a user impatiently clicks 'Submit Payment' twice, the browser might send two identical API requests simultaneously.\n\n**Solution: Idempotency Keys**\n1. The frontend generates a unique UUID (the Idempotency Key) for the transaction and attaches it to the HTTP Headers of the `POST` request.\n2. When the server receives the request, it checks a fast in-memory database (like **Redis**) to see if this UUID already exists.\n3. **Request 1** arrives, the UUID is not found. The server locks the UUID in Redis, processes the actual payment with Stripe/Visa, and saves the successful HTTP response in Redis against that exact UUID.\n4. **Request 2** arrives just milliseconds later. The server checks Redis, sees the UUID is already locked/processed, and immediately returns the cached success response *without* ever hitting the payment gateway a second time."
    },
    {
        "type": "question",
        "content": "Bank Scenario: Two users try to withdraw the exact same last $100 from a joint account at the exact same millisecond. How do you handle this?"
    },
    {
        "type": "theory",
        "content": "This is a classic **Race Condition**. If both threads read the balance as $100 simultaneously, both will pass the validation check, resulting in the account illegally going to -$100.\n\n**Solution 1: Pessimistic Locking (Database Level)**\nUse `SELECT * FROM accounts WHERE id = 1 FOR UPDATE`. This strictly locks the physical database row. The first transaction acquires the lock, while the second transaction is forced to wait until the first commits or rolls back. It is incredibly safe, but severely degrades system performance under high load.\n\n**Solution 2: Optimistic Locking (Hibernate/Application Level - Preferred)**\nAdd a `@Version` column (an integer) to the Account entity. \n1. Both threads read the balance ($100) and version (`v=1`).\n2. Thread A deducts $100 and updates the row: `UPDATE accounts SET balance = 0, version = 2 WHERE id = 1 AND version = 1`. This fully succeeds.\n3. Thread B tries to update: `UPDATE accounts ... WHERE id = 1 AND version = 1`. Because Thread A already changed the database version to 2, Thread B's query affects 0 rows. \n4. Hibernate detects this 0 row update and violently throws an `OptimisticLockException`. You catch this exception and tell User B: \"Transaction failed due to concurrent modification, please try again.\""
    },
    {
        "type": "question",
        "content": "Bank Scenario: Distributed Transactions. Deducting money in 'Account Service', but adding money in 'Wallet Service' fails."
    },
    {
        "type": "theory",
        "content": "In a legacy monolithic application, you simply use Spring's `@Transactional` to roll back the entire database. However, in Microservices, the 'Account Service' and 'Wallet Service' have completely different, physically isolated databases. You cannot use a standard database transaction across the network.\n\n**Solution: The Saga Pattern (Event-Driven Architecture)**\nInstead of a single distributed lock (like the extremely slow Two-Phase Commit / 2PC), you use **Compensating Transactions**.\n1. Account Service deducts $100 and publishes a `PaymentDeductedEvent` to a Kafka broker.\n2. Wallet Service consumes the event and attempts to deposit $100. \n3. If Wallet Service's database is down and it fails, it publishes a `DepositFailedEvent` back to Kafka.\n4. Account Service listens for `DepositFailedEvent` and automatically executes a **Compensating Transaction**: it runs a brand new SQL query to refund the $100 back to the user's account, achieving **Eventual Consistency**."
    }
]

# 3. Add Collections Table
collections_table = [
    {
        "type": "question",
        "content": "When should you use each Collection? (Data Structures Cheat Sheet)"
    },
    {
        "type": "theory",
        "content": """<table>
    <tr><th>Collection</th><th>Key Characteristic</th><th>When to Use? (Real-World Scenario)</th></tr>
    <tr><td><strong>ArrayList</strong></td><td>Fast Iteration, Slow Insertion/Deletion (O(n)).</td><td>Read-heavy operations. E.g., Storing a massive catalog of products to display on an e-commerce webpage.</td></tr>
    <tr><td><strong>LinkedList</strong></td><td>Fast Insertion/Deletion (O(1)), Slow Iteration (O(n)).</td><td>Write-heavy operations. E.g., Implementing a queue for a messaging system where items are constantly being added and removed from the ends.</td></tr>
    <tr><td><strong>HashSet</strong></td><td>No duplicates, No ordering, Fast lookups (O(1)).</td><td>When you need to quickly check if an element exists. E.g., Checking if a username is already taken during registration.</td></tr>
    <tr><td><strong>TreeSet</strong></td><td>No duplicates, Automatically Sorted (O(log n)).</td><td>When you need a unique, constantly sorted list. E.g., Displaying a live leaderboard of top scores in a game.</td></tr>
    <tr><td><strong>HashMap</strong></td><td>Key-Value pairs, Unordered, Fast lookups (O(1)).</td><td>Caching data. E.g., Storing user session data where the key is the highly unique Session ID.</td></tr>
    <tr><td><strong>TreeMap</strong></td><td>Key-Value pairs, Sorted by Key (O(log n)).</td><td>When you need to retrieve a sequential range of keys. E.g., Fetching all transactions between two specific dates.</td></tr>
    <tr><td><strong>ConcurrentHashMap</strong></td><td>Thread-safe, Segment-level locking.</td><td>When multiple threads need to read/write to a shared cache simultaneously without locking the entire map and causing bottlenecks.</td></tr>
</table>"""
    }
]

# Inject Bank scenarios under Spring Boot & Architecture
arch_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Architecture' in item.get('content', ''):
        arch_index = i
        break

if arch_index != -1:
    master_data[arch_index+1:arch_index+1] = bank_scenarios

# Inject Collections table under Collections Framework
coll_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Collections Framework' in item.get('content', ''):
        coll_index = i
        break

if coll_index != -1:
    master_data[coll_index+1:coll_index+1] = collections_table

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
