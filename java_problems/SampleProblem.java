import java.util.*;
import java.util.stream.*;

public class SampleProblem {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");
        
        // Find names starting with C or D
        List<String> filtered = names.stream()
                                     .filter(n -> n.startsWith("C") || n.startsWith("D"))
                                     .collect(Collectors.toList());
                                     
        System.out.println("Filtered names: " + filtered);
    }
}
