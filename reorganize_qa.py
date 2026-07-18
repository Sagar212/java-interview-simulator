import json
import glob
import re

# Load all data
all_items = []
for file_path in glob.glob('data/part*.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        all_items.extend(json.load(f))

# Group items into logical Question Objects
# A question object will look like: { "question": "...", "content": [ {type: theory, content: ...}, {type: code...} ] }
questions = []
current_q = None

for item in all_items:
    if item['type'] == 'category':
        continue
    if item['type'] == 'question':
        if current_q:
            questions.append(current_q)
        current_q = {"question": item['content'], "blocks": []}
    else:
        if current_q:
            current_q['blocks'].append(item)
if current_q:
    questions.append(current_q)

# Define categories
categories = {
    "Core Java & OOPs": [
        "overriding", "overload", "constructor", "final", "wrapper", "string", "== and equals", 
        "abstract", "interface", "marker", "reflection", "hashcode"
    ],
    "Java 8 & Streams": [
        "lambda", "functional", "stream", "filter", "reduce", "optional", "java 8"
    ],
    "Collections Framework": [
        "arraylist", "linkedlist", "set", "map", "comparator", "fail", "collection framework"
    ],
    "Multithreading & Concurrency": [
        "thread", "lock", "atomic", "notify", "blockingqueue", "deadlock"
    ],
    "Spring Boot & Architecture": [
        "spring", "controller", "bean", "microservice", "saga", "circuit", "rest api", "jwt", "mfa"
    ],
    "Database & SQL": [
        "sql", "procedure", "jpa", "hibernate", "rank", "dense_rank", "nvl"
    ],
    "Coding & Algorithms": [
        "program to", "array unique", "repeating character", "prime", "stock prices", "json object"
    ],
    "HR & Behavioral": [
        "project", "experience", "resume", "5 years", "ctc"
    ]
}

def assign_category(q_text):
    text = q_text.lower()
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            return cat
    return "Miscellaneous"

# Filter out old vague questions
filtered_questions = []
for q in questions:
    text = q['question'].lower()
    if 'abstraction' in text or 'encapsulation' in text or 'qualifier' in text or 'diamond' in text:
        continue # We will manually inject the detailed versions
    filtered_questions.append(q)

# Inject new highly detailed questions
new_questions = [
    {
        "question": "What is Abstraction? Provide a detailed real-world example.",
        "blocks": [
            {
                "type": "theory", 
                "content": "**Abstraction** is the process of hiding internal implementation details and exposing only essential functionalities to the user. It reduces complexity and isolates changes. In Java, it is achieved using `abstract` classes (0 to 100% abstraction) and `interfaces` (100% abstraction).\n\n**Real-World Example (Car Dashboard)**:\nWhen you drive a car, you press the accelerator pedal. You only know that pressing the pedal increases speed (the abstract behavior). You do **not** need to know the complex internal mechanics of fuel injection, spark plug ignition, and combustion happening in the engine. The dashboard \"abstracts\" the engine's complexity away from the driver.\n\n**Java Example:**\n`public interface PaymentGateway { void processPayment(double amount); }`\nThe caller just calls `processPayment()`. They don't care if the underlying implementation is `StripePaymentImpl` or `PayPalPaymentImpl`."
            }
        ]
    },
    {
        "question": "What is Encapsulation? Provide a detailed real-world example.",
        "blocks": [
            {
                "type": "theory", 
                "content": "**Encapsulation** is the mechanism of wrapping the data (variables) and code acting on the data (methods) together as a single unit. It restricts direct access to some of an object's components, which prevents accidental modification of data. In Java, this is strictly achieved by declaring variables as `private` and providing `public` getter and setter methods to access and modify the data with validation.\n\n**Real-World Example (Bank ATM)**:\nA bank account balance is encapsulated. You cannot directly change your balance (e.g., `account.balance = 1000000`). You must use the ATM interface (the public method like `deposit()` or `withdraw()`). The ATM checks if you have sufficient funds and the correct PIN before it alters the internal balance.\n\n**Key Difference vs Abstraction**:\nAbstraction is about hiding **complexity** (What does it do?). Encapsulation is about hiding **data state** (How is the data protected?)."
            }
        ]
    },
    {
        "question": "What is the Diamond Problem (Multiple Inheritance) in Java? How is it resolved?",
        "blocks": [
            {
                "type": "theory", 
                "content": "The **Diamond Problem** occurs in multiple inheritance when a class inherits from two parent classes that both have a method with the exact same signature. The compiler becomes confused about which parent's method to execute.\n\nJava completely prevents this with classes by **not allowing multiple inheritance for classes** (a class can only `extend` one parent). \n\nHowever, in **Java 8**, interfaces can now have `default` methods. If a class implements two interfaces (`InterfaceA` and `InterfaceB`), and both have a default method named `show()`, the Diamond Problem reappears! \n\n**Resolution**: Java forces the implementing class to **override the conflicting method** and explicitly choose which parent's method to call using the `super` keyword, like this: `InterfaceA.super.show();`."
            }
        ]
    },
    {
        "question": "What happens if multiple beans of the same type exist in Spring Boot? How do you resolve ambiguity using @Qualifier?",
        "blocks": [
            {
                "type": "theory", 
                "content": "In Spring Boot, if you autowire an interface (e.g., `@Autowired PaymentService`), but there are two implementations (`StripePaymentService` and `PayPalPaymentService`) both annotated with `@Service`, Spring will crash at startup with a **NoUniqueBeanDefinitionException** because it doesn't know which one to inject.\n\n**How to resolve it:**\n1. **@Qualifier Annotation**: You attach `@Qualifier(\"stripePaymentService\")` alongside `@Autowired` to explicitly tell Spring the exact bean name to inject (by default, the bean name is the class name in camelCase).\n2. **@Primary Annotation**: You can annotate one of the implementation classes with `@Primary`. If Spring finds multiple beans, it will automatically inject the one marked as Primary unless a Qualifier overrides it."
            }
        ]
    }
]

filtered_questions.extend(new_questions)

# Categorize and Sort
categorized = {k: [] for k in categories.keys()}
categorized["Miscellaneous"] = []

for q in filtered_questions:
    cat = assign_category(q['question'])
    categorized[cat].append(q)

# Rebuild flat list for the UI
final_flat_list = []
for cat_name in categories.keys():
    if categorized[cat_name]:
        final_flat_list.append({"type": "category", "content": cat_name})
        for q in categorized[cat_name]:
            final_flat_list.append({"type": "question", "content": q['question']})
            final_flat_list.extend(q['blocks'])

if categorized["Miscellaneous"]:
    final_flat_list.append({"type": "category", "content": "Other Important Concepts"})
    for q in categorized["Miscellaneous"]:
        final_flat_list.append({"type": "question", "content": q['question']})
        final_flat_list.extend(q['blocks'])

# Write master JSON
with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(final_flat_list, f, indent=4)
