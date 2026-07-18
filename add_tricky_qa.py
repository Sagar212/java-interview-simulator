import json

with open('data/master.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

new_questions = [
    {
        "type": "question",
        "content": "Is Java Pass-by-Reference? Prove why Java is strictly Pass-by-Value."
    },
    {
        "type": "theory",
        "content": "Java is **strictly Pass-by-Value**. It never passes the actual object itself; it passes a *copy of the memory reference* that points to the object. \n\nIf you modify the object's internal fields using that copied reference, the original object changes (which tricks people into thinking it's pass-by-reference). However, if you try to reassign the reference variable entirely to a brand new object using the `new` keyword, the original object in the calling method remains completely untouched. If Java were actually Pass-by-Reference, the original object would have been swapped."
    },
    {
        "type": "code",
        "lang": "java",
        "content": "public class PassByValueDemo {\n    public static void main(String[] args) {\n        Dog myDog = new Dog(\"Max\");\n        modifyDog(myDog);\n        \n        // Output is \"Charlie\", NOT \"Rex\"!\n        System.out.println(myDog.name); \n    }\n\n    public static void modifyDog(Dog dogParam) {\n        // 1. This works because the copied reference points to the same original object in memory.\n        dogParam.name = \"Charlie\"; \n        \n        // 2. TRICKY PART: We reassign the reference to a brand new object.\n        // If Java was Pass-By-Reference, 'myDog' in main would now point to this new \"Rex\" dog.\n        // But because it is Pass-By-Value, this only overwrites the local 'dogParam' copy.\n        dogParam = new Dog(\"Rex\"); \n    }\n}"
    },
    {
        "type": "question",
        "content": "Tricky Scenarios: Interface vs Abstract Class in modern Java (8+)"
    },
    {
        "type": "theory",
        "content": "Since Java 8 introduced `default` and `static` methods in interfaces with concrete bodies, the line between them has blurred. Interviewers will test your knowledge on the strict limitations that remain:\n\n<table>\n    <tr><th>Feature</th><th>Interface</th><th>Abstract Class</th></tr>\n    <tr><td><strong>Constructors</strong></td><td><strong>CANNOT</strong> have constructors. An interface cannot be instantiated, nor does it have state to initialize.</td><td><strong>CAN</strong> have constructors. They are called when a concrete child class is created to initialize shared state.</td></tr>\n    <tr><td><strong>Variables (State)</strong></td><td>All variables are strictly <code>public static final</code> (constants). You cannot declare mutable instance variables.</td><td>Can have standard, mutable instance variables (protected, private) to maintain state across methods.</td></tr>\n    <tr><td><strong>Multiple Inheritance</strong></td><td>A class can <code>implement</code> multiple interfaces.</td><td>A class can only <code>extend</code> a single abstract class.</td></tr>\n    <tr><td><strong>Access Modifiers</strong></td><td>Methods are implicitly <code>public abstract</code>. (Java 9 added <code>private</code> methods for sharing internal logic).</td><td>Methods can be <code>protected</code>, <code>private</code>, or <code>public</code>.</td></tr>\n</table>"
    }
]

# Insert them into the Core Java category
core_index = -1
for i, item in enumerate(master_data):
    if item.get('type') == 'category' and 'Core Java' in item.get('content', ''):
        core_index = i
        break

if core_index != -1:
    master_data[core_index+1:core_index+1] = new_questions
else:
    master_data.append({"type": "category", "content": "Advanced Java Quirks"})
    master_data.extend(new_questions)

with open('data/master.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=4)
