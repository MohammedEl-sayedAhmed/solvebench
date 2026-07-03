// Reflection-based measurement harness for the complexity estimator.
// Driven by complexity.py (never run by hand):
//
//   java -cp .pst/build/java common.ComplexityHarness list <fqcn>
//       -> METHOD <name> <paramType,paramType,...>        (one per public method)
//
//   java -cp .pst/build/java common.ComplexityHarness measure \
//       <fqcn> <method> <sizesCsv> <repeat> <maxSeconds>
//       -> INPUTS <description>
//          DATA <n> <bestTimeNanos> <allocBytes|-1>        (one per size)
//          STOP <n>                                        (if the cap kicked in)
//
// Inputs are generated from the method's parameter types (worst-case-ish,
// mirroring the Python generators: int[] -> 0..n-1 so search problems can't
// early-exit on a lucky pair; String -> a palindrome so symmetric scans run
// fully). A solution class may define `static Object[] complexityInput(int n)`
// to override generation entirely.
package common;

import java.lang.management.ManagementFactory;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;

public final class ComplexityHarness {

    public static void main(String[] args) throws Exception {
        if (args.length >= 2 && args[0].equals("list")) {
            list(Class.forName(args[1]));
        } else if (args.length >= 6 && args[0].equals("measure")) {
            measure(Class.forName(args[1]), args[2], args[3],
                    Integer.parseInt(args[4]), Double.parseDouble(args[5]));
        } else {
            System.err.println("usage: list <fqcn> | measure <fqcn> <method> <sizesCsv> <repeat> <maxSeconds>");
            System.exit(2);
        }
    }

    // ---- list mode ---------------------------------------------------------
    private static void list(Class<?> cls) {
        for (Method m : cls.getDeclaredMethods()) {
            if (!Modifier.isPublic(m.getModifiers()) || m.getName().equals("main")
                    || m.getName().equals("complexityInput")) {
                continue;
            }
            StringBuilder types = new StringBuilder();
            for (Class<?> p : m.getParameterTypes()) {
                if (types.length() > 0) types.append(",");
                types.append(p.getSimpleName());
            }
            System.out.println("METHOD " + m.getName() + " " + types);
        }
    }

    // ---- measure mode ------------------------------------------------------
    private static void measure(Class<?> cls, String methodName, String sizesCsv,
                                int repeat, double maxSeconds) throws Exception {
        Method target = null;
        for (Method m : cls.getDeclaredMethods()) {
            if (m.getName().equals(methodName)) target = m;
        }
        if (target == null) {
            System.err.println("ERROR method not found: " + methodName);
            System.exit(1);
            return;
        }
        target.setAccessible(true);
        Object instance = Modifier.isStatic(target.getModifiers())
                ? null : cls.getDeclaredConstructor().newInstance();

        Method custom = null;
        try {
            custom = cls.getDeclaredMethod("complexityInput", int.class);
        } catch (NoSuchMethodException ignored) { /* no override — generate */ }

        Class<?>[] params = target.getParameterTypes();
        if (custom == null) {
            StringBuilder desc = new StringBuilder();
            for (Class<?> p : params) {
                if (desc.length() > 0) desc.append(", ");
                desc.append(p.getSimpleName());
                if (generate(p, 4) == null) {
                    System.err.println("ERROR cannot generate parameter type: " + p.getSimpleName());
                    System.exit(3);
                }
            }
            System.out.println("INPUTS generated from parameter types (" + desc + ")");
        } else {
            custom.setAccessible(true);
            System.out.println("INPUTS complexityInput(n) from the solution class");
        }

        String[] sizeStrs = sizesCsv.split(",");
        long[] sizes = new long[sizeStrs.length];
        for (int i = 0; i < sizeStrs.length; i++) sizes[i] = Long.parseLong(sizeStrs[i].trim());

        // JIT warm-up on the smallest size so compiled-vs-interpreted noise
        // doesn't masquerade as growth.
        for (int w = 0; w < 5; w++) invoke(target, instance, buildArgs(custom, params, (int) sizes[0]));

        for (int i = 0; i < sizes.length; i++) {
            int n = (int) sizes[i];
            long best = Long.MAX_VALUE;
            for (int r = 0; r < repeat; r++) {
                Object[] callArgs = buildArgs(custom, params, n);  // fresh (mutation-safe)
                long t0 = System.nanoTime();
                invoke(target, instance, callArgs);
                best = Math.min(best, System.nanoTime() - t0);
            }
            long alloc = measureAlloc(target, instance, buildArgs(custom, params, n));
            System.out.println("DATA " + n + " " + best + " " + alloc);

            double secs = best / 1e9;
            Long nxt = i + 1 < sizes.length ? sizes[i + 1] : null;
            if (secs > maxSeconds || (nxt != null && secs * ((double) nxt / n) > maxSeconds)) {
                System.out.println("STOP " + n);
                break;
            }
        }
    }

