import os

target_file = "JAVA & SPRING INTERVIEW MASTER QUES.txt"
with open(target_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

injections = {
    "Q: What guarantees does volatile provide regarding visibility and ordering?": """
Java Template
public class VolatileExample {
    // Volatile guarantees visibility across threads
    private volatile boolean isRunning = true;

    public void stopRunning() {
        isRunning = false; // Write becomes immediately visible
    }

    public void runWork() {
        while (isRunning) {
            // Do some work continuously until stopRunning() is called
        }
        System.out.println("Work stopped!");
    }
}
End Template
""",
    "Q: Difference between static block and static method?": """
Java Template
public class StaticExample {
    // Static Block - runs once when class is loaded
    static {
        System.out.println("1. Class is loaded. Initializing static resources.");
    }

    // Static Method - runs only when called explicitly
    public static void printMessage() {
        System.out.println("2. Static method called.");
    }

    public static void main(String[] args) {
        StaticExample.printMessage();
    }
}
End Template
""",
    "Q: How do lambdas depend on functional interfaces?": """
Java Template
@FunctionalInterface
interface MathOperation {
    int operate(int a, int b);
}

public class LambdaDemo {
    public static void main(String[] args) {
        // Lambda provides the implementation for the single abstract method
        MathOperation addition = (a, b) -> a + b;
        MathOperation multiplication = (a, b) -> a * b;

        System.out.println("Add: " + addition.operate(10, 5));
        System.out.println("Multiply: " + multiplication.operate(10, 5));
    }
}
End Template
""",
    "Q: Difference between Runnable and Callable?": """
Java Template
import java.util.concurrent.*;

public class RunnableCallableDemo {
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(2);

        // Runnable: No return type, cannot throw checked exceptions
        Runnable myRunnable = () -> {
            System.out.println("Runnable task executing...");
        };

        // Callable: Returns a result (String here), can throw exceptions
        Callable<String> myCallable = () -> {
            Thread.sleep(1000);
            return "Callable task finished!";
        };

        executor.submit(myRunnable);
        Future<String> futureResult = executor.submit(myCallable);
        
        System.out.println("Waiting for Callable result: " + futureResult.get());
        executor.shutdown();
    }
}
End Template
""",
    "Q: Difference between == and equals?": """
Java Template
public class StringEqualityDemo {
    public static void main(String[] args) {
        String s1 = "Hello";              // String Pool
        String s2 = "Hello";              // String Pool (reused)
        String s3 = new String("Hello");  // Heap Memory

        // == compares memory references
        System.out.println("s1 == s2 : " + (s1 == s2)); // true (same pool object)
        System.out.println("s1 == s3 : " + (s1 == s3)); // false (different objects)

        // .equals() compares the actual character content
        System.out.println("s1.equals(s3) : " + s1.equals(s3)); // true (content is same)
    }
}
End Template
""",
    "Q: Ways to create threads in Java?": """
Java Template
public class ThreadCreationDemo {
    // Way 1: Extend Thread
    static class MyThread extends Thread {
        public void run() {
            System.out.println("Thread running via Thread class");
        }
    }

    // Way 2: Implement Runnable
    static class MyRunnable implements Runnable {
        public void run() {
            System.out.println("Thread running via Runnable interface");
        }
    }

    public static void main(String[] args) {
        MyThread t1 = new MyThread();
        t1.start();

        Thread t2 = new Thread(new MyRunnable());
        t2.start();
        
        // Way 3: Lambda (Runnable)
        Thread t3 = new Thread(() -> System.out.println("Thread running via Lambda"));
        t3.start();
    }
}
End Template
"""
}

new_lines = []
pending_injection = None

for line in lines:
    # If we are about to start a new section or question, inject pending code first
    if (line.startswith("Q: ") or line.startswith("======")) and pending_injection:
        new_lines.append(pending_injection + "\n")
        pending_injection = None
        
    new_lines.append(line)
    
    # If this line matches one of our target questions, queue the code block to be injected
    # at the end of its answer
    if line.strip() in injections:
        pending_injection = injections[line.strip()]

# If file ended and we still have a pending injection
if pending_injection:
    new_lines.append(pending_injection + "\n")

with open(target_file, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Injected code snippets successfully.")
