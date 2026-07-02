// Minimal test helper — the Java counterpart of
// python/common/test_framework.py. Lives in the `common` package; solutions
// `import common.TestFramework;`. run.py (and VS Code) compile it alongside
// each solution automatically.
//
//   package leetcode.easy;
//   import common.TestFramework;
//
//   public class TwoSum {
//       public static void main(String[] args) {
//           TestFramework t = new TestFramework();
//           t.check("Example 1", solve(args), expected);
//           System.exit(t.summary());   // non-zero exit if any check failed
//       }
//   }
package common;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class TestFramework {
    private int passed = 0;
    private int total = 0;
    private final List<String> failures = new ArrayList<>();

    public void check(String name, Object got, Object expected) {
        total++;
        if (Objects.deepEquals(got, expected)) {
            passed++;
            System.out.println("✅ " + name + " passed");
        } else {
            failures.add(name);
            System.out.println("❌ " + name + " failed");
            System.out.println("   Expected: " + str(expected));
            System.out.println("   Got: " + str(got));
        }
    }

    /** Returns a process exit code: 0 when everything passed, 1 otherwise. */
    public int summary() {
        System.out.println("\nTest Results: " + passed + "/" + total + " passed");
        if (failures.isEmpty()) {
            System.out.println("All tests passed! 🎉");
            return 0;
        }
        System.out.println(failures.size() + " test(s) failed");
        return 1;
    }

    private static String str(Object o) {
        if (o instanceof int[]) return Arrays.toString((int[]) o);
        if (o instanceof long[]) return Arrays.toString((long[]) o);
        if (o instanceof double[]) return Arrays.toString((double[]) o);
        if (o instanceof boolean[]) return Arrays.toString((boolean[]) o);
        if (o instanceof char[]) return Arrays.toString((char[]) o);
        if (o instanceof Object[]) return Arrays.deepToString((Object[]) o);
        return String.valueOf(o);
    }
}
