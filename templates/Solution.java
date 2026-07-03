// <Problem Title>
// <url>
//
// <problem statement — paste here>
//
// NOTE: the `package` line and the class name are set by the scaffolder
// (new.py) so they match the file's location and name.
package PACKAGE_NAME;

import common.TestFramework;

public class Solution {
    // Explain the approach. Time O(?), Space O(?).
    // int solve(...) { }

    // Optional: custom input scaling for `./run.sh complexity <problem>` — only
    // needed when the input can't be derived from the parameter types.
    // public static Object[] complexityInput(int n) {
    //     return new Object[] { /* args for size n */ };
    // }

    public static void main(String[] args) {
        Solution s = new Solution();
        TestFramework t = new TestFramework();

        // t.check("Example 1", s.solve(/* args */), /* expected */);

        System.exit(t.summary());
    }
}
