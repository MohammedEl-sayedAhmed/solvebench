// 142. Linked List Cycle II
// https://leetcode.com/problems/linked-list-cycle-ii/
//
// Given the head of a linked list, return the node where the cycle begins. If
// there is no cycle, return null.
//
// There is a cycle in a linked list if there is some node in the list that can
// be reached again by continuously following the next pointer. Internally, pos
// denotes the index of the node that the tail's next pointer connects to (-1 if
// there is no cycle). pos is NOT passed to your function.
//
// Do not modify the linked list.
//
// Example 1:
//   Input:  head = [3,2,0,-4], pos = 1
//   Output: node at index 1 (value 2)   — the cycle starts at the second node
// Example 2:
//   Input:  head = [1,2], pos = 0
//   Output: node at index 0 (value 1)
// Example 3:
//   Input:  head = [1], pos = -1
//   Output: null                         — no cycle
//
// Constraints:
//   The number of the nodes in the list is in the range [0, 10^4].
//   -10^5 <= Node.val <= 10^5
//   pos is -1 or a valid index in the linked list.
//
// Follow-up: can you solve it using O(1) (constant) memory?
//
// NOTE: the `package` line and the class name are set by the scaffolder
// (new.py) so they match the file's location and name.
package leetcode.medium;

import common.ListNode;
import common.TestFramework;

public class LinkedListCycleII {

    // Floyd's cycle detection in two phases.
    //   Phase 1 (find a meeting point): fast moves two nodes per step, slow one,
    //     so if a cycle exists they must eventually collide inside it. If fast
    //     falls off the end (null), there is no cycle.
    //   Phase 2 (find the entry): reset one pointer to head, advance both one
    //     step at a time; they meet exactly at the node where the cycle begins.
    //
    // Why phase 2 works (the distance argument). Let
    //     a = distance from head to the cycle entry,
    //     L = cycle length,
    //     b = distance from the entry to the meeting point (going forward).
    // When the pointers meet, slow has walked a + b and fast has walked
    // 2*(a + b). Fast sits on the same node but has gone some whole number of
    // extra loops, so:
    //     2*(a + b) = (a + b) + k*L   =>   a + b = k*L   =>   a = k*L - b.
    // Rewrite as  a = (k-1)*L + (L - b).  Since (L - b) is the distance from the
    // meeting point forward to the entry, a pointer from head (needs a steps to
    // reach the entry) and a pointer from the meeting point (needs (L - b) steps,
    // plus (k-1) full loops) both land on the entry after exactly a steps -- so
    // they meet there. That's why phase 2 walks in lockstep from head + meeting.
    //
    // Visual walkthrough: https://www.youtube.com/shorts/qgXYgkeEXg8
    // Time O(n), Space O(1). The list is never modified.
    public ListNode detectCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;

        // Phase 1: advance until the pointers meet (cycle) or fast reaches the end.
        while (fast != null && fast.next != null) {
            slow = slow.next;         // +1 node
            fast = fast.next.next;    // +2 nodes
            if (slow == fast) {
                break;                // met inside the cycle
            }
        }

        // If we exited without meeting, fast hit the end -> no cycle. (After a
        // real meeting, both fast and fast.next are non-null cycle nodes.)
        if (fast == null || fast.next == null) {
            return null;
        }

        // Phase 2: one pointer from head, one from the meeting point, one step
        // each -> they converge on the node where the cycle begins.
        ListNode p1 = head;
        while (p1 != slow) {
            p1 = p1.next;
            slow = slow.next;
        }
        return p1;
    }

    // Build a list from values; if pos >= 0, connect the tail's next to
    // node[pos] to form a cycle. Returns the whole node array so a test can name
    // both the head (nodes[0]) and the true cycle-entry node (nodes[pos]). pos
    // is only for building the input; detectCycle never receives it.
    private static ListNode[] build(int[] vals, int pos) {
        ListNode[] nodes = new ListNode[vals.length];
        for (int i = 0; i < vals.length; i++) nodes[i] = new ListNode(vals[i]);
        for (int i = 0; i + 1 < vals.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0 && vals.length > 0) nodes[vals.length - 1].next = nodes[pos];
        return nodes;
    }

    // Whether detectCycle returns the EXACT node where the cycle starts
    // (identity, not value): node[pos], or null when pos < 0.
    private static boolean findsStart(LinkedListCycleII s, int[] vals, int pos) {
        ListNode[] nodes = build(vals, pos);
        ListNode head = nodes.length == 0 ? null : nodes[0];
        ListNode expected = pos >= 0 ? nodes[pos] : null;
        return s.detectCycle(head) == expected;
    }

    public static void main(String[] args) {
        LinkedListCycleII s = new LinkedListCycleII();
        TestFramework t = new TestFramework();

        // The three LeetCode examples.
        t.check("Example 1: [3,2,0,-4] pos=1 (entry val 2)", findsStart(s, new int[]{3, 2, 0, -4}, 1), true);
        t.check("Example 2: [1,2] pos=0 (entry val 1)", findsStart(s, new int[]{1, 2}, 0), true);
        t.check("Example 3: [1] pos=-1 (no cycle)", findsStart(s, new int[]{1}, -1), true);

        // No-cycle cases (must return null).
        t.check("empty list", findsStart(s, new int[]{}, -1), true);
        t.check("no cycle, four nodes", findsStart(s, new int[]{1, 2, 3, 4}, -1), true);

        // Cycle-shape edge cases.
        t.check("self-loop [1] pos=0", findsStart(s, new int[]{1}, 0), true);
        t.check("cycle back to head [1,2,3] pos=0", findsStart(s, new int[]{1, 2, 3}, 0), true);
        t.check("cycle at tail [1,2,3] pos=2", findsStart(s, new int[]{1, 2, 3}, 2), true);
        t.check("longer cycle [1..6] pos=3", findsStart(s, new int[]{1, 2, 3, 4, 5, 6}, 3), true);

        // Duplicate values: the entry must be the exact node[pos], not just any
        // node that happens to share its value (all three are 7 here).
        t.check("duplicates, entry by identity [7,7,7] pos=1", findsStart(s, new int[]{7, 7, 7}, 1), true);

        System.exit(t.summary());
    }
}
