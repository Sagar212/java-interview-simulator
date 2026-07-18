import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

new_db_questions = [
    {
        "type": "question",
        "content": "What is an Idempotent Operation?"
    },
    {
        "type": "theory",
        "content": "An operation is **idempotent** if executing it multiple times produces the exact same result as executing it once. \n\nIn REST APIs, `GET`, `PUT` (update entirely), and `DELETE` are idempotent. `POST` is NOT idempotent (clicking a checkout button twice creates two separate orders). \n\n**Real-World Scenario**: In payment gateways, clients send a unique \"Idempotency-Key\" in the HTTP header. If the network times out and the client retries the exact same payment request, the server checks the key, realizes it already processed that exact transaction, and simply returns the cached success response without charging the credit card twice."
    },
    {
        "type": "question",
        "content": "Ensuring OTP is the same for Client and Server (Validation Flow)?"
    },
    {
        "type": "theory",
        "content": "When a user requests an OTP:\n1. The server generates a random 6-digit secure string.\n2. The server hashes it (e.g., using SHA-256) and stores it in an in-memory cache like **Redis**, using the user's phone number or session ID as the key, with a strict 3-minute Time-To-Live (TTL).\n3. The raw OTP is sent to the client via SMS.\n4. When the client submits the OTP, the server hashes the input and compares it to the hash in Redis. \n5. If they match, authentication succeeds and the Redis key is immediately deleted to prevent **Replay Attacks**."
    },
    {
        "type": "question",
        "content": "Bank Scenario: ACID Properties & Atomicity"
    },
    {
        "type": "theory",
        "content": "ACID stands for Atomicity, Consistency, Isolation, Durability.\n\n**Atomicity** guarantees \"all or nothing\". \n**Scenario**: Transferring $100 from Account A to Account B involves two database queries:\n1. Deduct $100 from A.\n2. Add $100 to B.\nIf the server crashes after step 1 but before step 2, Atomicity ensures the database completely **rolls back** the entire transaction. The money isn't lost in the void. In Spring Boot, this is achieved by wrapping the service method in the `@Transactional` annotation."
    },
    {
        "type": "question",
        "content": "Bank Scenario: Auditing and Status Tracking"
    },
    {
        "type": "theory",
        "content": "In highly regulated financial systems, records are **never hard-deleted** (`DELETE FROM...`). \nInstead, a `status` column (e.g., 'PENDING', 'SUCCESS', 'FAILED', 'REVERSED') is used (Soft Deletion).\n\nTo ensure an immutable ledger, auditing tables (like `transaction_history`) track every state change. This is typically implemented at the database level using **AFTER UPDATE Triggers**, or at the application level using Hibernate Envers. Every modification logs the old value, new value, `updated_by` user ID, and exact timestamp."
    },
    {
        "type": "question",
        "content": "Trigger vs Procedure vs Function?"
    },
    {
        "type": "theory",
        "content": "- **Function**: Must return a single value. Can be executed inline within a `SELECT` statement. Generally cannot modify database state (No DML like INSERT/UPDATE).\n- **Procedure**: Can return zero or multiple values via `OUT` parameters. Used to execute complex business logic and DML operations. Cannot be used inside a `SELECT` statement (must be invoked via `CALL`).\n- **Trigger**: Cannot be called manually by a user. It executes **automatically** in response to specific DML events (INSERT/UPDATE/DELETE) on a table."
    },
    {
        "type": "question",
        "content": "What are the different Types of Triggers?"
    },
    {
        "type": "theory",
        "content": "1. **BEFORE Trigger**: Fires right before the DML operation executes. Extremely useful for data validation or sanitization (e.g., forcing an email string to lowercase before it hits the disk).\n2. **AFTER Trigger**: Fires immediately after the DML succeeds. Strictly used for cascading actions like auditing (e.g., inserting a copy of the old row into a history table).\n3. **INSTEAD OF Trigger**: Completely intercepts and replaces the DML operation. Most commonly used on complex Views to make them updatable, writing the data to the underlying base tables instead."
    },
    {
        "type": "question",
        "content": "View vs Materialized View?"
    },
    {
        "type": "theory",
        "content": "- **View**: A virtual table representing the result of a stored SQL query. It stores zero actual data. Every single time you query the view, the database re-executes the underlying `SELECT` statement.\n- **Materialized View**: Physically stores the result set of the query on the disk. It is incredibly fast for reading massive, complex aggregations. However, the data can become stale if the base tables change, requiring it to be manually refreshed (`REFRESH MATERIALIZED VIEW`) or refreshed via scheduled cron jobs/triggers."
    },
    {
        "type": "question",
        "content": "What are Temporary Tables?"
    },
    {
        "type": "theory",
        "content": "Temporary tables are specialized tables that exist entirely in memory (or a dedicated temp disk space) and only exist for the **duration of the database session or transaction**. \nOnce the connection closes, the table and all its data are automatically destroyed. They are highly efficient for storing intermediate results when performing complex data transformations inside a massive Stored Procedure."
    },
    {
        "type": "question",
        "content": "Pagination: SQL vs Hibernate"
    },
    {
        "type": "theory",
        "content": "Attempting to load 1 million rows into Java at once will cause an `OutOfMemoryError`. Pagination loads data in small chunks.\n\n**In SQL**: You use `LIMIT` and `OFFSET`. \n`SELECT * FROM employees ORDER BY id LIMIT 50 OFFSET 100` (Fetches 50 records, skipping the first 100. Ergo, Page 3).\n\n**In Spring Data JPA / Hibernate**: You pass a `Pageable` object.\n`Page<Employee> page = repo.findAll(PageRequest.of(2, 50));`\nSpring automatically translates this into the optimal database-specific pagination query and returns metadata like `getTotalPages()`."
    },
    {
        "type": "question",
        "content": "SQL Batch Inserts vs Single Inserts?"
    },
    {
        "type": "theory",
        "content": "If you need to insert 10,000 records, executing 10,000 separate `INSERT` statements causes massive network round-trip latency and immense transaction log overhead.\n\n**Batch Inserting** sends the data in one giant chunk over the network:\n`INSERT INTO my_table (col1, col2) VALUES (1,2), (3,4), (5,6)...`\n\nIn **Hibernate**, this is automated by setting `spring.jpa.properties.hibernate.jdbc.batch_size=50`. Hibernate will automatically queue up inserts in memory and flush them to the database in batches of 50, resulting in a 10x to 100x performance boost."
    },
    {
        "type": "question",
        "content": "Cursor vs Records in SQL?"
    },
    {
        "type": "theory",
        "content": "Relational Databases are heavily optimized for **Set-Based** operations (updating thousands of rows simultaneously with one command).\n\nA **Cursor** allows you to iterate through a result set **row-by-row**, similar to a `for` loop in Java. Cursors are notoriously slow and consume heavy memory; they should only be used as a last resort when complex procedural logic cannot be achieved with standard SQL `JOIN`s.\n\nA **Record** (or RowType) is simply a composite data type in PL/SQL that can hold an entire fetched row of data during the cursor iteration."
    },
    {
        "type": "question",
        "content": "What is DECODE vs CASE? What is a Sequence?"
    },
    {
        "type": "theory",
        "content": "`DECODE()` is an Oracle-specific function that behaves like an IF-THEN-ELSE switch. \nExample: `DECODE(status_id, 1, 'Active', 2, 'Inactive', 'Unknown')`. \nStandard ANSI SQL uses `CASE WHEN status_id = 1 THEN 'Active' ELSE 'Unknown' END`, which is universally preferred because it supports complex inequalities (`> 5`).\n\nA **Sequence** is an independent database object that generates a continuous stream of unique integers. It is primarily used to auto-populate Primary Keys, akin to `AUTO_INCREMENT` in MySQL or the `SERIAL` pseudo-type in PostgreSQL."
    }
]

# We want to insert these into the final list, ideally right under the "Database & SQL" category and some under "Spring Boot & Architecture".
# The easiest way is to append them before the "Other Important Concepts" category or at the end.
# Actually, the user asked to expand on databases, so appending them directly into the "Database & SQL" category would be best.

db_index = -1
for i, item in enumerate(master_data):
    if item['type'] == 'category' and item['content'] == 'Database & SQL':
        db_index = i
        break

if db_index != -1:
    # Find where the next category starts
    next_cat_index = len(master_data)
    for i in range(db_index + 1, len(master_data)):
        if master_data[i]['type'] == 'category':
            next_cat_index = i
            break
    
    # Insert new DB questions at the end of the Database category
    master_data[db_index+1:db_index+1] = new_db_questions
else:
    # Fallback, just append
    master_data.append({"type": "category", "content": "Advanced Databases, Architecture & Triggers"})
    master_data.extend(new_db_questions)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
