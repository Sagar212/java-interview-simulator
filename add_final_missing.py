import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

missing_questions = [
    {
        "type": "question",
        "content": "How do you check if a JWT token is expired in cache?"
    },
    {
        "type": "theory",
        "content": "JWT tokens inherently contain an `exp` (expiration time) claim directly inside their payload. You do **not** need to query a database or cache to check for expiration. The server simply decodes the payload and checks if the current server time is past the `exp` timestamp.\n\nHowever, if you want to **force-invalidate** a token *before* it naturally expires (e.g., the user clicks \"Logout\"), you store the token in a Redis cache as a \"blacklist\". The server must then check this Redis cache on every single request to verify the token hasn't been manually revoked."
    },
    {
        "type": "question",
        "content": "What are different HTTP methods? Can we use POST for updating?"
    },
    {
        "type": "theory",
        "content": "Common HTTP methods map to CRUD operations: `GET` (Retrieve), `POST` (Create), `PUT` (Full Replace), `PATCH` (Partial Update), and `DELETE` (Remove).\n\nYes, technically you *can* use `POST` for updating records (and many legacy APIs do). However, it severely violates strict RESTful conventions. `POST` is explicitly non-idempotent (calling it twice creates two resources), whereas updates should use `PUT` or `PATCH`, which are mathematically designed to be idempotent."
    },
    {
        "type": "question",
        "content": "Explain the role of tracing and correlation IDs in a distributed Spring Boot application."
    },
    {
        "type": "theory",
        "content": "In a Microservices architecture, a single user click might trigger a request that travels through 5 different services (API Gateway -> Auth -> Order -> Inventory -> Payment). If an error occurs deep in the Payment service, reading disjointed logs across 5 servers to find out what happened is impossible.\n\nTo solve this, we use **Distributed Tracing** (via Zipkin, Jaeger, or Spring Cloud Sleuth/Micrometer). When the request hits the very first API Gateway, it generates a unique UUID called a **Correlation ID** (or Trace ID). This ID is attached to the HTTP headers and passed to every subsequent service. All servers print this Correlation ID in their logs, allowing developers to query Logstash/Splunk for that exact ID and view the entire chronological lifecycle of the failed request."
    },
    {
        "type": "question",
        "content": "Difference between Spring MVC and Spring Boot?"
    },
    {
        "type": "theory",
        "content": """<table>
<tr><th>Feature</th><th>Spring MVC</th><th>Spring Boot</th></tr>
<tr><td><strong>Nature</strong></td><td>A web framework that is part of the core Spring Framework.</td><td>A complete ecosystem built <em>on top</em> of Spring MVC to simplify it.</td></tr>
<tr><td><strong>Configuration</strong></td><td>Requires massive amounts of manual XML or Java configuration (DispatcherServlet, ViewResolvers).</td><td>Eliminates boilerplate via Auto-Configuration (<code>@SpringBootApplication</code>).</td></tr>
<tr><td><strong>Deployment</strong></td><td>You must manually package a WAR file and deploy it to an external Tomcat/JBoss server.</td><td>Embeds a Tomcat server directly inside the JAR file, allowing you to run the app with a simple <code>java -jar</code> command.</td></tr>
</table>"""
    },
    {
        "type": "question",
        "content": "What are the uses of pom.xml and application.yml?"
    },
    {
        "type": "theory",
        "content": "- **`pom.xml` (Project Object Model)**: The core configuration file used by the **Maven** build tool. It manages the project's dependencies (downloading external JAR libraries like Spring Web or PostgreSQL Driver from the internet), build plugins, and the compilation lifecycle.\n- **`application.yml`**: A configuration file used strictly by **Spring Boot** at runtime (an alternative to `application.properties`). It stores environment-specific settings like Database URLs, credentials, server ports, logging levels, and custom business properties in a highly readable hierarchical YAML format."
    },
    {
        "type": "question",
        "content": "How do you execute a stored procedure in Java code?"
    },
    {
        "type": "theory",
        "content": "There are two main ways to execute stored procedures in modern Java:\n1. **Core JDBC API**: You use a `CallableStatement`.\n`CallableStatement stmt = connection.prepareCall(\"{call update_salary(?, ?)}\");`\n`stmt.setInt(1, empId);`\n`stmt.execute();`\n\n2. **Spring Data JPA**: You can map it directly in your Repository interface using the `@Procedure` annotation, making it completely declarative.\n`@Procedure(procedureName = \"update_salary\")`\n`void updateSalary(Integer empId, Double newSalary);`"
    },
    {
        "type": "question",
        "content": "What are HTTP Status codes? 4xx stands for what status?"
    },
    {
        "type": "theory",
        "content": "HTTP status codes indicate the result of a client's request to the server.\n- **2xx (Success)**: The request succeeded (e.g., 200 OK, 201 Created).\n- **3xx (Redirection)**: The resource has moved and the client must take additional action.\n- **4xx (Client Error)**: Indicates the client (the frontend) messed up. They sent bad data, an invalid token, or requested a non-existent page (e.g., 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found).\n- **5xx (Server Error)**: Indicates the server crashed or failed to process a perfectly valid request (e.g., 500 Internal Server Error)."
    },
    {
        "type": "question",
        "content": "What is the @NoArgsConstructor annotation?"
    },
    {
        "type": "theory",
        "content": "It is a **Lombok** annotation that automatically generates a default, empty constructor (with zero parameters) at compile time. \n\n**Why is it important?** This is strictly required by frameworks like JPA/Hibernate and Jackson JSON parsers. Hibernate requires a no-argument constructor to dynamically instantiate entity objects via reflection before using setters/reflection to populate them with the database row data."
    },
    {
        "type": "question",
        "content": "Which Java security frameworks have you implemented?"
    },
    {
        "type": "theory",
        "content": "In my projects, I exclusively implement **Spring Security**. \nI secure REST APIs by establishing stateless authentication using **JWT (JSON Web Tokens)**. I implement custom `OncePerRequestFilter` classes to intercept all incoming requests, cryptographically validate the JWT signature and expiration, and load the user's `GrantedAuthorities` into the `SecurityContextHolder`. \n\nFurthermore, I extensively configure method-level security using annotations like `@PreAuthorize(\"hasRole('ADMIN')\")` to strictly restrict access to specific sensitive endpoints."
    },
    {
        "type": "question",
        "content": "Write code to iterate over a JSON object and print an address."
    },
    {
        "type": "code",
        "lang": "java",
        "content": "import com.fasterxml.jackson.databind.JsonNode;\nimport com.fasterxml.jackson.databind.ObjectMapper;\nimport java.util.Iterator;\nimport java.util.Map;\n\npublic class JsonIteratorDemo {\n    public static void main(String[] args) throws Exception {\n        ObjectMapper mapper = new ObjectMapper();\n        String jsonString = \"{\\\"name\\\":\\\"John\\\", \\\"address\\\":{\\\"city\\\":\\\"New York\\\", \\\"zip\\\":\\\"10001\\\"}}\";\n\n        // 1. Parse JSON into a tree structure\n        JsonNode rootNode = mapper.readTree(jsonString);\n        \n        // 2. Extract the \"address\" object node\n        JsonNode addressNode = rootNode.get(\"address\");\n        \n        // 3. Iterate over the fields of the address object\n        Iterator<Map.Entry<String, JsonNode>> fields = addressNode.fields();\n        while (fields.hasNext()) {\n            Map.Entry<String, JsonNode> field = fields.next();\n            System.out.println(field.getKey() + \" : \" + field.getValue().asText());\n        }\n    }\n}"
    }
]

# Insert them under Spring Boot & Architecture
arch_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Architecture' in item.get('content', ''):
        arch_index = i
        break

if arch_index != -1:
    master_data[arch_index+1:arch_index+1] = missing_questions
else:
    master_data.append({"type": "category", "content": "Missing Spring Boot & REST Concepts"})
    master_data.extend(missing_questions)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
