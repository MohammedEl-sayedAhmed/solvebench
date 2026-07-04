// Singly-linked list node — the repo's counterpart of the ListNode that
// LeetCode "provides" for you. Linked-list solutions `import common.ListNode;`
// and solve against it exactly as on the site (head.val, head.next, ...).
//
// Fields are public (LeetCode's are package-private) because solutions live in
// a different package here — package-private fields wouldn't be reachable. The
// body of your method is identical to what you'd paste on LeetCode either way.
package common;

public class ListNode {
    public int val;
    public ListNode next;

    public ListNode() {}
    public ListNode(int val) { this.val = val; }
    public ListNode(int val, ListNode next) { this.val = val; this.next = next; }

    /** Build a straight (acyclic) list from values; returns the head (or null). */
    public static ListNode of(int... vals) {
        ListNode dummy = new ListNode();
        ListNode tail = dummy;
        for (int v : vals) { tail.next = new ListNode(v); tail = tail.next; }
        return dummy.next;
    }
}
