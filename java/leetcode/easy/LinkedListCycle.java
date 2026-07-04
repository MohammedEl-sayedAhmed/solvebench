// 141. Linked List Cycle
// https://leetcode.com/problems/linked-list-cycle/
//
// Given head, the head of a linked list, determine if the linked list has a
// cycle in it.
//
// There is a cycle in a linked list if there is some node in the list that can
// be reached again by continuously following the next pointer. Internally, pos
// denotes the index of the node that the tail's next pointer connects to. Note
// that pos is NOT passed to your function; it only describes the test input.
//
// Return true if there is a cycle in the linked list, otherwise false.
//
// Example 1:
//   Input:  head = [3,2,0,-4], pos = 1   (tail's next connects to index 1)
//   Output: true
// Example 2:
//   Input:  head = [1,2], pos = 0
//   Output: true
// Example 3:
//   Input:  head = [1], pos = -1         (no cycle)
//   Output: false
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
package leetcode.easy;

import common.ListNode;
import common.TestFramework;

/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */

public class LinkedListCycle {

    // Floyd's tortoise & hare. slow advances one node, fast two, so fast gains
    // exactly one node per step: in a cycle the gap keeps shrinking until they
    // land on the same node; with no cycle, fast reaches the end first. Guarding
    // fast up front (it's always ahead) covers both pointers — one check, no
    // mid-loop break, and the empty list falls straight through to false.
    // Time O(n), Space O(1).
    public boolean hasCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;         // one node
            fast = fast.next.next;    // two nodes
            if (slow == fast) {
                return true;          // same node object -> cycle
            }
        }
        return false;                 // fast hit the end -> no cycle
    }

    // Test helper — build a list from values and, if pos >= 0, connect the
    // tail's next to node[pos] to form a cycle. pos is only for constructing
    // the input; your solution never receives it.
    private static ListNode build(int[] vals, int pos) {
        if (vals.length == 0) return null;
        ListNode[] nodes = new ListNode[vals.length];
        for (int i = 0; i < vals.length; i++) nodes[i] = new ListNode(vals[i]);
        for (int i = 0; i + 1 < vals.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0) nodes[vals.length - 1].next = nodes[pos];
        return nodes[0];
    }

    public static void main(String[] args) {
        LinkedListCycle s = new LinkedListCycle();
        TestFramework t = new TestFramework();

        t.check("Example 1", s.hasCycle(build(new int[]{3, 2, 0, -4}, 1)), true);
        t.check("Example 2", s.hasCycle(build(new int[]{1, 2}, 0)), true);
        t.check("Example 3", s.hasCycle(build(new int[]{1}, -1)), false);
        t.check("Empty list", s.hasCycle(build(new int[]{}, -1)), false);
        t.check("Long, no cycle", s.hasCycle(build(new int[]{
                -21, 10, 17, 8, 4, 26, 5, 35, 33, -7, -16, 27, -12, 6, 29, -12,
                5, 9, 20, 14, 14, 2, 13, -24, 21, 23, -21, 5}, -1)), false);

        System.exit(t.summary());
    }
}
