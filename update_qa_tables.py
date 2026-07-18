import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

# 1. Update Hibernate vs JPA to use a table
for item in master_data:
    if item.get('type') == 'question' and 'Hibernate and JPA' in item.get('content', ''):
        # We need to find the blocks associated with this question. 
        # Wait, the structure in master.json is flat.
        pass

# Since master.json is a flat list, let's iterate and replace
for i in range(len(master_data)):
    if master_data[i].get('type') == 'question' and 'Hibernate and JPA' in master_data[i].get('content', ''):
        # The next item should be the theory block
        if master_data[i+1].get('type') == 'theory':
            master_data[i+1]['content'] = """<table>
    <tr><th>Feature</th><th>JPA (Java Persistence API)</th><th>Hibernate</th></tr>
    <tr><td><strong>Definition</strong></td><td>A specification/standard that defines rules for ORM.</td><td>A concrete implementation of the JPA specification.</td></tr>
    <tr><td><strong>Nature</strong></td><td>Contains only interfaces and annotations (no code).</td><td>Contains actual Java classes that execute the database logic.</td></tr>
    <tr><td><strong>Dependency</strong></td><td>Cannot be used alone without an implementation provider.</td><td>Can be used standalone, but using it via JPA interfaces is standard practice.</td></tr>
    <tr><td><strong>Query Language</strong></td><td>JPQL (Java Persistence Query Language).</td><td>HQL (Hibernate Query Language).</td></tr>
</table>
<br>
<strong>Notes / Advantages of Hibernate:</strong>
<ul>
    <li><strong>Database Independence:</strong> By simply changing the Dialect in properties, Hibernate translates queries for MySQL, Oracle, or Postgres without rewriting Java code.</li>
    <li><strong>Caching:</strong> Provides powerful First-Level (Session) and Second-Level (SessionFactory) caches to drastically reduce database hits.</li>
    <li><strong>Lazy Loading:</strong> Delays fetching child entities until explicitly requested, saving massive amounts of memory.</li>
</ul>"""
            break

# 2. Prepare new questions
new_java8_questions = [
    {
        "type": "question",
        "content": "How do you create a custom Functional Interface and use it with a Lambda expression?"
    },
    {
        "type": "theory",
        "content": "A Functional Interface must contain exactly **one abstract method**. You strongly enforce this using the `@FunctionalInterface` annotation so the compiler throws an error if someone adds a second method.\n\nLambdas allow us to provide the implementation for this single abstract method inline, completely eliminating the need for bulky anonymous inner classes."
    },
    {
        "type": "code",
        "lang": "java",
        "content": "// 1. Define the Custom Interface\n@FunctionalInterface\npublic interface MathOperation {\n    int operate(int a, int b);\n}\n\npublic class LambdaDemo {\n    public static void main(String[] args) {\n        // 2. Implement it instantly using a Lambda Expression\n        MathOperation addition = (a, b) -> a + b;\n        MathOperation multiplication = (a, b) -> a * b;\n\n        // 3. Execute the implementation\n        System.out.println(\"Sum: \" + addition.operate(10, 5)); // Output: 15\n        System.out.println(\"Product: \" + multiplication.operate(10, 5)); // Output: 50\n    }\n}"
    },
    {
        "type": "question",
        "content": "Provide concrete examples of Intermediate vs Terminal operations in Streams."
    },
    {
        "type": "theory",
        "content": "**Intermediate Operations** transform the stream into another stream. They are **lazy**, meaning they absolutely do not execute until a terminal operation is called. \nExamples: `filter()`, `map()`, `sorted()`, `distinct()`.\n\n**Terminal Operations** trigger the execution of the entire pipeline and produce a final non-stream result (like a Collection, integer, or void).\nExamples: `collect()`, `forEach()`, `reduce()`, `count()`."
    },
    {
        "type": "code",
        "lang": "java",
        "content": "List<String> names = Arrays.asList(\"Alice\", \"Bob\", \"Charlie\", \"David\", \"Alice\");\n\n// Pipeline Execution\nlong count = names.stream()\n    .filter(name -> name.length() > 3)  // Intermediate: Keeps [Alice, Charlie, David, Alice]\n    .distinct()                         // Intermediate: Keeps [Alice, Charlie, David]\n    .map(String::toUpperCase)           // Intermediate: Transforms to [ALICE, CHARLIE, DAVID]\n    .count();                           // Terminal: Triggers execution! Returns 3"
    }
]

# Find the "Java 8 & Streams" category index
j8_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Java 8' in item.get('content', ''):
        j8_index = i
        break

if j8_index != -1:
    # insert after the category header
    master_data[j8_index+1:j8_index+1] = new_java8_questions
else:
    master_data.append({"type": "category", "content": "Java 8 Additions"})
    master_data.extend(new_java8_questions)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
