# Python for DSA — Why Each Piece of Syntax

You asked *why* each piece of syntax is used. This page is the answer, gathered in one
place so the day files can point here instead of repeating themselves. Skim it now; return
whenever an annotation says "see the Python reference".

Every claim about cost here is what makes the difference between an O(n) solution and an
O(n²) one that looks identical.

---

## 1. `set` vs `list` — the single most important choice

```python
if num in seen:
```

What `seen` is decides your whole complexity:

| Type | `x in seen` | Why |
|---|---|---|
| `list` | **O(n)** | Scans every element until it finds a match |
| `set` | **O(1)** average | Hashes `x` and jumps straight to the bucket |
| `dict` | **O(1)** average | Same mechanism; a set is a dict with no values |

Putting `in` on a list inside a loop silently gives you O(n²):

```python
seen = []                    # O(n^2) overall  <-- the bug
seen = set()                 # O(n) overall    <-- correct
```

This one substitution is the entire trick behind Contains Duplicate, Two Sum, Valid
Anagram, and Number of Islands' `visit` set. When you see "have I seen this before?",
reach for a set.

**Cost:** a set of n ints is roughly 32–60 bytes per element. You are buying time with
memory. That is the trade, and stating it out loud is half of a complexity answer.

**Requirement:** elements must be *hashable* — immutable. `int`, `str`, `tuple` yes;
`list`, `dict`, `set` no. This is why grid coordinates go into a set as `(r, c)` tuples,
never `[r, c]`:

```python
visit.add((r, c))     # works: tuple is hashable
visit.add([r, c])     # TypeError: unhashable type: 'list'
```

---

## 2. `dict` — a set that remembers *where*

Use a set when you only need "does it exist". Use a dict the moment you need "…and where /
how many":

```python
numMap[nums[i]] = i          # 04-Two_sum: value -> index, so we can return the index
```

Three ways to count, in increasing order of idiomatic:

```python
# 1. manual
counts = {}
for c in s:
    counts[c] = counts.get(c, 0) + 1    # .get(key, default) avoids KeyError

# 2. defaultdict -- the default is created on first touch
from collections import defaultdict
counts = defaultdict(int)               # missing key -> 0
for c in s:
    counts[c] += 1

# 3. Counter -- purpose-built
from collections import Counter
counts = Counter(s)                     # {'a': 2, 'b': 1}
```

`Counter` also gives you `counts.most_common(k)`, which is a ready-made "top k" — worth
knowing, though on Day 3 you'll write the heap version, because that is what gets asked.

`defaultdict(list)` is the one you want for grouping:

```python
groups = defaultdict(list)
groups[key].append(word)      # no "if key not in groups" needed
```

---

## 3. `collections.deque` vs `list` — the BFS trap

```python
q = []                        # WRONG for a queue
q.pop(0)                      # O(n): every remaining element shifts left one slot

from collections import deque
q = deque()                   # RIGHT
q.popleft()                   # O(1)
```

A list is an array. Removing the front means moving all n−1 remaining elements. Inside a
BFS that runs n times, so your O(n) traversal quietly becomes **O(n²)**.

`deque` is a doubly linked list of blocks; both ends are O(1).

| Operation | `list` | `deque` |
|---|---|---|
| `append` (right) | O(1) amortised | O(1) |
| `pop()` (right) | O(1) | O(1) |
| `pop(0)` / `popleft()` | **O(n)** | **O(1)** |
| `q[i]` random access | O(1) | **O(n)** |

**Rule:** stack → `list` (both ends of the action are the right end). Queue → `deque`.

Your `39-avg_level_bt.py` and `42-Level_order_traversal_bt.py` use `q.pop(0)`. They give
correct answers and they pass on LeetCode, but they are O(n²). Day 6 shows the fix.

---

## 4. `//` vs `/` — integer division, and the negative-number trap

```python
n * (n + 1) // 2      # int
n * (n + 1) / 2       # float -- 5050.0, not 5050
```

`/` **always** returns a float in Python 3. That matters for:

- **Indices.** `nums[len(nums) / 2]` → `TypeError: list indices must be integers`.
  Always `//` for a midpoint: `mid = (lo + hi) // 2`.
- **Precision.** Floats lose exactness above 2⁵³. With LeetCode's large constraints,
  a float can return the wrong integer.

**The trap:** `//` floors *toward negative infinity*, which is not truncation:

```python
 7 //  2  ==  3        int( 7 / 2) ==  3     # agree
-7 //  2  == -4        int(-7 / 2) == -3     # DISAGREE
```

