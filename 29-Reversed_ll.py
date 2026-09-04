# Question Link => https://leetcode.com/problems/reverse-linked-list-ii/
# NOTE: this file was empty in the original repo -- the problem was never solved.

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        # A dummy node in front of head removes the special case "left == 1", where the
        # head itself moves. With the dummy there is always a real node before the segment.
        dummy = ListNode(0, head)

        # Walk `prev` to the node just BEFORE position `left` (1-indexed).
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next

        # Head-insertion reversal: `cur` stays pinned at the first node of the segment and
        # keeps sliding backwards as we repeatedly lift the node after it to the front.
        cur = prev.next
        for _ in range(right - left):
            nxt = cur.next          # the node we are lifting out
            cur.next = nxt.next     # unlink it -- cur now skips over nxt
            nxt.next = prev.next    # nxt points at the current front of the segment
            prev.next = nxt         # nxt becomes the new front

        return dummy.next