    private static Object[] buildArgs(Method custom, Class<?>[] params, int n) throws Exception {
        if (custom != null) return (Object[]) custom.invoke(null, n);
        Object[] out = new Object[params.length];
        for (int i = 0; i < params.length; i++) out[i] = generate(params[i], n);
        return out;
    }

    private static void invoke(Method m, Object instance, Object[] args) throws Exception {
        try {
            m.invoke(instance, args);
        } catch (java.lang.reflect.InvocationTargetException e) {
            Throwable c = e.getCause();
            System.err.println("ERROR the method raised on a generated input ("
                    + c.getClass().getSimpleName() + ": " + c.getMessage() + ")");
            System.exit(4);
        }
    }

    /** Allocated bytes on this thread during one call, or -1 if unsupported. */
    private static long measureAlloc(Method m, Object instance, Object[] args) throws Exception {
        try {
            com.sun.management.ThreadMXBean mx =
                    (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
            long tid = Thread.currentThread().getId();
            long before = mx.getThreadAllocatedBytes(tid);
            invoke(m, instance, args);
            return Math.max(0, mx.getThreadAllocatedBytes(tid) - before);
        } catch (Throwable t) {
            return -1;
        }
    }

    // ---- input generators (mirror complexity.py's Python defaults) ---------
    private static Object generate(Class<?> p, int n) {
        if (p == int.class || p == Integer.class) return n;
        if (p == long.class || p == Long.class) return (long) n;
        if (p == double.class || p == Double.class) return (double) n;
        if (p == boolean.class || p == Boolean.class) return true;
        if (p == String.class) return palindrome(n);
        if (p == int[].class) {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = i;
            return a;
        }
        if (p == long[].class) {
            long[] a = new long[n];
            for (int i = 0; i < n; i++) a[i] = i;
            return a;
        }
        if (p == char[].class) return palindrome(n).toCharArray();
        if (p == String[].class) {
            String[] a = new String[n];
            String base = "abcdefgh";
            for (int i = 0; i < n; i++) a[i] = base;   // shared prefix: worst case for prefix scans
            return a;
        }
        if (p == int[][].class) {
            int[][] a = new int[n][8];
            for (int i = 0; i < n; i++) for (int j = 0; j < 8; j++) a[i][j] = (i + j) % 100;
            return a;
        }
        if (List.class.isAssignableFrom(p)) {
            List<Integer> xs = new ArrayList<>(n);
            for (int i = 0; i < n; i++) xs.add(i);
            return xs;
        }
        return null;
    }

    /** Non-uniform palindrome — worst case for symmetric scans. */
    private static String palindrome(int n) {
        StringBuilder half = new StringBuilder();
        for (int i = 0; i < n / 2; i++) half.append((char) ('a' + i % 26));
        String h = half.toString();
        return h + (n % 2 == 1 ? "z" : "") + half.reverse();
    }

    private ComplexityHarness() {}
}