Evaluate RPN (`34-*.py`) requires truncation toward zero, so it must use `int(a / b)`, not
`a // b`. This is a real LeetCode wrong-answer, not a nitpick.

---

## 5. Slicing — and the copy you didn't notice

```python
nums[a:b]       # elements a .. b-1        -- a NEW list, O(b-a) time and space
nums[:i]        # everything before i
nums[i+1:]      # everything after i
nums[::-1]      # reversed COPY            -- O(n) space
nums[:]         # full shallow copy
```

Every slice **allocates**. Inside a recursion this is easy to miss:

```python
backtrack(nums[:i] + nums[i+1:], path + [nums[i]])
```

That line makes two new lists per call. It is why the clean permutations solution is O(n!·n)
and not O(n!) — and it is the honest reason `path + [x]` is used instead of `path.append(x)`
(next section).

Reversing in place, when you own the list, is free of that cost:

```python
nums.reverse()        # in place, O(1) extra space, returns None
rev = nums[::-1]      # new list, O(n) extra space
rev = reversed(nums)  # lazy iterator, O(1) space -- but you can only walk it once
```

---

## 6. `path + [x]` vs `path.append(x)` — the backtracking decision

This one bites everybody. Lists are **mutable and passed by reference**.

```python
# Version A -- copy. Simple, slightly slower.
def backtrack(start, path):
    result.append(path)                       # safe: nothing will mutate this list later
    for i in range(start, len(nums)):
        backtrack(i + 1, path + [nums[i]])    # `+` builds a NEW list

# Version B -- mutate and undo. Faster, but you MUST copy on save.
def backtrack(start, path):
    result.append(path[:])                    # the [:] is mandatory
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()                            # the "backtrack" step -- undo the choice
```

In Version B, forgetting `path[:]` is the classic bug: you append *the same list object*
every time, and at the end `result` is a list of N identical empty lists, because every
`append`/`pop` mutated the one object you stored.

Your `22-Subsets.py` uses Version A; `23-Combinations.py` uses Version B (note its
`curr[:]`). Both are in this repo — compare them side by side on Day 7.

---

## 7. `float('inf')` — the sentinel

```python
min_diff = float("inf")
for ...:
    min_diff = min(min_diff, candidate)
```

You need an initial value that **any** real candidate beats. `0` is wrong (negative
differences would never win); the first element works but needs a special case for an empty
input. `float('inf')` compares greater than every number, so the first candidate always
replaces it.

- Looking for a **minimum** → start at `float('inf')`
- Looking for a **maximum** → start at `float('-inf')`

The alternative you'll see in `14-Minimum_size_subarray_sum.py` is an impossible-value
sentinel: `min_len = len(nums) + 1`, then "if it never changed, return 0". Both are fine;
`inf` reads better.

---

## 8. `enumerate` and `zip`

```python
for i in range(len(nums)):     # works
    print(i, nums[i])

for i, num in enumerate(nums): # better: no indexing, no len(), harder to typo
    print(i, num)
```

`enumerate(xs, start=1)` if the problem is 1-indexed.

```python
for a, b in zip(xs, xs[1:]):   # every adjacent pair
    ...
```

`zip` stops at the shorter input, which is exactly what you want for adjacent-pair scans.

---

## 9. `sorted()` vs `.sort()`, and `key=`

```python
arr.sort()               # in place, returns None  <-- `x = arr.sort()` gives you None
new = sorted(arr)        # returns a new list, leaves arr alone
```

`arr = arr.sort()` is a very common bug: `arr` becomes `None`.

Both are **Timsort: O(n log n) time, O(n) space**. Sorting is not free — but it is often
worth it, because turning O(n²) into O(n log n) + O(n) is a big win.

```python
sorted(points, key=lambda p: p[0])          # by first coordinate
sorted(words, key=len)                      # by length
sorted(items, key=lambda x: (-x[1], x[0]))  # count DESC, then name ASC
```

The `(-count, name)` tuple trick is how you sort by two keys in opposite directions without
sorting twice.

---

## 10. `heapq` — the priority queue (Day 3)

Python has no `PriorityQueue` class you'd want; you use `heapq` on a plain list.

```python
import heapq

h = []
heapq.heappush(h, 5)      # O(log n)
smallest = heapq.heappop(h)   # O(log n) -- ALWAYS the minimum
h[0]                      # peek at the minimum, O(1)

heapq.heapify(nums)       # turn an existing list into a heap IN PLACE, O(n) -- not O(n log n)
heapq.heappushpop(h, x)   # push then pop, one operation, cheaper than doing both
```

