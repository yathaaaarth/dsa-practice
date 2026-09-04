# Day 4 — Stacks, Queues & Monotonic Stack

> **Today's big idea:** a stack is memory with a policy — "the most recent unresolved thing
> is the one that matters". That policy solves matching, evaluation, and the entire
> "next greater element" family. Seven of today's problems are your own; three are new,
> including the **monotonic stack**, the second big pattern missing from your original 50.

**Warm-up (10 min, blank screen):** re-solve Binary Search and Kth Largest Element.
**Reference:** [Python for DSA §3 (deque)](./01-python-for-dsa.md)

---

## Pattern primer

### Stack = LIFO, and it's just a Python list

```python
stack = []
stack.append(x)      # push  -- O(1) amortised
stack.pop()          # pop the LAST item -- O(1)
stack[-1]            # peek -- O(1)
if stack:            # "not empty" -- ALWAYS guard before pop/peek
```

No import, no special class. `list` *is* the stack, because both operations happen at the
end where they're cheap.

**When a stack is the answer:** whenever the thing you need is **the most recent unresolved
item**. Matching brackets — the bracket that must close next is the last one opened.
Evaluating RPN — the operands for an operator are the last two produced. Undo — the last
action. That "most recent" phrasing is the trigger.

### Queue = FIFO, and it must be a `deque`

```python
from collections import deque
q = deque()
q.append(x)          # enqueue at the right -- O(1)
q.popleft()          # dequeue from the left -- O(1)
```

**Never use `list.pop(0)` for a queue.** A list is an array; removing the front shifts every
remaining element — O(n). Inside a loop that runs n times, your O(n) algorithm silently
becomes **O(n²)**. See [Python §3](./01-python-for-dsa.md).

### Monotonic stack — the new pattern

A stack whose contents are kept **sorted** (all increasing or all decreasing) by popping
anything that would violate the order before you push.

The insight: when you pop an element, the thing that forced the pop **is its answer**.

```python
stack = []                                   # holds INDICES; values stay decreasing
res = [0] * len(nums)

for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:     # x is bigger -> x is the "next greater"
        j = stack.pop()                      # ...for everything smaller still waiting
        res[j] = i - j                       # (or nums[i], depending on the question)
    stack.append(i)                          # x now waits for ITS next greater
return res
```

**Why it's O(n) and not O(n²):** each index is pushed exactly once and popped at most once.
The inner `while` can run many times in one iteration, but across the entire loop it runs at
most n times **in total**. Same amortised argument as Day 2's sliding window.

**Store indices, not values.** You almost always need the *distance* or the *position*, and
you can always recover the value with `nums[i]`. Going the other way is impossible.

Copy all three out by hand.

---

## 1. Valid Parentheses

