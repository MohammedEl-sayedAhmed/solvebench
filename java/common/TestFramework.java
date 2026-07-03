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
import java.util.Collection;
import java.util.Collections;
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

    /**
     * Strict, order-sensitive check (Objects.deepEquals). Use this by default —
     * whenever the exact sequence matters (a sorted array, a path, a string,
     * "return the answer in order", etc.).
     */
    public void check(String name, Object got, Object expected) {
        record(name, Objects.deepEquals(got, expected), got, expected, "expected:");
    }

    /**
     * Order-insensitive check: collections and arrays are compared as multisets,
     * recursively — so [[-1,0,1],[-1,-1,2]] equals [[-1,-1,2],[-1,0,1]], and the
     * order inside each triplet is ignored too. Use it only when the problem says
     * the result may be "in any order" (3Sum, subsets, group anagrams, ...).
     * Duplicates still count: it's a multiset, not a set. Maps compare by their
     * entry sets. Scalars stay type-strict (Integer 1 != "1" != 1L), matching
     * what check() would say.
     */
    public void checkUnordered(String name, Object got, Object expected) {
        record(name, unorderedEquals(got, expected), got, expected, "expected (any order):");
    }

    private void record(String name, boolean ok, Object got, Object expected, String expectedLabel) {
        total++;
        if (ok) {
            passed++;
            OUT.println(PASS + "  " + name);
        } else {
            failures.add(name);
            OUT.println(FAIL + "  " + name);
            OUT.println("      " + expectedLabel + " " + str(expected));
            OUT.println("      got:      " + str(got));
        }
    }

    // Deep, order-insensitive equality via canonical keys (see canonKey).
    private static boolean unorderedEquals(Object a, Object b) {
        return canonKey(a).equals(canonKey(b));
    }

    // A canonical, order-insensitive key. Collections/arrays -> the sorted
    // multiset of their elements' keys, so order never matters at any depth.
    // Maps -> the sorted multiset of "<key>value" entry pairs. Scalars -> type
    // tag + length-prefixed string form: the tag keeps 1, 1L, and "1" distinct
    // (as deepEquals would), and the length prefix makes the key grammar
    // unambiguous, so no string content can forge list/map syntax.
    private static String canonKey(Object o) {
        if (o == null) return "=null";
        if (o instanceof java.util.Map) {
            List<String> entries = new ArrayList<>();
            for (java.util.Map.Entry<?, ?> e : ((java.util.Map<?, ?>) o).entrySet())
                entries.add("<" + canonKey(e.getKey()) + ">" + canonKey(e.getValue()));
            Collections.sort(entries);
            return "{" + String.join(",", entries) + "}";
        }
        List<Object> items = elements(o);
        if (items == null) {
            String s = String.valueOf(o);
            return "=" + o.getClass().getName() + "|" + s.length() + ":" + s;
        }
        List<String> keys = new ArrayList<>(items.size());
        for (Object item : items) keys.add(canonKey(item));
        Collections.sort(keys);
        return "[" + String.join(",", keys) + "]";
    }

    // The elements of a Collection or any array (primitives boxed), else null.
    private static List<Object> elements(Object o) {
        if (o instanceof Collection) return new ArrayList<>((Collection<?>) o);
        if (o instanceof Object[]) return Arrays.asList((Object[]) o);
        if (o instanceof int[]) { List<Object> l = new ArrayList<>(); for (int x : (int[]) o) l.add(x); return l; }
        if (o instanceof long[]) { List<Object> l = new ArrayList<>(); for (long x : (long[]) o) l.add(x); return l; }
        if (o instanceof double[]) { List<Object> l = new ArrayList<>(); for (double x : (double[]) o) l.add(x); return l; }
        if (o instanceof float[]) { List<Object> l = new ArrayList<>(); for (float x : (float[]) o) l.add(x); return l; }
        if (o instanceof boolean[]) { List<Object> l = new ArrayList<>(); for (boolean x : (boolean[]) o) l.add(x); return l; }
        if (o instanceof char[]) { List<Object> l = new ArrayList<>(); for (char x : (char[]) o) l.add(x); return l; }
        if (o instanceof short[]) { List<Object> l = new ArrayList<>(); for (short x : (short[]) o) l.add(x); return l; }
        if (o instanceof byte[]) { List<Object> l = new ArrayList<>(); for (byte x : (byte[]) o) l.add(x); return l; }
        return null;
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
        if (o instanceof float[]) return Arrays.toString((float[]) o);
        if (o instanceof boolean[]) return Arrays.toString((boolean[]) o);
        if (o instanceof char[]) return Arrays.toString((char[]) o);
        if (o instanceof short[]) return Arrays.toString((short[]) o);
        if (o instanceof byte[]) return Arrays.toString((byte[]) o);
        if (o instanceof Object[]) return Arrays.deepToString((Object[]) o);
        return String.valueOf(o);
    }
}
