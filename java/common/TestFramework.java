// Minimal test helper — the Java counterpart of
// python/common/test_framework.py. Lives in the `common` package; solutions
// `import common.TestFramework;`. run.py, the VS Code Run button, and CI all
// compile it alongside each solution automatically.
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

import java.io.FileDescriptor;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class TestFramework {
    // Write straight to stdout as UTF-8 so the emoji render even when the JVM's
    // default charset is ASCII (e.g. a container with a C/POSIX locale);
    // otherwise they print as "?". (Source is UTF-8: run.py compiles with
    // -encoding UTF-8, and the VS Code Java extension defaults to UTF-8.)
    private static final PrintStream OUT =
            new PrintStream(new FileOutputStream(FileDescriptor.out), true, StandardCharsets.UTF_8);

    private static final String PASS = "✅";           // check mark
    private static final String FAIL = "❌";           // cross mark
    private static final String PARTY = "🎉";    // party popper
    private static final String RULE = "─";           // box-drawing horizontal
    private static final String DASH = "—";           // em dash
    private static final String DOT = "·";            // middle dot

    private int passed = 0;
    private int total = 0;
    private final List<String> failures = new ArrayList<>();

    public void check(String name, Object got, Object expected) {
        total++;
        if (Objects.deepEquals(got, expected)) {
            passed++;
            OUT.println(PASS + "  " + name);
        } else {
            failures.add(name);
            OUT.println(FAIL + "  " + name);
            OUT.println("      expected: " + str(expected));
            OUT.println("      got:      " + str(got));
        }
    }

    /** Returns a process exit code: 0 when everything passed, 1 otherwise. */
    public int summary() {
        OUT.println("\n" + RULE.repeat(34));
        if (failures.isEmpty()) {
            OUT.println(PARTY + "  " + passed + "/" + total + " passed " + DASH + " all green");
            return 0;
        }
        OUT.println(FAIL + "  " + passed + "/" + total + " passed " + DOT + " " + failures.size() + " failed");
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