**[LeetCode 20 →](https://leetcode.com/problems/valid-parentheses/)** · Easy · Stack · [`33-Valid_Parenthese.py`](../33-Valid_Parenthese.py)

### In one line
Is the bracket string correctly matched and nested?

```
"()[]{}" → True      "(]" → False      "([)]" → False      "{[]}" → True
```

### Recognise it
Matching, nesting, "properly closed". The defining test is `"([)]"` — counting brackets
isn't enough, **order** matters, and order-of-most-recent is exactly a stack.

### Intuition
Push every opening bracket. On a closing bracket, the only thing it may legally close is
**the most recently opened** one — so pop and check they're a matching pair. Mismatch, or an
empty stack, means invalid. Leftovers at the end mean unclosed brackets.

### Dry run — `s = "{[]}"`

| char | action | stack |
|---|---|---|
| `{` | push | `['{']` |
| `[` | push | `['{','[']` |
| `]` | pop `[`, matches | `['{']` |
| `}` | pop `{`, matches | `[]` |

Empty at the end → **True**

And `"([)]"`:

| char | action | stack |
|---|---|---|
| `(` | push | `['(']` |
| `[` | push | `['(','[']` |
| `)` | pop `[` — **`(` expected, `[` found** | → **False** |

### Your solution

```python
class Solution:
    def isValid(self,s:str) -> bool:
        while len(s) > 0:
            l = len(s)
            s = s.replace("()","").replace("{}","").replace("[]","")   # (1)
            if l == len(s):        # (2)
                return False
        return True                # (3)
```

**(1)** Repeatedly delete every adjacent matched pair. Valid strings collapse to nothing;
`"{[]}"` → `"{}"` → `""`.

**(2)** If a full pass removed nothing, whatever remains can never be reduced — invalid.
Without this check, an unmatched string loops forever.

**(3)** Everything vanished → valid.

This is **correct** and rather elegant. But: each `replace` scans and rebuilds the entire
string, and the outer loop can run O(n) times, so it's **O(n²) time and O(n) space**. On a
string of 10⁴ characters that's 10⁸ character operations.

### The stack solution — the one to know

```python
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {')': '(', ']': '[', '}': '{'}       # (1) closing -> opening
        stack = []

        for c in s:
            if c in pairs:                            # (2) it's a CLOSING bracket
                if not stack or stack.pop() != pairs[c]:   # (3)
                    return False
            else:
                stack.append(c)                       # (4) opening -> remember it

        return not stack                              # (5)
```

**(1)** Keyed by the **closing** bracket, because that's what triggers a lookup. Mapping
opening→closing would force you to search the dict backwards. A dict makes this O(1) and
avoids a three-way `if/elif/else`.

**(2)** `c in pairs` checks **keys**, so it's "is this a closing bracket?" — one membership
test instead of `if c == ')' or c == ']' or c == '}'`.

**(3)** Two failure modes in one condition, and the order matters:

- **`not stack`** — a closing bracket with nothing open, e.g. `")("`. Must be checked
  **first**: `stack.pop()` on an empty list raises `IndexError`. Python's `or` short-circuits,
  so if `not stack` is true the `pop` never runs. That short-circuit is load-bearing.
- **`stack.pop() != pairs[c]`** — wrong type of bracket, e.g. `"(]"`.

**(4)** Anything not a closing bracket is an opening one (the problem guarantees only these
six characters).

**(5)** `not stack` is `True` for an empty list. Leftovers mean unclosed brackets, e.g. `"(("`.
Forgetting this final check is the most common bug — `"(("` would otherwise return `True`.

### Complexity
| | Time | Space |
|---|---|---|
| Your `replace` version | O(n²) | O(n) |
| **Stack version** | **O(n)** | **O(n)** |

O(n) time: one pass, each character pushed and popped at most once. O(n) space: worst case
`"((((("` puts everything on the stack.

### Try next
[Min Stack (next)](https://leetcode.com/problems/min-stack/) ·
[Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) ·
[Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) (hard, same idea)

---

## 2. Min Stack

**[LeetCode 155 →](https://leetcode.com/problems/min-stack/)** · Medium · Auxiliary stack · [`32-minstack.py`](../32-minstack.py)

### In one line
A stack that also reports its minimum in **O(1)**.

```
push(-2) push(0) push(-3) → getMin() = -3 → pop() → top() = 0, getMin() = -2
```

### Recognise it
"Design a structure where operation X is O(1)." The general technique: **precompute and
store the answer alongside the data**, rather than computing it on demand.

### Intuition
Scanning for the minimum on each `getMin()` is O(n). Caching a single `min` variable fails
too — when you pop the minimum, what's the *new* minimum? You'd have to rescan.

The fix: keep a **second stack** that, at every depth, records the minimum of everything at
or below that depth. Push both stacks together, pop both together, and they stay in lockstep.
`minStack[-1]` is then always the current minimum.

The insight is that "the minimum" has a *history* that mirrors the main stack exactly, so
store the history instead of a single value.

### Dry run

| operation | `stack` | `minStack` | `getMin()` |
|---|---|---|---|
| `push(-2)` | `[-2]` | `[-2]` | −2 |
| `push(0)` | `[-2,0]` | `[-2,-2]` | −2 ← `min(0, -2)` |
| `push(-3)` | `[-2,0,-3]` | `[-2,-2,-3]` | −3 |
| `pop()` | `[-2,0]` | `[-2,-2]` | −2 ← restored automatically |
| `top()` | | | `0` |

### The code

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.minStack = []                                   # (1)

    def push(self, val: int) -> None:
        self.stack.append(val)
        val = min(val, self.minStack[-1] if self.minStack else val)   # (2)
        self.minStack.append(val)                            # (3)

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()                                  # (4)

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]                             # (5)
```

**(1)** Two stacks kept at **identical depth**. That invariant is what makes (4) correct.

**(2)** "The new minimum is the smaller of the incoming value and the previous minimum."
The conditional expression handles the empty case: on the first push there's no previous
minimum, so `val` compares against itself and wins. (Reassigning the parameter `val` is a bit
untidy — `new_min = ...` reads better — but it's correct.)

**(3)** Push a value even when it isn't a new minimum. That "redundant" duplicate is the
whole design: it guarantees the two stacks stay the same height, so `pop` can blindly pop
both. Trying to save space by only pushing on a new minimum breaks the lockstep and forces
you to track *when* to pop — a much bigger source of bugs than the memory you'd save.

**(4)** Pop both. No comparison, no bookkeeping, because of the invariant.

**(5)** O(1). The whole point.

### Complexity
- **All operations O(1)** — push, pop, top, getMin.
- **Space O(n)** — 2n slots instead of n. You're buying O(1) `getMin` with 2× memory.

### The space optimisation (a common follow-up)
Push to `minStack` only when `val <= minStack[-1]`, and pop only when
`stack.pop() == minStack[-1]`. Saves memory on inputs with few new minima; costs you a
comparison in `pop` and one more chance to get it wrong. Note the **`<=`** — with `<`,
duplicate minima break it: push `[2, 2]`, pop once, and the minimum is wrongly gone.

### Try next
[Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) ·
[Max Stack](https://leetcode.com/problems/max-stack/) ·
[Design a Stack With Increment Operation](https://leetcode.com/problems/design-a-stack-with-increment-operation/)

---

## 3. Evaluate Reverse Polish Notation

**[LeetCode 150 →](https://leetcode.com/problems/evaluate-reverse-polish-notation/)** · Medium · Stack evaluation · [`34-eval_reverse_polish_notation.py`](../34-eval_reverse_polish_notation.py)

> ⚠️ **This file was broken** — `st.append(first, second)` raised `TypeError` on every
> subtraction. Fixed; see [bugs-found.md §2](./bugs-found.md).

### In one line
Evaluate postfix notation, where operators follow their operands.

```
["2","1","+","3","*"] → 9        because (2 + 1) * 3
["4","13","5","/","+"] → 6       because 4 + (13 / 5) = 4 + 2
```

### Recognise it
Expression evaluation with no parentheses. RPN exists precisely because it's
**unambiguous without brackets** — and a stack evaluates it in one pass.

### Intuition
Read left to right. A number has nothing to do yet — push it. An operator's operands are, by
the definition of postfix, **the two most recent results**. Pop two, combine, push the
answer back. At the end, exactly one value remains.

### Dry run — `["10","6","9","3","+","-11","*","/","*","17","+","5","+"]`

| token | action | stack |
|---|---|---|
| `10` | push | `[10]` |
| `6` | push | `[10,6]` |
| `9` | push | `[10,6,9]` |
| `3` | push | `[10,6,9,3]` |
| `+` | 9+3 | `[10,6,12]` |
| `-11` | push | `[10,6,12,-11]` |
| `*` | 12×−11 | `[10,6,-132]` |
| `/` | 6 / −132 → `int(-0.045)` = **0** | `[10,0]` |
| `*` | 10×0 | `[0]` |
| `17` | push | `[0,17]` |
| `+` | 0+17 | `[17]` |
| `5` | push | `[17,5]` |
| `+` | 17+5 | `[22]` |

→ **22**

### The code (fixed)

```python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        st = []

        for c in tokens:
            if c == "+":
                st.append(st.pop() + st.pop())        # (1)
            elif c == "-":
                second, first = st.pop(), st.pop()    # (2)
                st.append(first - second)             # (3)
            elif c == "*":
                st.append(st.pop() * st.pop())
            elif c == "/":
                second, first = st.pop(), st.pop()
                st.append(int(first / second))        # (4)
            else:
                st.append(int(c))                     # (5)

        return st[0]                                  # (6)
```

**(1)** `+` and `*` are **commutative**, so pop order is irrelevant — `a+b == b+a`. That's
why the one-liner is safe here and not below.

**(2)** `-` and `/` are **not** commutative, so order is critical. The stack pops in reverse,
so the **first** pop is the **right** operand. Naming them `second, first` in that order
makes the intent explicit and prevents the classic `5 2 -` → `-3` bug (correct: 3).

**(3)** **This was the bug**: `st.append(first, second)` — `list.append` takes exactly one
argument. See [bugs-found.md §2](./bugs-found.md).

**(4)** `int(first / second)`, **not** `first // second`. LeetCode requires truncation
**toward zero**; `//` floors toward negative infinity. They differ on negatives:

```python
int(-7 / 2) == -3      #  truncate toward zero -- what LeetCode wants
    -7 // 2  == -4      #  floor -- a WRONG ANSWER on this problem
```

This is a real submission failure, not a nitpick. See [Python §4](./01-python-for-dsa.md).

**(5)** `int(c)` handles negative literals like `"-11"` correctly — Python's `int()` parses
the sign. Note the check is "is it an operator?" first, *else* it's a number: testing
`c.isdigit()` instead would return `False` for `"-11"` and misroute it.

**(6)** Valid RPN leaves exactly one value. `st[-1]` is equivalent and more idiomatic.

### Complexity
- **Time O(n)** — one pass; each token does O(1) work.
- **Space O(n)** — worst case (all numbers, then all operators) the stack holds n/2 values.

### Try next
[Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii/) (infix — much harder) ·
[Baseball Game](https://leetcode.com/problems/baseball-game/) ·
[Decode String](https://leetcode.com/problems/decode-string/)

---

## 4. Sort a Stack

**[GeeksforGeeks →](https://www.geeksforgeeks.org/problems/sort-a-stack/1)** · Easy · Auxiliary stack · [`35-stack_sorting.py`](../35-stack_sorting.py)

> Not a LeetCode problem — it's a classic interview exercise. The closest LeetCode relatives
> are [Remove All Adjacent Duplicates](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) (problem 8 today)
> and [Sort an Array](https://leetcode.com/problems/sort-an-array/).

### In one line
Sort a stack **using only another stack** — no arrays, no `sort()`.

```
[34,3,31,98,92,23] → [3,23,31,34,92,98]      (smallest at the bottom)
```

### Recognise it
An artificial constraint ("you may only use stack operations") designed to test whether you
can think in terms of the data structure's actual primitives. This is insertion sort in
disguise.

### Intuition
Take elements one at a time from the input stack and insert each into its correct place in a
`sorted_stack` that's kept in increasing order (largest on top).

To insert `temp`: while the top of `sorted_stack` is **bigger** than `temp`, pour those
elements back into the input stack. Now the top is ≤ `temp`, so `temp` goes on. The poured-back
elements get re-processed later and find their places again.

That "pour back and re-process" is the only way to insert into the middle of a stack when
you have no random access.

### Dry run — `[34, 3, 31]` (top is the rightmost)

| pop `temp` | pour back while `sorted[-1] > temp` | push `temp` | `input` | `sorted` |
|---|---|---|---|---|
| 31 | (empty) | 31 | `[34,3]` | `[31]` |
| 3 | 31 > 3 → move 31 back | 3 | `[34,31]` | `[3]` |
| 31 | 3 > 31? no | 31 | `[34]` | `[3,31]` |
| 34 | 31 > 34? no | 34 | `[]` | `[3,31,34]` |

→ `[3, 31, 34]` ✓

### The code

```python
def sort_stack(input_stack):
    sorted_stack = []                                # (1)

    while input_stack:                               # (2)
        temp = input_stack.pop()                     # (3)

        while sorted_stack and sorted_stack[-1] > temp:   # (4)
            input_stack.append(sorted_stack.pop())   # (5)

        sorted_stack.append(temp)                    # (6)

    return sorted_stack
```

**(1)** The auxiliary stack, maintained in increasing order — smallest at the bottom, largest
on top.

**(2)** Until every element has been placed.

**(3)** `pop()` from the end — the only element a stack lets you see.

**(4)** **The insertion step.** `sorted_stack and ...` guards the empty case — `sorted_stack[-1]`
on an empty list is `IndexError`, and Python's `and` short-circuits so the index never runs.
`>` (strict) keeps equal elements from being needlessly shuffled, making the sort stable-ish.

**(5)** Pour the too-large elements back onto the input. They'll be re-popped and re-inserted
later; this is why the algorithm is quadratic, and why it terminates anyway — each pour-back
is followed by a placement that makes net progress.

**(6)** The top of `sorted_stack` is now ≤ `temp`, so `temp` belongs here.

### Complexity
- **Time O(n²)** — each insertion can pour back up to n elements. This is insertion sort, and
  its cost is inherent to the constraint. Fully-reversed input is the worst case.
- **Space O(n)** for the auxiliary stack. If the recursive formulation is used instead, it's
  O(n) call-stack space.

### Try next
[Remove All Adjacent Duplicates (problem 8 today)](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) ·
[Sort an Array](https://leetcode.com/problems/sort-an-array/) ·
[Next Greater Element I (problem 10 today)](https://leetcode.com/problems/next-greater-element-i/)

---

## 5. Implement Stack using Queues

**[LeetCode 225 →](https://leetcode.com/problems/implement-stack-using-queues/)** · Easy · Queue rotation · [`36-implement_stack_queues.py`](../36-implement_stack_queues.py)

### In one line
Build a LIFO stack using only FIFO queue operations.

### Recognise it
"Implement X using Y" — a structural-understanding test. The question is always: *where do
you pay the cost?* You can make `push` expensive or `pop` expensive; you cannot make both
cheap.

### Intuition
A queue hands you the **oldest** element; a stack needs the **newest**. So after pushing a
new element, **rotate the queue** until that element sits at the front: dequeue and re-enqueue
everything that was ahead of it.

Then `pop` and `top` are trivially O(1) — the front is always the most recently pushed.

### Dry run — `push(1)`, `push(2)`, `push(3)`

| operation | after append | rotations (`len(q)-1`) | queue (front → back) |
|---|---|---|---|
| `push(1)` | `[1]` | 0 | `[1]` |
| `push(2)` | `[1,2]` | 1: move 1 to back | `[2,1]` |
| `push(3)` | `[2,1,3]` | 2: move 2, then 1 | `[3,2,1]` |

`pop()` → `popleft()` → **3** ✓ (LIFO from a FIFO)

### The code

```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()                          # (1)

    def push(self, x: int) -> None:
        self.q.append(x)                          # (2)
        for _ in range(len(self.q) - 1):          # (3)
            self.q.append(self.q.popleft())       # (4)

    def pop(self) -> int:
        return self.q.popleft()                   # (5)

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return len(self.q) == 0
```

**(1)** A `deque` used **strictly as a queue** — only `append` and `popleft`. That
self-imposed restriction is the point of the exercise; using `pop()` would be cheating.

**(2)** Add the new element at the back, where a queue puts things.

**(3)** `len(self.q) - 1` rotations: everything *except* the new element moves behind it.
Evaluating `len` here, **before** the loop body starts, matters — the length doesn't change
during rotation (one out, one in), but computing it up front is the clear way to express
"the count that was there".

**(4)** `popleft()` then `append()` — take from the front, put at the back. One rotation step.

**(5)** O(1). The front is the newest element, courtesy of `push`'s work.

### Complexity
- **`push`: O(n)** — n−1 rotations.
- **`pop`, `top`, `empty`: O(1)**.
- **Space O(n)**.

The classic follow-up is *"can you do it with O(1) push?"* — yes, by making `pop` do the
rotation instead (pop n−1 elements into a second queue, take the last one). Total work is
the same; you're choosing **which** operation absorbs it. Say that explicitly; it's the
answer they want.

### Try next
[Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) — the mirror, and it has a genuinely elegant **amortised O(1)** two-stack solution ·
[Design Circular Queue](https://leetcode.com/problems/design-circular-queue/) ·
[Min Stack](https://leetcode.com/problems/min-stack/)

---

## 6. Time Needed to Buy Tickets

**[LeetCode 2073 →](https://leetcode.com/problems/time-needed-to-buy-tickets/)** · Easy · Simulation → closed form · [`37-time_need_buy_ticket.py`](../37-time_need_buy_ticket.py)

> ⚠️ **This file returned wrong answers.** Off-by-one for people behind `k` with equal ticket
> counts — 27 mismatches against brute force on inputs of length ≤ 3. Fixed; see
> [bugs-found.md §3](./bugs-found.md).

### In one line
People queue in a circle, each buying one ticket per turn then rejoining the back. How many
seconds until person `k` finishes?

```
tickets = [2,3,2], k = 2 → 6
tickets = [5,1,1,1], k = 0 → 8
```

### Recognise it
A simulation you can collapse into a formula. Worth doing both ways: simulate to understand,
then derive the O(n) closed form.

### Intuition
Think about **person i** and ask: *how many tickets do they buy before the clock stops?*

The clock stops the instant person `k` buys their last ticket. So:

- **`i <= k`** (at or ahead of `k` in the queue): person `i` gets a turn in every round that
  `k` does, including `k`'s final round. They buy `min(tickets[i], tickets[k])`.
- **`i > k`** (behind `k`): the clock stops *before* their turn in the final round comes
  around. They participate in only `tickets[k] - 1` rounds, so they buy
  `min(tickets[i], tickets[k] - 1)`.

Every ticket bought is one second. Sum over everyone.

### Dry run — `tickets = [2,3,2]`, `k = 2`

| i | position | formula | tickets bought |
|---|---|---|---|
| 0 | `i < k` | `min(2, tickets[2]=2)` | 2 |
| 1 | `i < k` | `min(3, 2)` | 2 |
| 2 | `i == k` | `min(2, 2)` | 2 |

Total = **6** ✓

Verify by simulation: round 1 → p0, p1, p2 each buy (t=3); round 2 → p0, p1, p2 buy, and p2
finishes at **t=6** ✓

And the case the old code got wrong — `tickets = [2,2]`, `k = 0`:

| i | position | formula | bought |
|---|---|---|---|
| 0 | `i == k` | `min(2, 2)` | 2 |
| 1 | **`i > k`** | `min(2, 2−1)` = **1** | 1 |

Total = **3** ✓ (Simulation: p0 buys, p1 buys, p0 buys → done at t=3. The old code said 4.)

### The code (fixed)

```python
class Solution:
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        result = 0
        for i in range(len(tickets)):
            if i <= k:
                result += min(tickets[i], tickets[k])        # (1)
            else:
                result += min(tickets[i], tickets[k] - 1)    # (2)
        return result
```

**(1)** At or ahead of `k`: capped by `k`'s total, since the clock stops when `k` finishes.
Includes `i == k` itself, where `min(x, x) = x` — correct without a special case.

**(2)** **The `-1` is the entire problem.** Behind `k`, you miss the final round. The old code
branched on *ticket counts* rather than *position*, which happened to work whenever
`tickets[i] < tickets[k]` and broke on equality.

Note this branches on **`i <= k`** — position — with `min` handling the count. Getting the
branch key right is what makes it correct; getting it wrong is what made it plausible but wrong.

### Complexity
- **Time O(n)** — one pass. The naive simulation is O(n × max(tickets)), which passes here
  but doesn't generalise.
- **Space O(1)**.

### The lesson
This bug did not crash. It returned believable numbers. The only way to catch that class of
error is to **write the ten-line brute force and compare on small inputs** —
[`guide/verify.py`](./verify.py) now does exactly that, exhaustively over every queue of
length ≤ 4 with values ≤ 4. Two minutes of work; it found 27 failures.

### Try next
[Number of Students Unable to Eat Lunch](https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/) ·
[Reveal Cards In Increasing Order](https://leetcode.com/problems/reveal-cards-in-increasing-order/) ·
[Design Circular Queue](https://leetcode.com/problems/design-circular-queue/)

---

## 7. Reverse First K Elements of a Queue

**[GeeksforGeeks →](https://www.geeksforgeeks.org/problems/reverse-first-k-elements-of-queue/1)** · Easy · Stack + queue · [`38-Reverse_first_k_ele_queue.py`](../38-Reverse_first_k_ele_queue.py)

> Not a LeetCode problem. The closest relatives are
> [Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) (tomorrow!)
> and [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/).

### In one line
Reverse the first `k` elements of a queue, leaving the rest in order.

```
q = [1,2,3,4,5], k = 3 → [3,2,1,4,5]
```

### Recognise it
"Reverse a portion" + queue. **A stack is a reversal machine** — that is its defining
property. Whenever you need order flipped, a stack is the tool.

### Intuition
Three phases:

1. Dequeue the first `k` elements onto a **stack**. Popping them off comes out reversed.
2. Enqueue them back — they land at the *back* of the queue, reversed.
3. The remaining `n − k` originals are now in front of them. **Rotate** them to the back by
   dequeuing and re-enqueuing each one, which restores the intended order.

Phase 3 is the part people miss. Draw it out.

### Dry run — `q = [1,2,3,4,5]`, `k = 3`

| phase | operation | stack | queue (front → back) |
|---|---|---|---|
| start | | `[]` | `1,2,3,4,5` |
| 1 | pop 1,2,3 to stack | `[1,2,3]` | `4,5` |
| 2 | push back 3,2,1 | `[]` | `4,5,3,2,1` |
| 3 | rotate `n−k = 2` elements | | `5,3,2,1,4` → `3,2,1,4,5` |

→ `[3,2,1,4,5]` ✓

### The code

```python
class Solution:
    def modifyQueue(self, q, k):
        stack = []
        n = len(q) - k                     # (1)

        while k:                           # (2)
            stack.append(q.popleft())
            k -= 1

        while stack:                       # (3)
            q.append(stack.pop())

        while n:                           # (4)
            q.append(q.popleft())
            n -= 1

        return q
```

**(1)** `n` is computed **before** `k` is consumed by the loop at (2) — the count of elements
that must be rotated. Computing it after would give the wrong number, since `k` is destroyed.
(This is why `k` being mutated is a little dangerous; a `for _ in range(k)` loop would be safer.)

**(2)** `while k:` relies on `0` being falsy. Dequeue k elements onto the stack. Idiomatic,
though it does destroy the parameter.

**(3)** `stack.pop()` returns them in **reverse** order — the reversal, for free, from LIFO.
They're appended to the back of the queue.

**(4)** The rotation. The `n` untouched elements are still in front; move each to the back so
the reversed block ends up first.

### Complexity
- **Time O(n)** — each element is moved a constant number of times (k go through the stack,
  n−k get rotated once).
- **Space O(k)** for the stack.

### Try next
[Reverse Linked List II (tomorrow)](https://leetcode.com/problems/reverse-linked-list-ii/) ·
[Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) ·
[Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) (monotonic **deque**)

---

## 8. Remove All Adjacent Duplicates In String `LC-1047`

**[LeetCode 1047 →](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/)** · Easy · Stack · *new*

### In one line
Repeatedly delete adjacent equal pairs until none remain.

```
"abbaca" → "ca"      ("abbaca" → "aaca" → "ca")
```

### Recognise it
"Repeatedly remove adjacent pairs", "collapse", "cancel out". Same shape as Valid Parentheses:
the incoming character interacts with **the most recent unresolved one**.

### Intuition
The naive approach rescans the string after every deletion — O(n²), and it's exactly what
your `33-Valid_Parenthese.py` does.

With a stack it's one pass: for each character, if it equals the top of the stack, they
cancel — pop and move on. Otherwise push it. What remains on the stack, bottom to top, is the
answer.

The reason this catches *cascading* deletions in one pass: after popping, the new top is
whatever was underneath, which is exactly the character that becomes newly adjacent. The
stack maintains that adjacency automatically.

### Dry run — `s = "abbaca"`

| char | stack top | action | stack |
|---|---|---|---|
| `a` | — | push | `[a]` |
| `b` | `a` | differ → push | `[a,b]` |
| `b` | `b` | **match → pop** | `[a]` |
| `a` | `a` | **match → pop** | `[]` ← the cascade, caught for free |
| `c` | — | push | `[c]` |
| `a` | `c` | differ → push | `[c,a]` |

→ `"ca"` ✓

### The code

```python
class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []

        for c in s:
            if stack and stack[-1] == c:      # (1)
                stack.pop()                   # (2)
            else:
                stack.append(c)               # (3)

        return "".join(stack)                 # (4)
```

**(1)** `stack and ...` guards the empty case before indexing — `stack[-1]` on `[]` raises
`IndexError`, and `and` short-circuits so it's never evaluated.

**(2)** Both characters vanish: the stacked one is popped and the current one is simply not
pushed. Two deletions, one `pop`.

**(3)** No match → this character waits for a possible future partner.

**(4)** `"".join(stack)` builds the string in **O(n)**. Do not use `result += c` in a loop —
Python strings are immutable, so every `+=` copies the whole string and the loop becomes
**O(n²)**. See [Python §5](./01-python-for-dsa.md). `join` is the idiom for building strings
from pieces, always.

### Complexity
- **Time O(n)** — one pass; each character is pushed at most once and popped at most once.
- **Space O(n)** — worst case (`"abcdef"`, no matches) everything is on the stack.

### Try next
[Remove All Adjacent Duplicates in String II](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/) (k in a row — push `(char, count)` pairs) ·
[Backspace String Compare](https://leetcode.com/problems/backspace-string-compare/) ·
[Make The String Great](https://leetcode.com/problems/make-the-string-great/)

---

## 9. Daily Temperatures `LC-739`

**[LeetCode 739 →](https://leetcode.com/problems/daily-temperatures/)** · Medium · **Monotonic stack** · *new*

> This is the pattern that was completely missing from your original 50. Learn it today.

### In one line
For each day, how many days until a **warmer** temperature? 0 if none.

```
[73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]
```

### Recognise it
"**Next greater** element", "next warmer day", "how long until…", "days until". Any question
of the form *"for each element, find the first later element that is bigger/smaller"* is a
monotonic stack.

### Intuition
Brute force: for each day, scan forward until you find something warmer — O(n²).

The monotonic-stack idea reverses the question. Instead of each day *searching* for its
answer, each day **provides** answers to everyone still waiting.

Keep a stack of days that haven't found a warmer day yet. Their temperatures are necessarily
**decreasing** — if a later day were warmer than an earlier one on the stack, the earlier one
would already have been resolved and popped.

When today arrives, it resolves every waiting day cooler than it. Pop them, and their answer
is `today − their_day`. Then today joins the stack to wait for its own resolution.

### Dry run — `[73,74,75,71,69,72,76,73]`

Stack holds **indices**; temperatures in it stay decreasing.

| i | temp | pop while `T[stack[-1]] < temp` | answers set | stack after |
|---|---|---|---|---|
| 0 | 73 | — | | `[0]` |
| 1 | 74 | pop 0 (73<74) | `res[0] = 1−0 = 1` | `[1]` |
| 2 | 75 | pop 1 (74<75) | `res[1] = 2−1 = 1` | `[2]` |
| 3 | 71 | 75<71? no | | `[2,3]` |
| 4 | 69 | 71<69? no | | `[2,3,4]` |
| 5 | 72 | pop 4 (69<72), pop 3 (71<72) | `res[4]=1`, `res[3]=2` | `[2,5]` |
| 6 | 76 | pop 5 (72<76), pop 2 (75<76) | `res[5]=1`, `res[2]=4` | `[6]` |
| 7 | 73 | 76<73? no | | `[6,7]` |

Left on the stack: 6 and 7 — never resolved, so `res[6] = res[7] = 0`, which the array's
initialisation already provides.

→ `[1,1,4,2,1,1,0,0]` ✓

### The code

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        res = [0] * len(temperatures)              # (1)
        stack = []                                 # (2)

        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:   # (3)
                j = stack.pop()                    # (4)
                res[j] = i - j                     # (5)
            stack.append(i)                        # (6)

        return res                                 # (7)
```

**(1)** Pre-filled with **0**, which is the answer for any day that never finds a warmer one.
Initialising to the "not found" value means you never write it explicitly — the days left on
the stack at the end are handled for free. That's a deliberate design choice, not laziness.

**(2)** **Indices, not temperatures.** We need `i - j`, a distance, which requires positions.
You can always get the temperature back with `temperatures[j]`; you cannot recover a position
from a temperature. **Store indices** is the rule for monotonic stacks.

**(3)** The engine of the pattern. `stack and ...` guards the empty case. `<` (strict) means
equal temperatures do **not** resolve each other — correct, since the problem says *warmer*.
Using `<=` here would be a wrong answer, and it's the most common slip.

**(4)–(5)** `j` is a day that has been waiting; today `i` is the first warmer day after it, so
its answer is the gap `i - j`.

**(6)** Today joins the queue of unresolved days. Because everything cooler was just popped,
the stack stays decreasing — the invariant is maintained automatically.

**(7)** Anything still on the stack keeps its initial 0.

### Complexity
- **Time O(n)** — and this is the part to be able to defend. The inner `while` looks like it
  makes this quadratic, but **each index is pushed exactly once and popped at most once**.
  Total pops across the whole run ≤ n. So the loop body does O(n) work in aggregate, not
  O(n) per iteration. Same amortised argument as the sliding window.
- **Space O(n)** — a strictly decreasing input (`[5,4,3,2,1]`) puts every index on the stack.

### The general template
```python
# "next greater to the right"  ->  iterate forward, pop while stack top is SMALLER
# "next smaller to the right"  ->  iterate forward, pop while stack top is LARGER
# "previous greater to the left" -> iterate BACKWARD, or read the stack before pushing
```
Only the comparison and the direction change.

### Try next
[Next Greater Element I (next)](https://leetcode.com/problems/next-greater-element-i/) ·
[Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) (circular) ·
[Online Stock Span](https://leetcode.com/problems/online-stock-span/) ·
[Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) (hard, same pattern) ·
[Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)

---

## 10. Next Greater Element I `LC-496`

**[LeetCode 496 →](https://leetcode.com/problems/next-greater-element-i/)** · Easy · Monotonic stack + hash map · *new*

### In one line
For each value in `nums1` (a subset of `nums2`), find the next greater element to its right
**in `nums2`**. −1 if none.

```
nums1 = [4,1,2], nums2 = [1,3,4,2] → [-1,3,-1]
```

### Recognise it
Yesterday's monotonic stack, plus Day 1's hash map to bridge two arrays. Another
two-easy-patterns-stacked Medium… filed as Easy.

### Intuition
Two steps:

1. Run the monotonic stack over **`nums2`** to compute the next greater element for every
   value, storing results in a dict `{value: next_greater}`.
2. Look up each element of `nums1`. O(1) each, defaulting to −1.

The dict is what lets you answer for `nums1` without re-scanning `nums2` for each query. The
problem guarantees all values are **distinct**, which is what makes a value-keyed dict safe
here (with duplicates you'd need indices).

### Dry run — `nums2 = [1,3,4,2]`

| x | pop while `stack[-1] < x` | dict entries added | stack |
|---|---|---|---|
| 1 | — | | `[1]` |
| 3 | pop 1 | `{1: 3}` | `[3]` |
| 4 | pop 3 | `{1:3, 3:4}` | `[4]` |
| 2 | 4 < 2? no | | `[4,2]` |

Left over: `4`, `2` → no next greater → −1 each.

Then `nums1 = [4,1,2]` → `[-1, 3, -1]` ✓

### The code

```python
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        next_greater = {}                          # (1)
        stack = []                                 # (2)

        for x in nums2:
            while stack and stack[-1] < x:         # (3)
                next_greater[stack.pop()] = x      # (4)
            stack.append(x)

        return [next_greater.get(x, -1) for x in nums1]   # (5)
```

**(1)** `value → next greater value`. Only elements that *have* an answer get an entry;
absence means −1.

**(2)** Here the stack holds **values**, not indices — because the answer is a *value*, not a
distance, and the problem promises distinct values. Contrast with Daily Temperatures, where
`i - j` forced indices. **Pick based on what the answer needs.**

**(3)** Same engine. Everything on the stack smaller than `x` has just found its next greater.

**(4)** `stack.pop()` is evaluated first and used as the dict key. Compact, but
`j = stack.pop()` then `next_greater[j] = x` is easier to read under pressure.

**(5)** `dict.get(x, -1)` returns −1 for a missing key instead of raising `KeyError` — exactly
the "no next greater" case. This is the same `.get(key, default)` idiom as Day 1's counting.

### Complexity
- **Time O(n + m)** — one pass over `nums2` (each element pushed and popped at most once) plus
  one pass over `nums1` with O(1) lookups. Brute force is O(n·m).
- **Space O(n)** for the dict and stack.

### Try next
[Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) — circular array; the trick is to loop over the array **twice** using `i % n` ·
[Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) ·
[Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/)

---

## Recall drill

1. Why is `list.pop(0)` wrong for a queue, and what is the actual cost of using it in a BFS?
2. In Valid Parentheses, why must `not stack` be checked **before** `stack.pop() != pairs[c]`?
3. In Min Stack, why push to `minStack` even when the value isn't a new minimum?
4. A monotonic stack has a `while` loop nested inside a `for` loop. Why is it O(n), not O(n²)?
5. In Daily Temperatures, why store indices on the stack rather than temperatures?

<details>
<summary>Answers</summary>

1. A list is an array; removing the front shifts all n−1 remaining elements — **O(n)** per
   call. Inside a BFS that dequeues n times, the traversal becomes **O(n²)** instead of O(n).
   Use `collections.deque` and `popleft()`, which is O(1).
2. Because `stack.pop()` on an empty list raises `IndexError`. Python's `or` short-circuits:
   if `not stack` is `True`, the right side is never evaluated. Reverse the order and `")("`
   crashes instead of returning `False`.
3. To keep the two stacks at **identical depth**, so `pop` can blindly pop both with no
   bookkeeping. That invariant is worth 2× memory — the "optimised" version that only pushes
   new minima has to track *when* to pop and is a far richer source of bugs.
4. Because each element is pushed **exactly once** and popped **at most once**. The total
   number of pops across the entire run is bounded by n, so the aggregate work is O(n). The
   right question is never "how many inner iterations per outer iteration" but "how much work
   in total".
5. Because the answer is a **distance**, `i - j`, which needs positions. You can always
   recover a temperature from an index (`temperatures[j]`), but never an index from a
   temperature. In Next Greater Element I the answer is a *value*, so values on the stack are
   fine there — pick based on what the answer needs.

</details>

---

**Tomorrow:** [Day 5 — Linked Lists](./day-5-linked-lists.md). Seven of your own solutions
plus three new ones. Two techniques carry the whole topic: **fast & slow pointers** and the
**dummy node**. You'll also finally write `29-Reversed_ll.py`, which was empty in your repo.

**Warm-up:** re-solve **Valid Parentheses** (the stack version, not `replace`) and
**Daily Temperatures** from a blank screen.
