import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

table_replacements = {
    "difference between string and string buffer?": """<table>
<tr><th>Feature</th><th>String</th><th>StringBuffer</th></tr>
<tr><td><strong>Mutability</strong></td><td>Strictly Immutable. Every change creates a brand new object in memory.</td><td>Mutable. Can be modified directly without creating new objects.</td></tr>
<tr><td><strong>Thread Safety</strong></td><td>Inherently thread-safe (because it cannot change).</td><td>Thread-safe. All public methods are synchronized.</td></tr>
<tr><td><strong>Performance</strong></td><td>Slow for multiple concatenations (heavy memory overhead).</td><td>Fast for string manipulation, but slower than StringBuilder due to synchronization locks.</td></tr>
</table>""",

    "difference between == and equals": """<table>
<tr><th>Feature</th><th>== Operator</th><th>equals() Method</th></tr>
<tr><td><strong>Nature</strong></td><td>Operator</td><td>Method (defined in Object class)</td></tr>
<tr><td><strong>Comparison Type</strong></td><td><strong>Reference Comparison</strong>. Checks if both variables point to the exact same physical memory location.</td><td><strong>Content Comparison</strong>. Checks if the actual data/values inside the objects are logically identical.</td></tr>
<tr><td><strong>Overridability</strong></td><td>Cannot be overridden.</td><td>Can (and should) be overridden in custom classes to define logical equality.</td></tr>
</table>""",

    "what is exceptions? checked unchecked and how you handle them ? can you create  custom exceptions?": """<table>
<tr><th>Feature</th><th>Checked Exceptions</th><th>Unchecked Exceptions</th></tr>
<tr><td><strong>Class Hierarchy</strong></td><td>Extend <code>Exception</code> class (but not RuntimeException).</td><td>Extend <code>RuntimeException</code> class.</td></tr>
<tr><td><strong>Compiler Verification</strong></td><td>Checked at compile-time. The compiler strictly forces you to handle it with <code>try-catch</code> or declare it with <code>throws</code>.</td><td>Not checked at compile-time. Occur strictly at runtime.</td></tr>
<tr><td><strong>Root Cause</strong></td><td>External factors outside the program's immediate control (e.g., Network failure, File not found).</td><td>Programming errors or bad logic (e.g., Null pointer, Array index out of bounds).</td></tr>
<tr><td><strong>Examples</strong></td><td><code>IOException</code>, <code>SQLException</code></td><td><code>NullPointerException</code>, <code>IllegalArgumentException</code></td></tr>
</table>
<br><strong>Custom Exceptions:</strong> Yes, you can create them by extending `Exception` (for custom checked) or `RuntimeException` (for custom unchecked).""",

    "difference between arraylist and linkedlist?": """<table>
<tr><th>Feature</th><th>ArrayList</th><th>LinkedList</th></tr>
<tr><td><strong>Underlying Structure</strong></td><td>Dynamic Resizable Array.</td><td>Doubly Linked List.</td></tr>
<tr><td><strong>Search/Retrieval</strong></td><td>Very Fast: <strong>O(1)</strong> because it uses a direct memory index to fetch the element.</td><td>Slow: <strong>O(n)</strong> because it must traverse pointers sequentially from the head/tail.</td></tr>
<tr><td><strong>Insertion/Deletion</strong></td><td>Slow: <strong>O(n)</strong> because all subsequent elements must be physically shifted in memory to fill the gap.</td><td>Fast: <strong>O(1)</strong> (if node reference is known) because it merely updates surrounding memory pointers.</td></tr>
<tr><td><strong>Memory Overhead</strong></td><td>Low. Only stores the actual data elements.</td><td>High. Stores the data plus two extra memory pointers (Next and Prev) per node.</td></tr>
</table>""",

    "restcontroller vs controller?": """<table>
<tr><th>Feature</th><th>@Controller</th><th>@RestController</th></tr>
<tr><td><strong>Primary Use Case</strong></td><td>Traditional Spring MVC applications rendering UI pages (HTML/JSP).</td><td>Building RESTful Web Services/APIs returning raw JSON or XML.</td></tr>
<tr><td><strong>Return Behavior</strong></td><td>The returned string is intercepted by a <code>ViewResolver</code> to find a physical HTML template.</td><td>The returned object is automatically serialized into JSON and written directly to the HTTP response body.</td></tr>
<tr><td><strong>Composition</strong></td><td>Just <code>@Controller</code></td><td>It is a convenience annotation combining <code>@Controller</code> + <code>@ResponseBody</code>.</td></tr>
</table>""",

    "difference between rest and soap?": """<table>
<tr><th>Feature</th><th>REST (Representational State Transfer)</th><th>SOAP (Simple Object Access Protocol)</th></tr>
<tr><td><strong>Architecture</strong></td><td>Architectural Style / Guidelines.</td><td>Strict Protocol.</td></tr>
<tr><td><strong>Data Format</strong></td><td>Supports JSON, XML, HTML, Plain Text (JSON is the absolute standard).</td><td>Strictly XML only.</td></tr>
<tr><td><strong>Security</strong></td><td>Uses HTTPS and stateless JWT tokens.</td><td>Has built-in WS-Security (heavy enterprise-grade security protocols).</td></tr>
<tr><td><strong>Performance & Bandwidth</strong></td><td>Lightweight, fast, uses less bandwidth (JSON is much smaller).</td><td>Heavyweight, slow parsing, extremely large XML payloads.</td></tr>
</table>""",

    "put vs patch?": """<table>
<tr><th>Feature</th><th>PUT</th><th>PATCH</th></tr>
<tr><td><strong>Update Type</strong></td><td><strong>Full Update</strong> / Replacement.</td><td><strong>Partial Update</strong> / Modification.</td></tr>
<tr><td><strong>Payload Requirement</strong></td><td>You must send the *entire* object. If you omit a field in the JSON, the server overrides it to null in the database.</td><td>You only send the specific fields you actively want to change.</td></tr>
<tr><td><strong>Idempotency</strong></td><td>Idempotent (Running it 10 times has the exact same final state as 1 time).</td><td>Not strictly idempotent by default, depending on implementation.</td></tr>
</table>""",

    "delete vs drop vs truncate?": """<table>
<tr><th>Feature</th><th>DELETE</th><th>TRUNCATE</th><th>DROP</th></tr>
<tr><td><strong>Command Type</strong></td><td>DML (Data Manipulation Language)</td><td>DDL (Data Definition Language)</td><td>DDL</td></tr>
<tr><td><strong>Action</strong></td><td>Deletes specific rows based on a <code>WHERE</code> clause.</td><td>Instantly deletes <em>all</em> rows in the table. Leaves the empty table structure intact.</td><td>Violently destroys the entire table (data + structure + indexes).</td></tr>
<tr><td><strong>Rollback</strong></td><td>Can be successfully rolled back if executed inside a transaction.</td><td>Cannot be rolled back (it auto-commits immediately).</td><td>Cannot be rolled back.</td></tr>
<tr><td><strong>Performance</strong></td><td>Slow (the database must log every single row deletion into the transaction log).</td><td>Extremely fast (deallocates the data pages without logging individual rows).</td><td>Extremely fast.</td></tr>
</table>""",

    "diff between where and having?": """<table>
<tr><th>Feature</th><th>WHERE</th><th>HAVING</th></tr>
<tr><td><strong>Execution Phase</strong></td><td>Filters rows <strong>before</strong> any grouping (GROUP BY) occurs.</td><td>Filters groups <strong>after</strong> the grouping has occurred.</td></tr>
<tr><td><strong>Aggregate Functions</strong></td><td>Cannot contain aggregate functions like <code>SUM()</code> or <code>COUNT()</code>.</td><td>Explicitly designed to evaluate aggregate functions (e.g., <code>HAVING COUNT(id) > 5</code>).</td></tr>
<tr><td><strong>Performance</strong></td><td>Faster because it aggressively eliminates unnecessary rows early in the pipeline.</td><td>Slower because grouping calculations must happen first.</td></tr>
</table>""",

    "difference between postgresql and mysql": """<table>
<tr><th>Feature</th><th>PostgreSQL</th><th>MySQL</th></tr>
<tr><td><strong>Nature</strong></td><td>Object-Relational Database Management System (ORDBMS). Highly strictly compliant with SQL standards.</td><td>Pure Relational Database Management System (RDBMS). Historically focuses on pure speed over strict compliance.</td></tr>
<tr><td><strong>Complex Queries</strong></td><td>Incredible performance for complex aggregations, massive JOINs, and Window functions.</td><td>Can struggle with highly complex queries; historically preferred for simple, fast read-heavy web apps.</td></tr>
<tr><td><strong>Advanced Features</strong></td><td>Native support for JSONB, User-Defined Types (UDT), Table Inheritance, and array data types.</td><td>Limited advanced data types. JSON support exists but is significantly less robust than Postgres JSONB.</td></tr>
</table>""",

    "rank vs dense rank? what is nvl()?": """<table>
<tr><th>Feature</th><th>RANK()</th><th>DENSE_RANK()</th></tr>
<tr><td><strong>Handling Ties</strong></td><td>Assigns the exact same rank to duplicate values.</td><td>Assigns the exact same rank to duplicate values.</td></tr>
<tr><td><strong>Subsequent Rank Number</strong></td><td><strong>Skips</strong> the next rank number. (e.g., Ranks: 1, 1, 3).</td><td><strong>Does not skip</strong> the next rank number. (e.g., Ranks: 1, 1, 2).</td></tr>
<tr><td><strong>Best Use Case</strong></td><td>General rankings where a "tie for first" officially eliminates second place.</td><td>Finding the "Nth Highest Salary" because it mathematically guarantees contiguous numbers.</td></tr>
</table>
<br><strong>What is NVL()?</strong> NVL() is an Oracle-specific SQL function used to gracefully handle NULL values. `NVL(column, 'default_value')` replaces nulls with a default. In standard SQL/Postgres, you use `COALESCE()`.""",

    "method vs constructor?": """<table>
<tr><th>Feature</th><th>Method</th><th>Constructor</th></tr>
<tr><td><strong>Purpose</strong></td><td>Defines the behavior or actions an object can perform.</td><td>Initializes the internal state of a newly created object.</td></tr>
<tr><td><strong>Return Type</strong></td><td>Must have a return type (or <code>void</code>).</td><td>Cannot have any return type whatsoever (not even <code>void</code>).</td></tr>
<tr><td><strong>Invocation</strong></td><td>Called explicitly by the programmer on an existing object instance.</td><td>Called implicitly and automatically by the JVM using the <code>new</code> keyword.</td></tr>
<tr><td><strong>Naming Convention</strong></td><td>Can be named anything (usually camelCase).</td><td>Must perfectly match the exact Class name.</td></tr>
</table>""",

    "what is fail fast and fail safe iterators?": """<table>
<tr><th>Feature</th><th>Fail-Fast Iterators</th><th>Fail-Safe Iterators</th></tr>
<tr><td><strong>Data Source</strong></td><td>Iterates directly over the actual, original collection memory array.</td><td>Iterates over a clone/snapshot of the collection.</td></tr>
<tr><td><strong>Concurrent Modification</strong></td><td>If Thread B modifies the collection while Thread A is iterating, it immediately aborts and throws a <code>ConcurrentModificationException</code>.</td><td>If Thread B modifies the collection, Thread A's iterator is completely unaffected. No exception is thrown.</td></tr>
<tr><td><strong>Performance / Memory</strong></td><td>Fast and requires zero extra memory.</td><td>Slower and consumes double the memory because it clones the array.</td></tr>
<tr><td><strong>Examples</strong></td><td><code>ArrayList</code>, <code>HashMap</code>, <code>HashSet</code></td><td><code>CopyOnWriteArrayList</code>, <code>ConcurrentHashMap</code></td></tr>
</table>""",

    "concurrenthashmap vs collections.synchronizedmap() - why is one preferred?": """<table>
<tr><th>Feature</th><th>Collections.synchronizedMap()</th><th>ConcurrentHashMap</th></tr>
<tr><td><strong>Locking Mechanism</strong></td><td><strong>Object-Level Locking.</strong> Uses a single massive global lock for the entire map object.</td><td><strong>Segment-Level Locking (Lock Stripping).</strong> Divides the map into segments (usually 16 independent locks).</td></tr>
<tr><td><strong>Concurrency / Throughput</strong></td><td>Terrible under load. If Thread A writes, Thread B is completely blocked from reading or writing anything until A finishes.</td><td>Incredible under load. Thread A can write to Segment 1 while Thread B simultaneously writes to Segment 2. Reads do not block at all.</td></tr>
<tr><td><strong>Null Handling</strong></td><td>Allows one <code>null</code> key and multiple <code>null</code> values (if the underlying map is HashMap).</td><td>Strictly forbids <code>null</code> keys and <code>null</code> values (throws NullPointerException).</td></tr>
</table>""",

    "difference between procedure and function?": """<table>
<tr><th>Feature</th><th>Stored Procedure</th><th>Function</th></tr>
<tr><td><strong>Return Value</strong></td><td>Can return zero values, or multiple values via <code>OUT</code> parameters.</td><td><strong>Must</strong> return exactly one single value.</td></tr>
<tr><td><strong>DML Operations</strong></td><td>Can actively modify database state using <code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>.</td><td>Generally forbidden from modifying database state (read-only computations).</td></tr>
<tr><td><strong>Invocation / Usage</strong></td><td>Cannot be used in a <code>SELECT</code> statement. Must be executed via <code>CALL</code> or <code>EXEC</code>.</td><td>Can be used smoothly inline inside <code>SELECT</code>, <code>WHERE</code>, or <code>HAVING</code> clauses.</td></tr>
<tr><td><strong>Transaction Management</strong></td><td>Can manage complex transactions internally (can use <code>COMMIT</code> and <code>ROLLBACK</code>).</td><td>Cannot manage transactions.</td></tr>
</table>""",

    "view vs materialized view?": """<table>
<tr><th>Feature</th><th>View</th><th>Materialized View</th></tr>
<tr><td><strong>Physical Storage</strong></td><td>Virtual. It does not physically store any data on the disk.</td><td>Physical. It actually executes the query and stores the physical result set on the disk.</td></tr>
<tr><td><strong>Performance</strong></td><td>Slower. The database must re-execute the complex underlying <code>SELECT</code> query every single time it is called.</td><td>Lightning fast. Because the data is already computed and sitting on disk, retrieval is instant.</td></tr>
<tr><td><strong>Data Freshness</strong></td><td>Always 100% up-to-date real-time data.</td><td>Data becomes stale. It must be manually refreshed (<code>REFRESH MATERIALIZED VIEW</code>) or updated via cron jobs/triggers.</td></tr>
</table>""",

    "cursor vs records in sql?": """<table>
<tr><th>Feature</th><th>Cursor</th><th>Record (RowType)</th></tr>
<tr><td><strong>Purpose</strong></td><td>A control structure used to iterate through a massive result set <strong>row-by-row</strong> (like a while-loop).</td><td>A composite data type variable used to temporarily hold exactly <strong>one row</strong> of fetched data in memory.</td></tr>
<tr><td><strong>Performance</strong></td><td>Extremely slow because relational databases are designed for Set-based operations, not procedural looping.</td><td>N/A (It is simply a variable type).</td></tr>
<tr><td><strong>Analogy</strong></td><td>The <code>Iterator</code> object traversing a Java List.</td><td>The <code>Employee</code> object holding the data for one iteration.</td></tr>
</table>""",

    "what is decode vs case? what is a sequence?": """<table>
<tr><th>Feature</th><th>DECODE()</th><th>CASE WHEN</th></tr>
<tr><td><strong>SQL Standard</strong></td><td>Oracle-specific proprietary function.</td><td>Universal ANSI SQL standard (works in Postgres, MySQL, Oracle, SQL Server).</td></tr>
<tr><td><strong>Evaluation Capability</strong></td><td>Can only evaluate strict equality (e.g., <code>status = 1</code>).</td><td>Can evaluate complex logic, inequalities, and multiple columns (e.g., <code>status > 1 AND age < 30</code>).</td></tr>
<tr><td><strong>Readability</strong></td><td>Compact, but gets extremely messy and unreadable when nested.</td><td>Highly readable, structured like a standard programming switch/if-else block.</td></tr>
</table>
<br><strong>What is a Sequence?</strong> A Sequence is an independent database object that generates a continuous stream of unique integers. It is primarily used to auto-populate Primary Keys, akin to `AUTO_INCREMENT` in MySQL or the `SERIAL` pseudo-type in PostgreSQL.""",
    
    "what is hs256 and rs256? (256 encryption in jwt)": """<table>
<tr><th>Feature</th><th>HS256 (HMAC with SHA-256)</th><th>RS256 (RSA Signature with SHA-256)</th></tr>
<tr><td><strong>Encryption Type</strong></td><td><strong>Symmetric Algorithm</strong>.</td><td><strong>Asymmetric Algorithm</strong>.</td></tr>
<tr><td><strong>Key Usage</strong></td><td>Uses the exact same <strong>Shared Secret Key</strong> to both sign the token and verify the token.</td><td>Uses a <strong>Private Key</strong> (kept strictly on the Auth Server) to sign, and a <strong>Public Key</strong> (distributed everywhere) to verify.</td></tr>
<tr><td><strong>Security Risk</strong></td><td>If one microservice is compromised, the shared secret key is leaked, allowing the hacker to forge valid admin tokens.</td><td>Extremely secure. If a microservice is compromised, the hacker only gets the Public Key (can only verify, cannot forge).</td></tr>
<tr><td><strong>Best Use Case</strong></td><td>Small monolithic applications or tightly coupled internal services.</td><td>Large distributed Microservice architectures or public APIs (like Google OAuth).</td></tr>
</table>"""
}

# Apply the replacements
for i, item in enumerate(master_data):
    if item.get('type') == 'question':
        q_text = item.get('content', '').lower()
        
        # Exact match logic (ignoring case and whitespace)
        for key, new_table in table_replacements.items():
            if key in q_text or q_text in key:
                if i + 1 < len(master_data) and master_data[i+1].get('type') == 'theory':
                    master_data[i+1]['content'] = new_table
                break

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