**`heapq` is a min-heap only.** For a max-heap, negate on the way in and out:

```python
heapq.heappush(h, -val)
largest = -heapq.heappop(h)
```

For "kth largest", the trick is a **min-heap of size k**: the smallest thing in the heap is
the kth largest overall, and you evict whenever the heap grows past k. That is O(n log k),
better than sorting's O(n log n) when k is small.

---

## 11. Truthiness — why `if not root:` works

```python
if not root:          # None is falsy
if not nums:          # [] is falsy
if not s:             # "" is falsy
```

Falsy: `None`, `False`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`.

**The trap:** `0` is falsy. On a tree of node values this is fine (`root` is a node object,
never `0`), but here it bites:

```python
if not node.val:      # WRONG: true when node.val == 0
if node.val is None:  # right
```

Use `is None` when zero is a legitimate value. Use `if not x` when you mean "empty or
absent".

`or` returns the first truthy operand, not a boolean — which is why `47-LCA.py` ends with
`return l or r`: "whichever side found something, or None if neither did."

---

## 12. Multiple assignment and swapping

```python
l, r = 0, len(nums) - 1
slow = fast = head                # both names -> the SAME object
root.left, root.right = root.right, root.left     # swap, no temp variable
```

The right-hand side is fully evaluated *before* any assignment, which is what makes the
swap work — and what makes this linked-list idiom safe:

```python
curr.next, prev, curr = prev, curr, curr.next     # one-line list reversal
```

Correct, but write the four-line version in an interview. Clever is not the goal.

`slow = fast = head` binds two names to one object. For immutable ints that is harmless;
for a mutable object, mutating through one name is visible through the other.

---

## 13. Bitwise operators (Day 1)

```python
a ^ b        # XOR: 1 where the bits differ
a & b        # AND
a | b        # OR
i >> 1       # right shift = i // 2
i << 1       # left shift  = i * 2
i & 1        # last bit: 1 if odd, 0 if even
```

Two XOR properties do all the work in `15-Single_number.py`:

- `x ^ x == 0` — a value cancels itself
- `x ^ 0 == x` — zero is the identity

XOR the whole array and every duplicated value annihilates, leaving the single one. O(n)
time, **O(1) space** — that is the point; a hash set would also be O(n) time but O(n) space.

And `19-Counting_bits.py`'s recurrence:

```python
ans[i] = ans[i >> 1] + (i & 1)
```

"Bits in i = bits in (i without its last bit) + that last bit." Note the parentheses:
`+` binds tighter than `&` in Python, so `ans[i>>1] + i & 1` would parse as
`(ans[i>>1] + i) & 1` — wrong. **When you mix bitwise and arithmetic, parenthesise.**

---

## 14. The mutable default argument

```python
def backtrack(first=1, curr=[]):     # DANGEROUS
```

The default `[]` is created **once**, when the function is defined — not per call. If the
function ever mutates it, the mutation persists into the next call.

`23-Combinations.py` uses this signature. It is safe *there* because every `curr.append` is
matched by a `curr.pop`, so the list is empty again by the time the call returns. But it is
a fragile thing to rely on. The standard fix:

```python
def backtrack(first=1, curr=None):
    if curr is None:
        curr = []
```

---

## 15. Type hints — decoration, not enforcement

```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
```

Python does not check these at runtime. They exist for readers and IDEs. LeetCode
pre-imports `List` and `Optional` from `typing`, which is why these files fail locally with
`NameError: name 'List' is not defined` — and why `guide/verify.py` injects them.

Python 3.9+ lets you write `list[int]` and `int | None` without any import.

---

## Quick reference

| You want | Use | Cost |
|---|---|---|
| "Seen this before?" | `set` | O(1) add / lookup |
| "Seen it, and where/how many?" | `dict` / `Counter` | O(1) |
| Group things by a key | `defaultdict(list)` | O(1) per item |
| Stack (LIFO) | `list` + `append`/`pop` | O(1) |
| Queue (FIFO) | `deque` + `append`/`popleft` | O(1) |
| Smallest/largest k | `heapq`, size-k heap | O(n log k) |
| Ordered scan of pairs | `sort()` then two pointers | O(n log n) |
| Midpoint of a range | `(lo + hi) // 2` | — |
| Sentinel for a minimum | `float('inf')` | — |
| Grid cell as a key | `(r, c)` tuple | hashable |
