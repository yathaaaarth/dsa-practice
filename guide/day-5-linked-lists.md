# Day 5 — Linked Lists

> **Today's big idea:** linked lists have no indices, no `len()`, and no way back. Everything
> you do is pointer manipulation, and **two techniques carry the entire topic**: fast & slow
> pointers (which extract positional information without counting) and the dummy node (which
> deletes every "what if the head changes?" special case).

**Warm-up (10 min, blank screen):** re-solve Valid Parentheses (stack version) and Daily
Temperatures.

Today you also finally write [`29-Reversed_ll.py`](../29-Reversed_ll.py) — it was empty in
your repo, the one problem in the original 50 that was never solved.

---

## Pattern primer

### The node

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

That's all there is. `head` is a reference to the first node; the last node's `next` is
`None`. There is **no length, no index, no backwards pointer**. Every operation is a walk.

**Draw the list.** Every time. Boxes and arrows, on paper. Linked-list bugs are almost always
"I lost the rest of the list" or "I updated the wrong arrow", and both are obvious in a
diagram and invisible in your head.

### Technique 1 — Fast & slow pointers (Floyd)

```python
slow = fast = head
while fast and fast.next:        # BOTH checks -- fast.next.next must be legal
    slow = slow.next             # 1 step
    fast = fast.next.next        # 2 steps
```

Two facts fall out of this single loop:

- **When `fast` reaches the end, `slow` is at the middle.** It moved half as far.
- **If there is a cycle, `fast` and `slow` must meet.** Inside a loop, `fast` gains one
  position on `slow` per iteration, so it closes any gap and cannot jump past — the gap
  shrinks by exactly 1 each step until it's 0.

**The loop condition is the thing to get exactly right.** `while fast and fast.next:`
- `fast` — is `fast` itself a real node? (even-length lists end here)
- `fast.next` — because we're about to write `fast.next.next`; without this check you get
  `AttributeError: 'NoneType' object has no attribute 'next'` (odd-length lists end here)

Both, in that order. `and` short-circuits, so the second is only evaluated when the first
passes.

### Technique 2 — The dummy node

```python
dummy = ListNode(0, head)     # a fake node in front
prev = dummy
# ... do work, possibly changing what follows dummy ...
return dummy.next             # the real head, whatever it turned out to be
```

**The problem it solves:** the head is special. It has nothing before it, so "delete a node"
or "insert before a node" needs a separate code path when the target *is* the head. That
special case is where the bugs live.

A dummy node gives the head a predecessor, so **every** node — head included — is handled by
the same code. Then `dummy.next` is the answer, whether or not the head changed.

Use it whenever the head might be removed or replaced.

### Technique 3 — In-place reversal

```python
prev, curr = None, head
while curr:
    nxt = curr.next          # SAVE -- the next line destroys this link
    curr.next = prev         # flip the arrow backwards
    prev = curr              # both pointers advance
    curr = nxt
return prev                  # curr is None; prev is the new head
```

**The `nxt` save is the entire trick.** `curr.next = prev` overwrites your only route to the
rest of the list. Grab it first, or you've orphaned everything after `curr`.

Draw four boxes and step through this by hand once. It appears in problems 4, 5, and 8 today.

---

## 1. Middle of the Linked List

