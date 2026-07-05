// 876. Middle of the Linked List
// https://leetcode.com/problems/middle-of-the-linked-list/
//
// Given the head of a singly linked list, return the middle node of the linked
// list.
//
// If there are two middle nodes, return the second middle node.
//
// Example 1:
//   Input:  head = [1,2,3,4,5]
//   Output: [3,4,5]     (the middle node has value 3)
// Example 2:
//   Input:  head = [1,2,3,4,5,6]
//   Output: [4,5,6]     (two middles; return the second, value 4)
//
// Constraints:
//   The number of nodes in the list is in the range [1, 100].
//   1 <= Node.val <= 100
//
// NOTE: the `package` line and the class name are set by the scaffolder
// (new.py) so they match the file's location and name.
package leetcode.easy;

import common.ListNode;
import common.TestFramework;

public class MiddleOfTheLinkedList {

    // Two pointers (tortoise & hare): fast advances two nodes for every one that
    // slow advances, so when fast runs off the end, slow sits at the middle. On
    // an even-length list fast takes a final full double-step, nudging slow onto
    // the SECOND of the two middles — exactly what's asked, with no special case.
    // Time O(n), Space O(1).
    public ListNode middleNode(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;         // +1 node
            fast = fast.next.next;    // +2 nodes
        }
        return slow;                  // fast reached the end -> slow is the middle
    }

    // Test helper — the values from `node` to the end. The judge accepts the
    // node you return plus everything after it, so we compare that whole tail.
    private static int[] tail(ListNode node) {
        int len = 0;
        for (ListNode n = node; n != null; n = n.next) len++;
        int[] out = new int[len];
        int i = 0;
        for (ListNode n = node; n != null; n = n.next) out[i++] = n.val;
        return out;
    }

    public static void main(String[] args) {
        MiddleOfTheLinkedList s = new MiddleOfTheLinkedList();
        TestFramework t = new TestFramework();

        // The two LeetCode examples.
        t.check("Example 1: odd [1..5]", tail(s.middleNode(ListNode.of(1, 2, 3, 4, 5))), new int[]{3, 4, 5});
        t.check("Example 2: even [1..6] -> 2nd middle", tail(s.middleNode(ListNode.of(1, 2, 3, 4, 5, 6))), new int[]{4, 5, 6});

        // Boundary lengths.
        t.check("single node", tail(s.middleNode(ListNode.of(1))), new int[]{1});
        t.check("two nodes -> 2nd middle", tail(s.middleNode(ListNode.of(1, 2))), new int[]{2});
        t.check("three nodes (odd)", tail(s.middleNode(ListNode.of(1, 2, 3))), new int[]{2, 3});
        t.check("four nodes (even) -> 2nd middle", tail(s.middleNode(ListNode.of(1, 2, 3, 4))), new int[]{3, 4});

        // Longer odd / even.
        t.check("seven nodes (odd)", tail(s.middleNode(ListNode.of(1, 2, 3, 4, 5, 6, 7))), new int[]{4, 5, 6, 7});
        t.check("eight nodes (even) -> 2nd middle", tail(s.middleNode(ListNode.of(1, 2, 3, 4, 5, 6, 7, 8))), new int[]{5, 6, 7, 8});

        // Middle is chosen by POSITION, not value: an all-equal list still
        // returns the second-middle index (a 2-element tail here, not 1).
        t.check("all duplicates [1,1,1,1]", tail(s.middleNode(ListNode.of(1, 1, 1, 1))), new int[]{1, 1});

        // Constraint value boundaries (1 and 100).
        t.check("min/max values", tail(s.middleNode(ListNode.of(100, 1, 100))), new int[]{1, 100});

        // Max length n = 100 (even) -> second middle at index 50 (value 51).
        int[] big = new int[100];
        for (int i = 0; i < big.length; i++) big[i] = i + 1;
        int[] expectBig = new int[50];
        for (int i = 0; i < expectBig.length; i++) expectBig[i] = 51 + i;
        t.check("max length n=100 (even)", tail(s.middleNode(ListNode.of(big))), expectBig);

        System.exit(t.summary());
    }
}