**[LeetCode 876 →](https://leetcode.com/problems/middle-of-the-linked-list/)** · Easy · Fast & slow · [`25-Middle_ll.py`](../25-Middle_ll.py)

### In one line
Return the middle node. For even length, return the **second** middle.

```
1→2→3→4→5     → 3
1→2→3→4→5→6   → 4      (second middle, not 3)
```

### Recognise it
"Middle", "halfway". You could count the length then walk `n//2` steps — two passes, and
perfectly acceptable. Fast & slow does it in **one pass**, which is the answer they want.

### Intuition
If `fast` moves twice as fast as `slow`, then when `fast` has covered the whole list, `slow`
has covered exactly half. No counting required — the ratio does the arithmetic.

### Dry run — `1→2→3→4→5`

| step | slow | fast | `fast and fast.next`? |
|---|---|---|---|
| start | 1 | 1 | yes |
| 1 | 2 | 3 | yes |
| 2 | **3** | 5 | `fast.next` is None → **stop** |

→ node 3 ✓

Even length, `1→2→3→4→5→6`:

| step | slow | fast | continue? |
|---|---|---|---|
| start | 1 | 1 | yes |
| 1 | 2 | 3 | yes |
| 2 | 3 | 5 | yes |
| 3 | **4** | None | `fast` is None → **stop** |

→ node 4, the **second** middle ✓

### The code

```python
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head                       # (1)
        fast = head
        while fast and fast.next:         # (2)
            slow = slow.next
            fast = fast.next.next         # (3)
        return slow                       # (4)
```

**(1)** Both start at `head`. (`slow = fast = head` is equivalent — see
[Python §12](./01-python-for-dsa.md).)

**(2)** **The two-part condition, and the reason for each:**
- `fast` handles **even**-length lists — `fast` lands exactly on `None` past the end.
- `fast.next` handles **odd**-length lists — `fast` stops on the last real node, and
  `fast.next.next` would crash.

Order matters: `and` short-circuits, so if `fast` is `None` the second test never runs. Swap
them and you get `AttributeError`.

**(3)** Two steps. Safe precisely because (2) verified both hops exist.

**(4)** When `fast` falls off the end, `slow` is at the middle. For even lengths this
naturally lands on the *second* middle, which is what the problem asks — no adjustment needed.

### Complexity
- **Time O(n)** — `fast` traverses the list once; `slow` covers half.
- **Space O(1)** — two pointers. That's the win over "store all nodes in a list and index the
  middle", which is O(n) space.

### The variant to remember
To get the **first** middle for even lengths (needed for splitting a list in half — merge
sort, palindrome checks), start `fast` one step ahead:
```python
slow, fast = head, head.next
```

### Try next
[Linked List Cycle (next)](https://leetcode.com/problems/linked-list-cycle/) ·
[Palindrome Linked List (problem 8)](https://leetcode.com/problems/palindrome-linked-list/) ·
[Delete the Middle Node of a Linked List](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/)

---

## 2. Linked List Cycle

**[LeetCode 141 →](https://leetcode.com/problems/linked-list-cycle/)** · Easy · Floyd's cycle detection · [`26-Cycle_ll.py`](../26-Cycle_ll.py)

### In one line
Does the list contain a cycle?

### Recognise it
"Cycle", "loop", "does it terminate". The O(n)-space answer is a set of visited nodes. The
answer they want is **O(1) space**, and that means Floyd.

### Intuition
Picture two runners on a circular track at different speeds. The faster one **must** lap the
slower one — they cannot pass without meeting, because the gap closes by exactly one position
per step.

On a linked list: if there's a cycle, both pointers eventually enter it, and then `fast` gains
one position per iteration on `slow`. A gap of `g` becomes `g−1`, then `g−2`, … then 0. They
meet. If there's no cycle, `fast` simply runs off the end and the loop exits.

The "gains exactly one per step" part is why the speeds must be 1 and 2 — with speeds 1 and 3
the gap changes by 2 each step and could skip over zero.

### Dry run — `3→2→0→-4` with `-4` pointing back to `2`

| step | slow | fast | meet? |
|---|---|---|---|
| start | 3 | 3 | — |
| 1 | 2 | 0 | no |
| 2 | 0 | 2 | no |
| 3 | −4 | −4 | **yes → True** |

### The code

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        while fast and fast.next:      # (1)
            slow = slow.next
            fast = fast.next.next
            if slow == fast:           # (2)
                return True
        return False                   # (3)
```

**(1)** Identical condition to problem 1 — and here it does double duty: it's also the
**no-cycle exit**. A list without a cycle has an end, so `fast` reaches it and the loop stops.

**(2)** **Check after moving, not before.** Both start at `head`, so testing first would
report a cycle immediately on every input. Move, then compare.

`==` on objects without a custom `__eq__` compares **identity** — the same object in memory —
which is exactly right. (`is` would be more explicit about that intent.) Comparing `.val`
would be wrong: two different nodes can hold the same value.

**(3)** `fast` ran off the end → no cycle.

### Complexity
- **Time O(n)** — before entering the cycle, at most n steps; inside it, at most one lap.
- **Space O(1)** — two pointers, versus O(n) for the visited-set approach. That is the entire
  reason this algorithm is famous.

### Try next
[Linked List Cycle II (next)](https://leetcode.com/problems/linked-list-cycle-ii/) — find where the cycle *starts* ·
[Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) — Floyd on an **array**, a beautiful reframing ·
[Happy Number](https://leetcode.com/problems/happy-number/) — Floyd on a number sequence

---

## 3. Linked List Cycle II `LC-142`

**[LeetCode 142 →](https://leetcode.com/problems/linked-list-cycle-ii/)** · Medium · Floyd, phase 2 · *new*

### In one line
Return the **node where the cycle begins**, or `None`.

### Recognise it
Cycle detection plus "where". There's a genuinely surprising piece of maths here — this is one
of the few problems where the proof is worth memorising alongside the code.

### Intuition — with the proof

Let:
- `F` = distance from `head` to the cycle entrance
- `a` = distance from the entrance to the meeting point (along the cycle)
- `C` = cycle length

When they meet:
- `slow` has travelled `F + a`
- `fast` has travelled `F + a + nC` for some whole number of extra laps `n`
- `fast` travelled exactly twice as far: `2(F + a) = F + a + nC`

Rearranging: **`F + a = nC`**, so **`F = nC − a`**.

Read that last equation: the distance from the head to the entrance (`F`) equals the distance
from the meeting point onward, around the cycle, back to the entrance (`nC − a`).

**Therefore:** put one pointer back at `head`, leave the other at the meeting point, and
advance both **one step at a time**. They travel equal distances and **meet exactly at the
cycle entrance**.

### Dry run — `3→2→0→-4`, cycle back to `2` (index 1). `F = 1`, `C = 3`

Phase 1 — they meet at node `-4` (from problem 2).

Phase 2:

| step | `p1` (from head) | `p2` (from meeting point) | equal? |
|---|---|---|---|
| start | 3 | −4 | no |
| 1 | **2** | **2** | **yes** |

→ node `2` ✓ — the cycle entrance.

### The code

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head

        while fast and fast.next:          # (1) --- phase 1: find a meeting point
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                p1, p2 = head, slow        # (2) --- phase 2
                while p1 != p2:            # (3)
                    p1 = p1.next
                    p2 = p2.next           # (4)
                return p1                  # (5)

        return None                        # (6)
```

**(1)** Phase 1 is problem 2, unchanged.

**(2)** `p1` restarts at `head`; `p2` stays at the meeting point. This is where `F = nC − a`
gets cashed in.

**(3)** `while p1 != p2` — they may already be equal (when the cycle starts at the head, so
`F = 0`), in which case the loop body never runs and we return `head` immediately. Correct.

**(4)** **Both move ONE step now.** Phase 2 is not fast-and-slow; the equal-distance argument
requires equal speed. Leaving `p2` at double speed here is the classic error.

**(5)** They meet at the entrance. Return either.

**(6)** No cycle.

### Complexity
- **Time O(n)** — phase 1 is O(n), phase 2 is at most one more traversal.
- **Space O(1)**.

### Try next
[Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) — the array version, and a genuinely lovely problem ·
[Happy Number](https://leetcode.com/problems/happy-number/) ·
[Circular Array Loop](https://leetcode.com/problems/circular-array-loop/)

---

## 4. Reverse Linked List

**[LeetCode 206 →](https://leetcode.com/problems/reverse-linked-list/)** · Easy · In-place reversal · [`27-Reversed_ll.py`](../27-Reversed_ll.py)

### In one line
Reverse the list and return the new head.

```
1→2→3→4→5  →  5→4→3→2→1
```

### Recognise it
The most fundamental linked-list operation there is. It appears *inside* problems 5, 8, and a
dozen harder ones. Know it cold — you should be able to write it without thinking.

### Intuition
Walk the list flipping each `next` pointer to point backwards. You need three references at
all times:

- `prev` — the part already reversed (initially nothing)
- `curr` — the node being flipped
- `nxt` — **saved before flipping**, because the flip destroys the forward link

Miss `nxt` and you've cut the list in half with no way to reach the rest.

### Dry run — `1→2→3`

| step | prev | curr | nxt | after `curr.next = prev` |
|---|---|---|---|---|
| start | None | 1 | — | |
| 1 | None | 1 | 2 | `1→None` |
| 2 | 1 | 2 | 3 | `2→1→None` |
| 3 | 2 | 3 | None | `3→2→1→None` |
| 4 | 3 | None | — | loop ends, return `prev = 3` |

### The code

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None                # (1)
        curr = head
        while curr:                # (2)
            next = curr.next       # (3)
            curr.next = prev       # (4)
            prev = curr            # (5)
            curr = next
        return prev                # (6)
```

**(1)** `prev = None` because the old head becomes the new **tail**, and a tail's `next` must
be `None`. Initialising to `None` gives that for free on the first iteration.

**(2)** `while curr:` — stop when we walk off the end. This also handles the empty list: if
`head` is `None`, the loop never runs and we return `None`. No special case needed.

**(3)** **The save.** The next line overwrites `curr.next`. Without this line you lose every
node after `curr` permanently — the single most common linked-list bug.

*(Naming note: `next` shadows Python's built-in `next()` function. Harmless in this scope, but
`nxt` is the conventional spelling and avoids the question.)*

**(4)** The flip.

**(5)** Both pointers advance. `prev` becomes the head of the growing reversed portion.

**(6)** `curr` is `None`, so `prev` is the last node processed — the new head.

### Complexity
- **Time O(n)** — one pass.
- **Space O(1)** — three references, no allocation. (The recursive version is O(n) space for
  the call stack; interviewers sometimes ask for it, but iterative is what you should write.)

### Try next
[Reverse Linked List II (next)](https://leetcode.com/problems/reverse-linked-list-ii/) ·
[Palindrome Linked List (problem 8)](https://leetcode.com/problems/palindrome-linked-list/) ·
[Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) (hard, but it's just this in a loop)

---

## 5. Reverse Linked List II

**[LeetCode 92 →](https://leetcode.com/problems/reverse-linked-list-ii/)** · Medium · Dummy node + head insertion · [`29-Reversed_ll.py`](../29-Reversed_ll.py)

> **This was the empty file in your repo** — the one problem from the original 50 that was
> never solved. It's now written.

### In one line
Reverse only positions `left` through `right` (1-indexed), leaving the rest intact.

```
1→2→3→4→5, left=2, right=4  →  1→4→3→2→5
```

### Recognise it
Reversal with boundaries. Two things make it harder than problem 4: you must **reconnect**
the reversed segment to both neighbours, and `left = 1` means the head itself moves — the
exact situation a dummy node exists for.

### Intuition
Rather than the three-pointer reversal, use **head insertion**, which handles the reconnection
automatically:

- `prev` = the node just before the segment (never moves)
- `cur` = the **first** node of the segment. It stays pinned to the same node the whole time,
  and slides steadily backwards as things are lifted over it — so at the end it's the segment's
  *last* node, already pointing at whatever follows.

Repeat `right − left` times: take the node right after `cur`, unlink it, and insert it at the
**front** of the segment (just after `prev`).

The reconnection at both ends is free: `prev.next` is always updated to the new front, and
`cur.next` never stops pointing at the tail of the list.

### Dry run — `1→2→3→4→5`, `left = 2`, `right = 4`

`dummy→1→2→3→4→5`. Walk `prev` to node 1. `cur` = node 2. Loop `4−2 = 2` times.

| iteration | `nxt` | `cur.next = nxt.next` | `nxt.next = prev.next` | `prev.next = nxt` | list |
|---|---|---|---|---|---|
| start | | | | | `1→2→3→4→5` |
| 1 | 3 | `2→4` | `3→2` | `1→3` | `1→3→2→4→5` |
| 2 | 4 | `2→5` | `4→3` | `1→4` | `1→4→3→2→5` |

→ `1→4→3→2→5` ✓

Notice `cur` stayed on node 2 throughout, drifting from position 2 to position 4 as nodes were
lifted over it.

### The code

```python
class Solution:
    def reverseBetween(self, head, left: int, right: int):
        dummy = ListNode(0, head)          # (1)

        prev = dummy
        for _ in range(left - 1):          # (2)
            prev = prev.next

        cur = prev.next                    # (3)
        for _ in range(right - left):      # (4)
            nxt = cur.next                 # (5)
            cur.next = nxt.next            # (6)
            nxt.next = prev.next           # (7)
            prev.next = nxt                # (8)

        return dummy.next                  # (9)
```

**(1)** **The dummy node.** When `left = 1` the head itself is inside the reversed segment and
will move. Without a dummy you'd need a whole separate branch for that case. With one, `prev`
is always a real node and the loop below never cares whether it's touching the head.

**(2)** Walk to the node **just before** position `left`. Positions are 1-indexed, so reaching
position `left` takes `left − 1` steps from the dummy (which sits at "position 0").

**(3)** `cur` is the first node of the segment — and it **never changes**. It will end up as
the segment's tail, which is exactly right: its `next` already points at the node after the
segment, so the right-hand reconnection happens by itself.

**(4)** `right − left` insertions. Reversing a segment of length L needs L−1 lifts, and
`right − left` is L−1.

**(5)** The node being lifted out.

**(6)** Unlink it: `cur` skips over `nxt`.

**(7)** `nxt` points at the current front of the segment. Note this reads `prev.next`, which is
still the *old* front at this moment — the ordering of (7) before (8) is essential. Swap them
and `nxt.next = nxt`, a self-loop that hangs the list.

**(8)** `nxt` becomes the new front.

**(9)** `dummy.next` — the real head, whether or not it changed. This line is why the dummy
earns its keep.

### Complexity
- **Time O(n)** — `left − 1` steps to position, then `right − left` constant-time insertions.
  One pass.
- **Space O(1)**.

### Edge cases (all handled with no extra code)
- `left == right` → the loop runs 0 times, list unchanged ✓
- `left == 1` → `prev` stays the dummy, head correctly replaced ✓
- single node → nothing to do ✓

### Try next
[Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) ·
[Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) ·
[Rotate List](https://leetcode.com/problems/rotate-list/)

---

## 6. Remove Linked List Elements

**[LeetCode 203 →](https://leetcode.com/problems/remove-linked-list-elements/)** · Easy · Deletion / dummy node · [`28-Remove_ll_element.py`](../28-Remove_ll_element.py)

### In one line
Delete every node whose value equals `val`.

```
1→2→6→3→4→5→6, val=6  →  1→2→3→4→5
7→7→7→7, val=7        →  (empty)
```

### Recognise it
Deletion, where the head might also need deleting. **The dummy-node problem, in its purest
form.**

### Intuition
To delete a node you need its **predecessor**, so you can point `prev.next` past it. The head
has no predecessor — hence the special case, hence the dummy.

### Your solution

```python
class Solution:
    def removeElements(self, head, val):
        if not head:
            return head

        node = head
        while node and node.next:          # (1)
            if node.next.val == val:
                node.next = node.next.next # (2)
            else:
                node = node.next           # (3)

        if head.val == val:                # (4)
            head = head.next

        return head
```

**(1)** Look **ahead** — inspect `node.next`, because that's the node you can actually
unlink.

**(2)** Skip it. Note we do **not** advance `node` here: the new `node.next` also needs
checking, since values can repeat consecutively (`1→7→7→2`). Advancing here would skip the
second `7`.

**(3)** Only advance when nothing was deleted.

**(4)** **The head special case, deferred to the end.** This is correct but subtle. It works
because a run of matching heads (`7→7→7`) is collapsed by the loop into a single leading `7`
— every `7` after the first is deleted by (2) — and then this one line removes the survivor.

It's correct. I verified it against `[7,7,7,7]`, `[1,1,2]`, and `[1,2,1]`. But you have to
*reason* about it to be sure, and that's the cost of not using a dummy.

### The dummy-node version — the one to write

```python
class Solution:
    def removeElements(self, head, val):
        dummy = ListNode(0, head)          # (1)
        prev = dummy

        while prev.next:                   # (2)
            if prev.next.val == val:
                prev.next = prev.next.next # (3) delete; do NOT advance
            else:
                prev = prev.next           # (4)

        return dummy.next                  # (5)
```

**(1)** The dummy gives the head a predecessor, so the head is no longer special.

**(2)** One loop, one condition, no trailing fix-up.

**(3)** Delete and **stay put**, so consecutive matches are all caught.

**(4)** Advance only on a non-match.

**(5)** `dummy.next` — the head, or `None` if everything was deleted.

Fewer lines, no reasoning required, and the empty-list check at the top of your version
becomes unnecessary too. **This is what the dummy node buys.**

### Complexity
Both versions: **O(n) time, O(1) space.**

### Try next
[Remove Nth Node From End (next)](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) ·
[Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) ·
[Delete Node in a Linked List](https://leetcode.com/problems/delete-node-in-a-linked-list/) (the trick one)

---

## 7. Remove Nth Node From End of List `LC-19`

**[LeetCode 19 →](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)** · Medium · Two pointers with a gap + dummy · *new*

### In one line
Remove the nth node **from the end**, in one pass.

```
1→2→3→4→5, n = 2  →  1→2→3→5
```

### Recognise it
"From the end" + "one pass". A linked list has no length, so counting first is two passes. The
trick: **two pointers held a fixed distance apart**.

### Intuition
Advance `fast` exactly `n` steps ahead of `slow`. Now move both together. When `fast` reaches
the end, `slow` is `n` nodes from the end — because the gap between them never changed.

Combined with a dummy node (in case the *head* is the one being removed, e.g. a 1-node list
with `n = 1`), `slow` conveniently stops on the **predecessor** of the target, which is exactly
what deletion needs.

### Dry run — `1→2→3→4→5`, `n = 2`

`dummy→1→2→3→4→5`. Both start at `dummy`. Advance `fast` 2 steps → `fast` at node 2.

| step | slow | fast | `fast.next`? |
|---|---|---|---|
| start | dummy | 2 | yes |
| 1 | 1 | 3 | yes |
| 2 | 2 | 4 | yes |
| 3 | **3** | 5 | `fast.next` is None → **stop** |

`slow` is node 3 = the predecessor of node 4, the 2nd from the end. `slow.next = slow.next.next`
→ `1→2→3→5` ✓

### The code

```python
class Solution:
    def removeNthFromEnd(self, head, n: int):
        dummy = ListNode(0, head)          # (1)
        slow = fast = dummy                # (2)

        for _ in range(n):                 # (3)
            fast = fast.next

        while fast.next:                   # (4)
            slow = slow.next
            fast = fast.next

        slow.next = slow.next.next         # (5)
        return dummy.next                  # (6)
```

**(1)** The dummy handles removing the head. With `[1]` and `n = 1`, `slow` stays at the dummy
and `dummy.next` becomes `None` — correct, and no special case.

**(2)** Both start at the **dummy**, not at `head`. This one-position offset is what makes
`slow` land on the *predecessor* rather than the target itself. Starting both at `head` gives
you the node to delete but not the one before it — useless, since you can't unlink without the
predecessor.

**(3)** Open the gap to exactly `n`.

**(4)** `while fast.next:` (not `while fast:`) — stop when `fast` is on the **last node**, not
past it. That extra position is what makes `slow` land on the predecessor. This is the line to
get right; `while fast:` puts `slow` one node too far.

**(5)** Unlink. Guaranteed safe: the problem promises `1 <= n <= length`, so `slow.next` exists.

**(6)** The head, changed or not.

### Complexity
- **Time O(n)** — one pass. The naive version (count the length, then walk `len − n`) is two
  passes and also O(n), but "one pass" is explicitly the follow-up they ask for.
- **Space O(1)**.

### Try next
[Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) ·
[Remove Duplicates from Sorted List II](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/) ·
[Swapping Nodes in a Linked List](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/)

---

## 8. Palindrome Linked List

**[LeetCode 234 →](https://leetcode.com/problems/palindrome-linked-list/)** · Easy · Fast/slow + reversal · [`30-Palindrome.py`](../30-Palindrome.py)

### In one line
Is the list a palindrome? **O(n) time, O(1) space.**

```
1→2→2→1 → True        1→2 → False
```

### Recognise it
Palindrome + linked list + constant space. This is the problem that **combines** today's first
two techniques, which is why it's the best problem of the day despite being marked Easy.

### Intuition
With an array you'd use two pointers from both ends — but a linked list has no way to walk
backwards.

The O(n)-space answer is to copy the values into a list and check `vals == vals[::-1]`. To get
O(1):

1. **Find the middle** with fast & slow (problem 1).
2. **Reverse the second half** in place (problem 4).
3. **Walk both halves in parallel**, comparing values.

Two techniques you already know, composed.

### Dry run — `1→2→2→1`

**Phase 1** — find the middle:

| step | slow | fast |
|---|---|---|
| start | 1 | 1 |
| 1 | 2(a) | 2(b) |
| 2 | 2(b) | None → stop |

`slow` is at the second `2`, the start of the back half.

**Phase 2** — reverse from `slow`: `2(b)→2(a)... ` wait — reversing from `slow` onward gives
`1→2(b)`, with `node` (the new head of the reversed part) at the original tail `1`.

**Phase 3** — compare, walking `node` from the reversed back half and `head` from the front:

| node | head | equal? |
|---|---|---|
| 1 | 1 | yes |
| 2 | 2 | yes |
| (None) | | → **True** ✓ |

### The code

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        fast = slow = head

        # Find the mid node
        while fast and fast.next:          # (1)
            fast = fast.next.next
            slow = slow.next

        # Reverse the second half
        node = None                        # (2)
        while slow:
            nxt = slow.next
            slow.next = node
            node = slow
            slow = nxt

        # Compare the first and second half nodes
        while node:                        # (3)
            if node.val != head.val:
                return False
            node = node.next
            head = head.next               # (4)
        return True
```

**(1)** Problem 1, verbatim.

**(2)** Problem 4, verbatim, starting from `slow`. `node` ends up as the head of the reversed
back half.

**(3)** **Iterate on `node`, not on `head`** — this is the subtle and important choice. For
**odd**-length lists the two halves overlap by one node (the exact middle belongs to both), so
the reversed half is one node *longer*… no: it's the same length or one shorter depending on
where `slow` stopped. Either way, the reversed half is never longer than the front half, so
looping on `node` cannot run off the end of `head`.

Check `1→2→1`: `slow` stops at the final `1`; the reversed half is `1→2→1` reversed from
`slow`, i.e. just `1`. Compare `1` vs `head`'s `1` → True ✓. The middle `2` is never compared
against anything, which is correct — a middle element is always trivially a palindrome by
itself.

**(4)** Both walk forward one step, from opposite ends of the original list.

### Complexity
- **Time O(n)** — three passes (find middle, reverse, compare), each O(n). 3n = O(n).
- **Space O(1)** — the entire point. The copy-to-list version is O(n) space and is a fine first
  answer, but this is the follow-up they're after.

### The caveat worth mentioning
This **mutates the input list** — the second half is left reversed. Interviewers love asking
"can you restore it?" The answer is yes: reverse the second half again after comparing. Say so
proactively.

### Try next
[Reorder List](https://leetcode.com/problems/reorder-list/) — find middle + reverse + merge, all three techniques ·
[Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) ·
[Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) (the string version)

---

## 9. Merge Two Sorted Lists

**[LeetCode 21 →](https://leetcode.com/problems/merge-two-sorted-lists/)** · Easy · Dummy node + two pointers · [`31-Merg_sorted_ll.py`](../31-Merg_sorted_ll.py)

### In one line
Merge two sorted lists into one sorted list, splicing the existing nodes.

```
1→2→4  +  1→3→4  →  1→1→2→3→4→4
```

### Recognise it
The merge step of merge sort. It's also the building block for
[Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/), which is a very
common hard question.

### Intuition
Repeatedly take the smaller of the two front nodes and append it to the result. When one list
runs out, the other is already sorted — attach the whole remainder in one operation.

The dummy node removes the "which list has the first node?" special case: you build onto
`dummy` and read off `dummy.next` at the end.

### Dry run — `[1,2,4]` and `[1,3,4]`

| l1 | l2 | comparison | take | result so far |
|---|---|---|---|---|
| 1 | 1 | 1 > 1? no → else | l1's 1 | `1` |
| 2 | 1 | 2 > 1 | l2's 1 | `1→1` |
| 2 | 3 | 2 > 3? no | l1's 2 | `1→1→2` |
| 4 | 3 | 4 > 3 | l2's 3 | `1→1→2→3` |
| 4 | 4 | 4 > 4? no | l1's 4 | `1→1→2→3→4` |
| None | 4 | loop ends | attach rest of l2 | `1→1→2→3→4→4` |

### The code

```python
class Solution:
    def mergeTwoLists(self, list1, list2):
        dummy = ListNode()                 # (1)
        cur = dummy                        # (2)

        while list1 and list2:             # (3)
            if list1.val > list2.val:      # (4)
                cur.next = list2
                list2 = list2.next
            else:
                cur.next = list1
                list1 = list1.next
            cur = cur.next                 # (5)

        if list1:                          # (6)
            cur.next = list1
        else:
            cur.next = list2

        return dummy.next                  # (7)
```

**(1)** `ListNode()` with default `val=0, next=None`. Its value is never read — it exists
purely to have something to hang the first real node off.

**(2)** `cur` is the **tail of the result**, always pointing at the last node appended. `dummy`
stays put so we can find the head later.

**(3)** `and` — stop as soon as *either* list is exhausted, since the comparison at (4) needs
both.

**(4)** `>` and not `>=`. On a tie we take from `list1`, which makes the merge **stable**
(equal elements keep their relative source order). Not required here, but stability matters in
merge sort and it's free.

**(5)** Advance the tail. Note we're **splicing existing nodes**, not creating new ones — no
allocation, which is why the space is O(1).

**(6)** One list is empty; the other's remainder is already sorted, so attach it wholesale in
O(1). No loop needed. (Shorter: `cur.next = list1 or list2` — `or` returns the first truthy
operand, or the second if both are `None`.)

**(7)** The real head. If `list1` started smaller, that's `list1`'s first node; otherwise
`list2`'s. **The dummy meant we never had to ask.**

### Complexity
- **Time O(n + m)** — every node is visited once.
- **Space O(1)** — nodes are relinked, not copied. (The recursive version is O(n+m) stack space.)

### Try next
[Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) — this + a **heap** (Day 3!) ·
[Sort List](https://leetcode.com/problems/sort-list/) — merge sort on a linked list ·
[Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)

---

## 10. Add Two Numbers `LC-2`

**[LeetCode 2 →](https://leetcode.com/problems/add-two-numbers/)** · Medium · Dummy node + carry · *new*

### In one line
Two numbers stored as linked lists in **reverse** digit order. Add them, return the sum in the
same format.

```
2→4→3  +  5→6→4   →  7→0→8
(342 + 465 = 807)
```

### Recognise it
Digit-by-digit arithmetic. The reversed storage is a **gift**, not an obstacle: the least
significant digit comes first, which is exactly the order you add in by hand.

### Intuition
Long addition, one column at a time, carrying into the next. The three things that make it
fiddly are all handled by one loop condition:

- The lists can be **different lengths**.
- The carry can survive past **both** lists (`5 + 5 = 10` → `0→1`).
- Either list can be empty.

### Dry run — `[2,4,3] + [5,6,4]`

| l1 | l2 | carry in | total | digit | carry out |
|---|---|---|---|---|---|
| 2 | 5 | 0 | 7 | 7 | 0 |
| 4 | 6 | 0 | 10 | **0** | **1** |
| 3 | 4 | 1 | 8 | 8 | 0 |
| — | — | 0 | loop ends | | |

→ `7→0→8` ✓

And the carry-past-the-end case, `[5] + [5]`:

| l1 | l2 | carry | total | digit | carry out |
|---|---|---|---|---|---|
| 5 | 5 | 0 | 10 | 0 | 1 |
| — | — | 1 | 1 | 1 | 0 |

→ `0→1` — the loop ran an extra time **because `carry` was still 1**.

### The code

```python
class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()
        cur = dummy
        carry = 0                                  # (1)

        while l1 or l2 or carry:                   # (2)
            v1 = l1.val if l1 else 0               # (3)
            v2 = l2.val if l2 else 0

            total = v1 + v2 + carry                # (4)
            carry = total // 10                    # (5)
            cur.next = ListNode(total % 10)        # (6)
            cur = cur.next

            l1 = l1.next if l1 else None           # (7)
            l2 = l2.next if l2 else None

        return dummy.next
```

**(1)** The carry between columns, 0 or 1.

**(2)** **The three-part condition is the whole problem.** `or`, not `and`:
- `l1` — the first list still has digits
- `l2` — the second still has digits
- `carry` — **there's a leftover carry even though both lists are done**

Drop the `carry` term and `[5] + [5]` returns `0` instead of `0→1`. That's the classic bug here.

**(3)** Treat a finished list as contributing **0** — which is exactly right, since
`342 = 0342`. This one-liner removes the entire "different lengths" special case.

**(4)** The column sum: at most `9 + 9 + 1 = 19`, so the carry is always 0 or 1.

**(5)** `//` — integer division. `19 // 10 = 1`. With `/` you'd get `1.9` and the next
iteration's arithmetic would be float garbage. See [Python §4](./01-python-for-dsa.md).

**(6)** `total % 10` is the digit to store. `19 % 10 = 9`.

**(7)** Advance only if there's something to advance to. `l1.next if l1 else None` guards
against `AttributeError` on the shorter list.

### Complexity
- **Time O(max(n, m))** — one pass over the longer list, plus at most one extra iteration for
  a final carry.
- **Space O(max(n, m))** for the output list; **O(1)** auxiliary.

### The follow-up
[Add Two Numbers II](https://leetcode.com/problems/add-two-numbers-ii/) stores digits in
*forward* order, so you can't add left to right. Three good answers: reverse both lists first
(problem 4), push onto stacks (Day 4), or use recursion. Worth doing — it forces you to
combine two days' patterns.

### Try next
[Add Two Numbers II](https://leetcode.com/problems/add-two-numbers-ii/) ·
[Plus One](https://leetcode.com/problems/plus-one/) ·
[Multiply Strings](https://leetcode.com/problems/multiply-strings/)

---

## Recall drill

1. Write the fast & slow loop condition exactly. Why two checks, and why in that order?
2. What problem does the dummy node solve, and what do you return at the end?
3. In the three-pointer reversal, what breaks if you delete the `nxt = curr.next` line?
4. In Remove Nth From End, why do both pointers start at the **dummy** rather than at `head`,
   and why is the loop `while fast.next` instead of `while fast`?
5. In Add Two Numbers, why is the loop condition `while l1 or l2 or carry` and not
   `while l1 and l2`?

<details>
<summary>Answers</summary>

1. `while fast and fast.next:`. `fast` catches **even**-length lists, where `fast` lands
   exactly on `None`. `fast.next` catches **odd**-length lists, where `fast` stops on the last
   real node and `fast.next.next` would raise `AttributeError`. Order matters because `and`
   short-circuits — checking `fast.next` first would crash when `fast` is `None`.
2. It gives the head a **predecessor**, so code that deletes or inserts before a node needs no
   special case when the target is the head. Return `dummy.next` — the real head, whether or
   not it changed.
3. `curr.next = prev` overwrites your **only** reference to the rest of the list, so everything
   after `curr` is orphaned and unreachable. You'd end up returning a one- or two-node list.
4. **Dummy start:** the one-position offset makes `slow` stop on the *predecessor* of the
   target, which is what deletion requires — you cannot unlink a node without the node before
   it. **`while fast.next`:** it stops `fast` on the last node rather than past the end, and
   that extra position is precisely what puts `slow` on the predecessor. `while fast` sends
   `slow` one node too far.
5. Because the lists can be different lengths (`or`, not `and`) **and** because a final carry
   can outlive both lists — `[5] + [5]` must produce `0→1`, which needs one more iteration
   after both lists are exhausted. Missing the `carry` term returns `0`.

</details>

---

**Tomorrow:** [Day 6 — Binary Trees](./day-6-trees.md). Nine of your own solutions plus one
new. Almost every tree problem is the same six-line recursion with one line changed — once you
see that, the whole topic collapses into a single template.

**Warm-up:** re-solve **Reverse Linked List** and **Merge Two Sorted Lists** from a blank
screen. If Reverse Linked List II still feels shaky, draw it out again — it's the hardest
pointer manipulation of the week.
