# Day 7 — BST, Graphs, Backtracking & DP

> **Today's big idea, and the most valuable connection in this guide: backtracking is DFS on
> a tree that doesn't exist.** You spent yesterday writing tree recursion. Today the same
> recursion explores a tree of *decisions* you generate as you go. Once you see that, subsets,
> permutations, combinations, word search and N-Queens are all one template.

**Warm-up (10 min, blank screen):** re-solve Maximum Depth and Level Order Traversal.

All ten problems today are your own. This is consolidation day: four patterns, each building
on something you already have.

---

## Pattern primer

### A. BST — a tree with an ordering guarantee

```
For EVERY node:   all values in the left subtree  <  node.val  <  all values in the right subtree
```

That single invariant means you never have to search both sides. Compare with the current node
and go one way — **binary search on a tree**. Day 3's `lo`/`hi` narrowing, in pointer form.

```python
def search(node, val):
    if not node or node.val == val:
        return node
    return search(node.right, val) if node.val < val else search(node.left, val)
```
**O(h)** — O(log n) balanced, O(n) if the tree has degenerated into a chain.

And the fact worth banking: **in-order traversal of a BST yields sorted output.**

### B. Grid BFS/DFS — connected components

```python
from collections import deque
rows, cols = len(grid), len(grid[0])
visit = set()

def bfs(r, c):
    q = deque([(r, c)])
    visit.add((r, c))                          # mark on ENQUEUE, not on dequeue
    while q:
        row, col = q.popleft()
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):     # the 4 directions
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols \
               and (nr, nc) not in visit and grid[nr][nc] == "1":
                visit.add((nr, nc))
                q.append((nr, nc))
```

**Mark on enqueue.** If you mark when *dequeuing*, a cell can be added to the queue several
times before it's first processed — you'd revisit, and on a large grid you'd blow up.

Coordinates go into the set as **tuples** `(r, c)` because lists are unhashable — see
[Python §1](./01-python-for-dsa.md).

### C. Backtracking — DFS on an implicit tree

```python
def backtrack(start, path):
    if is_complete(path):
        result.append(path[:])         # the [:] COPY is mandatory when you mutate path
        return
    for choice in available(start):
        path.append(choice)            # CHOOSE
        backtrack(start + 1, path)     # EXPLORE
        path.pop()                     # UN-CHOOSE   <-- this is "backtracking"
```

Compare it with yesterday's tree DFS. Identical shape. The only difference: a tree DFS walks
children that already exist (`node.left`, `node.right`); backtracking walks children it
*generates* (`for choice in available(...)`). The "tree" is the space of partial solutions, and
it's never built in memory — only the current root-to-node path exists at any moment.

**The two styles, and when to use which:**

```python
# MUTATE + UNDO -- faster, but the [:] copy on save is REQUIRED
path.append(x);  backtrack(...);  path.pop()
result.append(path[:])

# COPY ON DESCENT -- simpler, slightly slower, no undo needed
backtrack(..., path + [x])
result.append(path)
```
Your `23-Combinations.py` uses the first; `22-Subsets.py` uses the second. Both are in this
repo — compare them directly today.

### D. Dynamic programming — remember what you already computed

```python
dp = [base] * (n + 1)        # dp[i] = the answer for input size i
dp[0] = known
for i in range(1, n + 1):
    dp[i] = f(dp[i-1], dp[i-2], ...)     # the recurrence
return dp[n]
```

DP applies when a problem has **overlapping subproblems** — the naive recursion computes the
same thing over and over. Storing each answer once turns exponential into linear.

**The code is never the hard part. Writing down the recurrence is.** Ask: *"to solve size i,
what smaller answers do I need?"*

Copy all four templates out by hand.

---

## 1. Search in a Binary Search Tree

**[LeetCode 700 →](https://leetcode.com/problems/search-in-a-binary-search-tree/)** · Easy · BST navigation · [`48-Search_bt.py`](../48-Search_bt.py)

### In one line
Find the node with the given value; return its subtree, or `None`.

### Recognise it
The BST invariant, used for the first time. Day 3's binary search with pointers instead of
indices.

### Intuition
At each node, one comparison eliminates an **entire subtree**. If `val` is bigger than the
current node, everything to the left is bigger-than-impossible — it's all smaller — so discard
it and go right. Same halving as binary search on an array.

### Dry run — tree `[4,2,7,1,3]`, `val = 2`

| node | comparison | direction |
|---|---|---|
| 4 | `4 > 2` | go **left** |
| 2 | `2 == 2` | **found** → return the subtree rooted at 2 |

Two comparisons. A linear scan would need up to 5.

### The code

```python
class Solution(object):
    def searchBST(self, root, val):
        if not root:
            return root                              # (1)

        if root.val == val:
            return root                              # (2)
        if root.val < val:
            return self.searchBST(root.right,val)    # (3)
        else:
            return self.searchBST(root.left,val)     # (4)
```

**(1)** Ran off the bottom → not present. `return root` returns `None`, which is what the
problem asks for. (Returning the variable rather than the literal keeps the return type
uniform.)

**(2)** Found. The problem wants the whole **subtree** rooted here, not just the value.

**(3)** Current node is too small → the target must be in the larger half → go right.

**(4)** Otherwise go left.

Note the `self.` on both recursive calls — the thing whose absence broke
[`47-LCA.py`](../47-LCA.py). See [bugs-found.md §5](./bugs-found.md).

### The iterative version — O(1) space
```python
while root and root.val != val:
    root = root.left if val < root.val else root.right
return root
```
Two lines, no call stack. For BST navigation the iterative form is strictly better; there's
nothing to unwind on the way back up.

### Complexity
- **Time O(h)** — one node per level. **O(log n)** for a balanced tree, **O(n)** for a
  degenerate one (inserting `1,2,3,4,5` in order builds a chain).
- **Space O(h)** recursive, **O(1)** iterative.

### Try next
[Insert into a BST (next)](https://leetcode.com/problems/insert-into-a-binary-search-tree/) ·
[Closest Binary Search Tree Value](https://leetcode.com/problems/closest-binary-search-tree-value/) ·
[Range Sum of BST](https://leetcode.com/problems/range-sum-of-bst/)

---

## 2. Insert into a Binary Search Tree

**[LeetCode 701 →](https://leetcode.com/problems/insert-into-a-binary-search-tree/)** · Medium · BST navigation + reassignment · [`49-Insert_into_BST.py`](../49-Insert_into_BST.py)

### In one line
Insert a value, keeping it a valid BST. Any valid result is accepted.

### Recognise it
Problem 1, but you **build** on arrival instead of reading. Introduces the
`node.child = recurse(node.child)` idiom, which is how you modify a tree structure through
recursion.

### Intuition
Navigate exactly as in a search. When you fall off the bottom — the place where the value
*would* have been — that empty slot is where the new node goes.

The mechanism: every recursive call **returns the (possibly new) subtree**, and the parent
**reassigns** its child pointer to whatever comes back. Along the existing path nothing
changes (the same node is returned), but at the bottom a brand-new node is returned and gets
attached.

### Dry run — tree `[4,2,7,1,3]`, insert 5

| call | comparison | action |
|---|---|---|
| `insert(4, 5)` | `5 > 4` | `root.right = insert(7, 5)` |
| `insert(7, 5)` | `5 < 7` | `root.left = insert(None, 5)` |
| `insert(None, 5)` | — | **return `TreeNode(5)`** |
| back in `insert(7,…)` | | `7.left = node(5)`; return 7 |
| back in `insert(4,…)` | | `4.right = 7` (unchanged); return 4 |

### The code

```python
class Solution(object):
    def insertIntoBST(self, root, val):
        if not root:
            return TreeNode(val)                          # (1)

        if val < root.val:
            root.left = self.insertIntoBST(root.left,val)   # (2)
        else:
            root.right = self.insertIntoBST(root.right,val) # (3)

        return root                                       # (4)
```

**(1)** **The base case does the work.** Reaching `None` means we've found the empty slot;
create the node and return it. This also handles inserting into an entirely empty tree — the
first call returns the new root with no special case.

**(2)–(3)** **`root.left = self.insert(...)` — assign the result back.** This is the idiom to
internalise. For existing nodes the call returns the same object, so the assignment is a
harmless no-op; at the bottom it's what actually attaches the new node.

Without the assignment, the new node is created, returned, and **thrown away**. That's the
classic bug, and it produces an unchanged tree with no error.

**(4)** Return this subtree unchanged so the parent's assignment at (2)/(3) works.

### Complexity
- **Time O(h)** — one node per level. O(log n) balanced, O(n) degenerate.
- **Space O(h)** for the stack; the iterative version is O(1).

### Try next
[Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/) — much harder; deleting a node with two children needs its in-order successor ·
[Search in a BST](https://leetcode.com/problems/search-in-a-binary-search-tree/) ·
[Convert Sorted Array to BST (next)](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/)

---

## 3. Convert Sorted Array to Binary Search Tree

**[LeetCode 108 →](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/)** · Easy · Divide and conquer · [`50-convert_sorted_array_BST.py`](../50-convert_sorted_array_BST.py)

> ⚠️ **This file had two bugs** — `recursive(start, end)` was called with three arguments
> (`TypeError`), and there was **no base case**, so it recursed forever. Fixed; see
> [bugs-found.md §6](./bugs-found.md).

### In one line
Build a **height-balanced** BST from a sorted array.

```
[-10,-3,0,5,9] →       0
                     /   \
                   -3     9
                   /     /
                 -10    5
```

### Recognise it
"Sorted array" + "**balanced** BST". The word *balanced* is the whole instruction: it tells you
which element to pick as the root.

### Intuition
Why the middle? Because a BST puts everything smaller on the left and everything larger on the
right. Choosing the middle splits the array into two halves of (nearly) equal size, so the two
subtrees have equal height. Recurse.

Choosing `nums[0]` as the root would put all n−1 remaining elements on the right and build a
chain of height n — a valid BST, but not a balanced one.

This is the same halving logic as binary search, used to *construct* rather than to search.

### Dry run — `[-10,-3,0,5,9]`

| call | range | mid | value | children |
|---|---|---|---|---|
| `rec(0,4)` | all | 2 | **0** (root) | `rec(0,1)`, `rec(3,4)` |
| `rec(0,1)` | `[-10,-3]` | 0 | **−10** | `rec(0,-1)`→None, `rec(1,1)` |
| `rec(1,1)` | `[-3]` | 1 | **−3** | both empty |
| `rec(3,4)` | `[5,9]` | 3 | **5** | `rec(3,2)`→None, `rec(4,4)` |
| `rec(4,4)` | `[9]` | 4 | **9** | both empty |

Height 3 for 5 nodes — balanced ✓

*(Note the tree drawn above places −3 and 9 as children of 0, which is a different but equally
valid balanced BST — the problem accepts any.)*

### The code (fixed)

```python
class Solution(object):
    def sortedArrayToBST(self, nums):
        def recursive(start, end):
            if start > end:
                return None                       # (1)

            mid = (start + end) // 2              # (2)
            node = TreeNode(nums[mid])            # (3)

            node.left  = recursive(start, mid - 1)    # (4)
            node.right = recursive(mid + 1, end)
            return node

        return recursive(0, len(nums) - 1)        # (5)
```

**(1)** ⚠️ **This was missing entirely** — the original had no base case, so the recursion never
terminated. `start > end` means the range is empty, so that child is `None`.

**Write the base case before the recursive call. Every time.** That habit alone prevents this
whole class of bug.

**(2)** `//` — indices must be integers. `(start + end) / 2` gives a float and
`nums[2.0]` raises `TypeError`.

**(3)** The middle element becomes the root of this subtree — the balancing decision.

**(4)** ⚠️ **These were `recursive(nums, 0, mid-1)`** — three arguments to a two-parameter
function, *and* the `0` restarted the left bound from the beginning of the array instead of
narrowing it. `nums` doesn't need passing: the inner function **closes over** it from the
enclosing scope. That's the entire reason to define the helper inside the method.

The ranges are **inclusive**, and `mid-1` / `mid+1` exclude the element just used — which is
what guarantees termination and that no element appears twice.

**(5)** Start with the whole array. `len(nums) - 1` as an inclusive end; an empty input gives
`recursive(0, -1)` → `None`, handled by (1) with no special case.

### Complexity
- **Time O(n)** — one node created per element, O(1) work each.
- **Space O(log n)** — the recursion stack, which is the height of the *balanced* tree we're
  building. (Plus O(n) for the output tree.)

### Try next
[Convert Sorted List to BST](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/) — the linked-list version; you can't index, so find the middle with fast/slow (Day 5!) ·
[Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) ·
[Maximum Binary Tree](https://leetcode.com/problems/maximum-binary-tree/)

---

## 4. Number of Islands

**[LeetCode 200 →](https://leetcode.com/problems/number-of-islands/)** · Medium · Grid BFS · [`08-Number_of_Island.py`](../08-Number_of_Island.py)

### In one line
Count connected groups of `'1'`s in a grid (4-directionally connected).

```
11110
11010    → 1
11000
00000
```

### Recognise it
"Islands", "connected regions", "groups", "flood fill". This is **connected components** —
your only graph problem in the original 50, and the template for a large family.

### Intuition
Scan every cell. When you find an unvisited `'1'`, you've discovered a new island — increment
the count, then **flood the entire island** with BFS so none of its cells starts another count.

The outer loop finds islands; the BFS consumes them. Each cell is visited by the flood exactly
once, so the total cost is one pass over the grid regardless of how the land is shaped.

### Dry run — the grid above

| outer scan | cell | action |
|---|---|---|
| (0,0) | `'1'`, unvisited | **count = 1**, BFS floods all 9 connected land cells |
| (0,1)…(2,1) | `'1'` but visited | skip |
| (1,3) | `'1'`… | wait — it was reached by the flood from (0,0)? |

Trace (1,3): from (0,3) — is (0,3) land? Row 0 is `11110`, so (0,3)=`'1'` ✓, and it connects
to (1,3)=`'1'`. So yes, the flood reaches it. Everything is one island → **1** ✓

### The code

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid: return 0

        rows = len(grid)
        cols = len(grid[0])                       # (1)

        count = 0
        visit = set()                             # (2)

        def bfs(r,c):
            q = deque()                           # (3)
            q.append((r,c))
            visit.add((r,c))                      # (4)
            while q:
                row,col = q.popleft()             # (5)
                direction = [[1,0],[-1,0],[0,1],[0,-1]]     # (6)
                for dr,dc in direction:
                    r = row + dr                  # (7)
                    c = col + dc
                    if(r in range(rows) and       # (8)
                       c in range(cols) and
                        (r,c) not in visit and
                        grid[r][c] == "1"):
                        q.append((r,c))
                        visit.add((r,c))          # (4 again)

        for r in range(rows):                     # (9)
            for c in range(cols):
                if grid[r][c] == "1" and((r,c) not in visit):
                    bfs(r,c)
                    count += 1
        return count
```

**(1)** `len(grid[0])` assumes at least one row — guarded by the `if not grid` above.

**(2)** A **set of `(r, c)` tuples**. Tuples because they're hashable; a `[r, c]` list would
raise `TypeError: unhashable type`. See [Python §1](./01-python-for-dsa.md).

**(3)** ⚠️ `deque` is used with **no import** — LeetCode pre-imports it, but this file won't run
locally without `from collections import deque`. (That's why
[`guide/verify.py`](./verify.py) injects it.)

**(4)** **Mark on enqueue, not on dequeue.** If you only marked when dequeuing, a cell with two
land neighbours could be added to the queue twice before it's processed once — duplicated work
that compounds badly on large grids. Marking at insertion time makes each cell enter the queue
exactly once.

**(5)** `popleft()` — O(1). This is what makes it a BFS rather than a DFS; swapping to `pop()`
would make it a DFS and still be correct here, since we only want connectivity, not distance.

**(6)** The four direction offsets: down, up, right, left. Rebuilding this list on every
dequeue is a small waste — hoist it out of the function, or use a tuple constant.

**(7)** ⚠️ **`r` and `c` shadow the function's own parameters.** It works — `row` and `col` were
already copied out at (5), so the parameters aren't needed again — but it's confusing to read
and one edit away from a real bug. `nr, nc` (new row, new col) is the conventional naming.

**(8)** Four conditions, all necessary: in bounds vertically, in bounds horizontally, not
already seen, and actually land.

`r in range(rows)` is correct and readable but constructs a range object each time;
`0 <= r < rows` is the faster, more idiomatic form.

**(9)** The outer scan. Every land cell is either the seed of a new island or already flooded
by a previous one.

### Complexity
- **Time O(rows × cols)** — every cell is examined by the outer loop once, and enqueued by BFS
  at most once (thanks to (4)).
- **Space O(rows × cols)** for the visited set, plus up to O(min(rows,cols)) for the queue in
  the worst case.

### The space optimisation
Instead of a visited set, overwrite visited land with `'0'`:
```python
grid[r][c] = "0"        # sink the island as you go
```
**O(1) extra space**, at the cost of destroying the input. Interviewers ask about this trade;
mention both.

### Try next
[Max Area of Island](https://leetcode.com/problems/max-area-of-island/) — same flood, return the size ·
[Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) — multi-source BFS, where the *levels* matter ·
[Flood Fill](https://leetcode.com/problems/flood-fill/) ·
[Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) ·
[Course Schedule](https://leetcode.com/problems/course-schedule/) — the graph version (topological sort)

---

## 5. Letter Case Permutation

**[LeetCode 784 →](https://leetcode.com/problems/letter-case-permutation/)** · Medium · Iterative expansion · [`21-letterCase.py`](../21-letterCase.py)

### In one line
Generate every string obtainable by changing the case of each letter. Digits are unchanged.

```
"a1b2" → ["a1b2","a1B2","A1b2","A1B2"]
```

### Recognise it
"Generate all possible…" — that phrasing means exponential output and either backtracking or
iterative expansion. Your solution uses the iterative form, which is worth studying as the
*other* way to enumerate.

### Intuition
Build the results one character at a time. Maintain a list of all partial strings built so far.
For each new character:

- a **letter** → each partial string spawns **two** children (lowercase and uppercase)
- a **digit** → each partial string spawns **one** child

The list doubles at every letter, which is exactly the 2^(letters) answer count.

### Dry run — `s = "a1b2"`

| char | is letter? | `output` after |
|---|---|---|
| start | | `[""]` |
| `a` | yes | `["a", "A"]` |
| `1` | no | `["a1", "A1"]` |
| `b` | yes | `["a1b","a1B","A1b","A1B"]` |
| `2` | no | `["a1b2","a1B2","A1b2","A1B2"]` |

### The code

```python
class Solution:
    def letterCasePermutation(self, s: str) -> List[str]:
        output = [""]                       # (1)
        for c in s:
            tmp = []                        # (2)
            if c.isalpha():                 # (3)
                for o in output:
                    tmp.append(o+c.lower()) # (4)
                    tmp.append(o+c.upper())
            else:
                for o in output:
                    tmp.append(o+c)         # (5)
            output = tmp                    # (6)
        return output
```

**(1)** Seeded with **one empty string**, not an empty list. `[""]` gives the loop something to
extend; `[]` would produce nothing, since the inner `for o in output` would never run.

**(2)** A fresh list each round. You cannot append to `output` while iterating it — you'd
process your own additions and loop forever.

**(3)** `c.isalpha()` — is it a letter? Digits take the single-child branch.

**(4)** Two children. `c.lower()` and `c.upper()` are no-ops on characters that have no case,
which is why the `isalpha()` check is what distinguishes the branches rather than the case
methods themselves.

**(5)** One child — the digit is copied through.

**(6)** Replace the frontier. `output` now holds all partial strings of length `i+1`.

### The backtracking version — for comparison

```python
def letterCasePermutation(self, s: str) -> List[str]:
    res = []
    def backtrack(i, path):
        if i == len(s):
            res.append("".join(path))
            return
        if s[i].isalpha():
            backtrack(i + 1, path + [s[i].lower()])
            backtrack(i + 1, path + [s[i].upper()])
        else:
            backtrack(i + 1, path + [s[i]])
    backtrack(0, [])
    return res
```

Same complexity, same answers. The iterative version builds **breadth-first** (all length-1
prefixes, then all length-2…); backtracking goes **depth-first** (one complete string, then
back up). Recognising that these are two traversals of the same decision tree is the point.

### Complexity
Let n = length, L = number of letters.

- **Time O(n · 2^L)** — 2^L results, each O(n) to build. Note the string concatenation `o + c`
  copies the whole prefix each time, which is where the factor of n comes from.
- **Space O(n · 2^L)** for the output.

### Try next
[Subsets (next)](https://leetcode.com/problems/subsets/) — the same doubling, on elements instead of cases ·
[Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) ·
[Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

---

## 6. Subsets

**[LeetCode 78 →](https://leetcode.com/problems/subsets/)** · Medium · Backtracking · [`22-Subsets.py`](../22-Subsets.py)

### In one line
Return the power set — every possible subset of a list of **distinct** integers.

```
[1,2,3] → [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
```

### Recognise it
"All subsets", "power set", "all combinations". Also: **n ≤ 20 in the constraints** is a direct
signal that 2ⁿ enumeration is intended — see [Complexity](./02-complexity.md).

### Intuition — and the connection to yesterday
Every element is either **in** the subset or **out**. That's a binary decision per element, so
2ⁿ subsets, and the decision tree is a binary tree of depth n.

**You already know how to walk a binary tree.** The only difference is that this tree isn't in
memory — each recursive call *is* a node, and the choices are generated rather than looked up.

The `start` parameter is the crucial detail: recursing with `i + 1` means each element is only
ever considered once, and only elements *after* it can follow. That's what makes the output
combinations (order-independent) rather than permutations.

### Dry run — `nums = [1,2,3]` (the recursion tree)

```
backtrack(0, [])                    → record []
├─ i=0: backtrack(1, [1])           → record [1]
│  ├─ i=1: backtrack(2, [1,2])      → record [1,2]
│  │  └─ i=2: backtrack(3, [1,2,3]) → record [1,2,3]
│  └─ i=2: backtrack(3, [1,3])      → record [1,3]
├─ i=1: backtrack(2, [2])           → record [2]
│  └─ i=2: backtrack(3, [2,3])      → record [2,3]
└─ i=2: backtrack(3, [3])           → record [3]
```

8 = 2³ subsets ✓. Notice **every node is recorded**, not just the leaves — that's what makes it
subsets rather than permutations.

### The code

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def backtrack(start,path):
            result.append(path)                     # (1)
            for i in range(start,len(nums)):        # (2)
                backtrack(i+1,path+[nums[i]])       # (3)

        result = []
        backtrack(0,[])                             # (4)
        return result
```

**(1)** **Record at every node, with no base case and no termination check.** Unusual, and
correct: every partial path *is* a valid subset. The recursion ends naturally when
`start == len(nums)` makes the `range` empty.

**(2)** `range(start, len(nums))` — only elements from `start` onward. This is what prevents
`[2,1]` from being generated after `[1,2]`; subsets are unordered, so each combination must
appear once.

**(3)** **`path + [nums[i]]` creates a NEW list.** This is the copy-on-descent style, and it's
why no `path.pop()` undo step is needed — the caller's `path` was never touched. It also means
`result.append(path)` at (1) is safe without a `[:]` copy, since nothing will ever mutate that
list afterwards.

Contrast with problem 7, which mutates and therefore **must** copy on save. Compare the two
files side by side today — they're the two halves of the same lesson.

**(4)** Start at index 0 with an empty path, which immediately records `[]` — the empty subset.

### Complexity
- **Time O(n · 2ⁿ)** — 2ⁿ subsets, each costing O(n) to build via the slice-and-concatenate.
- **Space O(n)** auxiliary (the recursion depth and current path), or **O(n · 2ⁿ)** counting
  the output. Say which you mean.

### The bitmask alternative
Each of the 2ⁿ integers from 0 to 2ⁿ−1 *is* a subset, with bit `i` meaning "include element i":
```python
res = []
for mask in range(1 << len(nums)):
    res.append([nums[i] for i in range(len(nums)) if mask & (1 << i)])
return res
```
No recursion at all. `1 << n` is 2ⁿ; `mask & (1 << i)` tests bit i — Day 1's bit operators,
reused.

### Try next
[Subsets II](https://leetcode.com/problems/subsets-ii/) — with duplicates; sort first, then skip `i > start and nums[i] == nums[i-1]` (the 3Sum dedup trick from Day 2!) ·
[Combination Sum](https://leetcode.com/problems/combination-sum/) ·
[Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)

---

## 7. Combinations

**[LeetCode 77 →](https://leetcode.com/problems/combinations/)** · Medium · Backtracking with a size target · [`23-Combinations.py`](../23-Combinations.py)

### In one line
All combinations of `k` numbers chosen from `1..n`.

```
n = 4, k = 2 → [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
```

### Recognise it
Subsets, but **only those of a specific size**. Adds a real base case — and demonstrates the
mutate-and-undo style that problem 6 avoided.

### Intuition
Same tree as Subsets, but instead of recording every node, record only nodes at **depth k**.

### Dry run — `n = 4, k = 2`

```
backtrack(1, [])
├─ append 1 → [1]
│  ├─ append 2 → [1,2]  ✓ RECORD, pop → [1]
│  ├─ append 3 → [1,3]  ✓ RECORD, pop → [1]
│  └─ append 4 → [1,4]  ✓ RECORD, pop → [1]
│  pop → []
├─ append 2 → [2]
│  ├─ [2,3] ✓   ├─ [2,4] ✓
└─ append 3 → [3] → [3,4] ✓
```

Watch `curr`: it's **one list**, mutated up and down. That's why (2) needs the copy.

### The code

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def backtrack(first = 1, curr = []):        # (1)
            if len(curr) == k:                      # (2)
                output.append(curr[:])              # (3)
                return                              # (4)
            for i in range(first,n+1):              # (5)
                curr.append(i)                      # (6)  CHOOSE
                backtrack(i+1,curr)                 # (7)  EXPLORE
                curr.pop()                          # (8)  UN-CHOOSE

        output = []
        backtrack()
        return output
```

**(1)** ⚠️ **`curr = []` is a mutable default argument** — one of Python's genuine traps. The
default list is created **once**, when the function is *defined*, not per call. If it were left
non-empty between calls, the next call would inherit the garbage.

It's safe **here** only because every `append` at (6) is matched by a `pop` at (8), so `curr`
is empty again by the time the top-level call returns. That's a fragile thing to depend on. The
standard fix:
```python
def backtrack(first=1, curr=None):
    if curr is None:
        curr = []
```
See [Python §14](./01-python-for-dsa.md).

**(2)** The base case: exactly `k` elements chosen.

**(3)** **`curr[:]` — the copy is MANDATORY.** `curr` is one list being mutated throughout the
recursion. Appending `curr` itself would store a **reference**; the subsequent `pop()` at (8)
would mutate the stored object, and you'd finish with C(n,k) references to a single empty list.

This is *the* backtracking bug. Whenever you mutate-and-undo, copy on save.

**(4)** `return` — the combination is complete, nothing more to add.

**(5)** `range(first, n+1)` — numbers are **1-indexed** here (`1..n`), hence `n+1` for an
inclusive bound. Starting at `first` prevents reusing earlier numbers, so `[2,1]` is never
generated after `[1,2]`.

**(6)–(8)** **The choose / explore / un-choose triple.** The `pop()` at (8) is literally the
"backtracking" — it undoes the choice so the next iteration of the loop starts from a clean
state. Delete it and `curr` grows without bound.

### The pruning optimisation
If fewer than `k − len(curr)` numbers remain, no valid combination can be completed — so don't
even start:
```python
for i in range(first, n - (k - len(curr)) + 2):
```
Cuts a large fraction of the tree for big `n`. Worth mentioning as a follow-up; the unpruned
version is what to write first.

### Complexity
- **Time O(k · C(n,k))** — C(n,k) combinations, each O(k) to copy at (3).
- **Space O(k)** auxiliary — the recursion depth and `curr`. Plus the output.

### Try next
[Combination Sum](https://leetcode.com/problems/combination-sum/) — reuse allowed, so recurse with `i` not `i+1` ·
[Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) ·
[Subsets](https://leetcode.com/problems/subsets/) — compare the two styles directly

---

## 8. Permutations

**[LeetCode 46 →](https://leetcode.com/problems/permutations/)** · Medium · Backtracking, all orderings · [`24-permutation.py`](../24-permutation.py)

> ⚠️ **This file had two bugs on one line** — `nums[:]` never removed the chosen element (so the
> recursion never shrank), and `path + nums[i]` raised `TypeError`. Fixed; see
> [bugs-found.md §1](./bugs-found.md).

### In one line
All orderings of the given distinct integers.

```
[1,2,3] → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### Recognise it
"All permutations", "all orderings", "arrangements". n! results, so n is always tiny (≤ 8 or so).

### Intuition — and the key difference from Combinations
In combinations, order **doesn't** matter, so we only look *forward* (`range(start, n)`).

In permutations, order **does** matter, so at every step **any remaining element** may be
chosen. That means no `start` index — instead, pass down the list of elements not yet used.

n choices, then n−1, then n−2… = n! leaves.

### Dry run — `nums = [1,2,3]`

```
backtrack([1,2,3], [])
├─ take 1 → backtrack([2,3], [1])
│  ├─ take 2 → backtrack([3], [1,2]) → take 3 → backtrack([], [1,2,3]) ✓
│  └─ take 3 → backtrack([2], [1,3]) → take 2 → [1,3,2] ✓
├─ take 2 → backtrack([1,3], [2]) → [2,1,3] ✓, [2,3,1] ✓
└─ take 3 → backtrack([1,2], [3]) → [3,1,2] ✓, [3,2,1] ✓
```

6 = 3! ✓ — and note results are recorded **only at the leaves** (when `remaining` is empty),
unlike Subsets which records at every node.

### The code (fixed)

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def backtrack(remaining, path):
            if not remaining:                # (1)
                result.append(path)
                return                       # (2)

            for i in range(len(remaining)):  # (3)
                backtrack(remaining[:i] + remaining[i+1:],   # (4)
                          path + [remaining[i]])             # (5)

        result = []
        backtrack(nums, [])
        return result
```

**(1)** Base case: nothing left to place, so `path` is a complete permutation. **Recording only
at leaves** is what distinguishes this from Subsets.

**(2)** ⚠️ The original was missing this `return`. Harmless (the loop below would be empty
anyway) but it made the intent unclear.

**(3)** **Every** remaining element is a candidate — no `start` index, because order matters.

**(4)** ⚠️ **The main bug.** The original was `remaining[:] + remaining[i+1:]`:
```python
remaining = [1,2,3]; i = 1
remaining[:]  + remaining[2:]   # [1,2,3,3]  <- element 1 NOT removed, 3 duplicated
remaining[:i] + remaining[i+1:] # [1,3]      <- correct
```
Because the list never shrank, the recursion never reached its base case.

**The check that catches this class of bug:** say the recursive call out loud and ask *"is the
argument I'm passing down smaller than the one I received?"* Here it was **larger**.

**(5)** ⚠️ The second bug: `path + nums[i]` is `list + int` → `TypeError`. `[remaining[i]]`
wraps the int in a list so `+` concatenates two lists. See [Python §5](./01-python-for-dsa.md).

Also note: `remaining[i]`, not `nums[i]`. The original mixed the two, which would index the
wrong list once `remaining` diverged from `nums`.

### The swap-based version — O(1) extra space per level
```python
def permute(self, nums):
    res = []
    def backtrack(start):
        if start == len(nums):
            res.append(nums[:])                    # copy, since nums is mutated
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]   # swap into place
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]   # swap back -- UNDO
    backtrack(0)
    return res
```
No slicing, so no per-level allocation. Uses the choose/explore/un-choose triple from problem 7.

### Complexity
- **Time O(n · n!)** — n! permutations, each O(n) to construct. The slicing at (4) adds
  another O(n) per level, so the slice version is closer to O(n² · n!/…) in practice; the swap
  version is the clean O(n · n!).
- **Space O(n · n!)** for the output; **O(n)** recursion depth. The slicing version also holds
  O(n) of temporary lists per level, so O(n²) auxiliary.

### Try next
[Permutations II](https://leetcode.com/problems/permutations-ii/) — with duplicates; sort and skip ·
[Next Permutation](https://leetcode.com/problems/next-permutation/) ·
[N-Queens](https://leetcode.com/problems/n-queens/) — permutations with constraint pruning

---

## 9. Coin Change

**[LeetCode 322 →](https://leetcode.com/problems/coin-change/)** · Medium · Bottom-up DP · [`16-Coin_change.py`](../16-Coin_change.py)

### In one line
Fewest coins summing to `amount`, or −1 if impossible. Unlimited coins of each denomination.

```
coins = [1,2,5], amount = 11 → 3      (5 + 5 + 1)
coins = [2], amount = 3      → -1
```

### Recognise it
"Minimum number of X to reach Y", "fewest coins", "minimum steps". Note the greedy approach
(**always take the biggest coin**) is **wrong**: with `coins = [1,3,4]` and `amount = 6`, greedy
gives `4+1+1 = 3` coins but the answer is `3+3 = 2`. That failure is exactly why this needs DP.

### Intuition
Ask: *to make amount `a`, what smaller answers do I need?*

For each coin `c`, if you use it, the rest is `a − c` — a subproblem you've already solved. So:

> `dp[a] = 1 + min(dp[a - c])` over every coin `c` that fits

Solve amounts in increasing order and every `dp[a - c]` is already known. That's bottom-up DP.

### Dry run — `coins = [1,2,5]`, `amount = 11` (first few)

| a | candidates `1 + dp[a-c]` | `dp[a]` |
|---|---|---|
| 0 | — | **0** (base) |
| 1 | `1+dp[0]=1` | **1** |
| 2 | `1+dp[1]=2`, `1+dp[0]=1` | **1** |
| 3 | `1+dp[2]=2`, `1+dp[1]=2` | **2** |
| 4 | `1+dp[3]=3`, `1+dp[2]=2` | **2** |
| 5 | `1+dp[4]=3`, `1+dp[3]=3`, `1+dp[0]=1` | **1** |
| 6 | `1+dp[5]=2`, `1+dp[4]=3`, `1+dp[1]=2` | **2** |
| … | | |
| 11 | `1+dp[10]=3`, `1+dp[9]=4`, `1+dp[6]=3` | **3** ✓ |

### The code

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1)        # (1)
        dp[0] = 0                               # (2)

        for a in range(1,amount+1):             # (3)
            for c in coins:                     # (4)
                if a - c >= 0:                  # (5)
                    dp[a] = min(dp[a],1+dp[a-c])    # (6)

        return dp[amount] if dp[amount] != amount + 1 else -1   # (7)
```

**(1)** **`amount + 1` as the "impossible" sentinel.** Cleverly chosen: you can never need more
than `amount` coins (the smallest possible coin is 1, giving exactly `amount` coins), so
`amount + 1` is unreachable but still a real integer that `min` and `+ 1` work on. `float('inf')`
also works but `inf + 1` in a comparison is slightly clumsier.

The array has `amount + 1` **slots**, indices 0 through `amount` inclusive. Note the value and
the length are both `amount + 1` for entirely unrelated reasons — a nice coincidence, and a
source of confusion when reading.

**(2)** The base case: zero coins make zero. Every other answer builds on this.

**(3)** **Increasing order** — essential. When computing `dp[a]`, every `dp[a - c]` has a
smaller index and is therefore already final.

**(4)** Try every coin. This is why coins can be reused without limit: `dp[a - c]` may itself
have used coin `c`.

**(5)** Don't index negatively. `dp[-1]` in Python is the *last* element — a silent wrong answer
rather than a crash, which is why this guard matters.

**(6)** Take the best option. `1 +` for the coin you just used.

**(7)** Unchanged sentinel → unreachable → −1.

### Complexity
- **Time O(amount × len(coins))** — the two nested loops.
- **Space O(amount)** for the table.

Note this is driven by the **numeric value** of `amount`, not by array length. That makes it
**pseudo-polynomial**: an amount of 10⁹ would be infeasible even with 3 coins. Saying this
aloud is a strong signal in an interview.

### Try next
[Coin Change II](https://leetcode.com/problems/coin-change-ii/) — count the *ways*, not the minimum; the loop order changes! ·
[Minimum Cost For Tickets](https://leetcode.com/problems/minimum-cost-for-tickets/) ·
[Perfect Squares](https://leetcode.com/problems/perfect-squares/) — the same recurrence with squares as coins

---

## 10. Climbing Stairs

**[LeetCode 70 →](https://leetcode.com/problems/climbing-stairs/)** · Easy · 1-D DP · [`17-climbing_stairs.py`](../17-climbing_stairs.py)

### In one line
You can climb 1 or 2 steps at a time. How many distinct ways to reach step `n`?

```
n = 2 → 2      (1+1, or 2)
n = 3 → 3      (1+1+1, 1+2, 2+1)
```

### Recognise it
"How many ways to…" + a small fixed set of moves. The canonical first DP problem, and the
cleanest possible illustration of a recurrence.

### Intuition
To arrive at step `i`, your **last** move was either a 1-step (from `i−1`) or a 2-step (from
`i−2`). Those two sets of paths are disjoint and cover everything, so:

> **dp[i] = dp[i−1] + dp[i−2]**

That's the Fibonacci recurrence, arrived at from first principles rather than recognised.

Note *why* the naive recursion is bad: `climb(5)` calls `climb(4)` and `climb(3)`; `climb(4)`
calls `climb(3)` again. The same subproblems are recomputed exponentially often — O(2ⁿ). Storing
each answer once makes it O(n). **That's what DP is**: the same recursion, with the repeats
removed.

### Dry run — `n = 6`

| i | `dp[i-1]` | `dp[i-2]` | `dp[i]` |
|---|---|---|---|
| 1 | — | — | 1 (base) |
| 2 | — | — | 2 (base) |
| 3 | 2 | 1 | **3** |
| 4 | 3 | 2 | **5** |
| 5 | 5 | 3 | **8** |
| 6 | 8 | 5 | **13** |

### The code

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:                  # (1)
            return 1

        dp = [0] * (n + 1)          # (2)
        dp[1] = 1                   # (3)
        dp[2] = 2

        for i in range(3, n + 1):   # (4)
            dp[i] = dp[i - 1] + dp[i - 2]   # (5)

        return dp[n]
```

**(1)** **The `n == 1` guard, and why it's needed.** With `n = 1`, the array has 2 slots
(indices 0 and 1), so `dp[2] = 2` at (3) would raise `IndexError`. Handling it up front is the
simplest fix.

**(2)** `n + 1` slots so `dp[n]` is a valid index — the standard 1-indexed DP array where slot
0 goes unused.

**(3)** The two base cases, which cannot be derived from the recurrence (they'd need `dp[0]` and
`dp[-1]`). Every DP needs enough base cases to bootstrap the recurrence; here that's two,
because the recurrence looks back two steps.

**(4)** From 3, since 1 and 2 are already known.

**(5)** The recurrence. Both indices are smaller than `i`, so both are final.

### The O(1)-space version — the standard follow-up
The recurrence only ever looks back **two** slots, so the whole array is unnecessary:

```python
def climbStairs(self, n: int) -> int:
    prev, curr = 1, 1               # ways to reach step 0 and step 1
    for _ in range(n - 1):
        prev, curr = curr, prev + curr
    return curr
```
**O(n) time, O(1) space.** The simultaneous assignment evaluates the right-hand side fully
before assigning — see [Python §12](./01-python-for-dsa.md).

**This "keep only the last k values" reduction applies to any DP with a fixed lookback**, and
it's the follow-up interviewers ask for most often on DP problems.

### Complexity
- **Time O(n)** — one pass. Naive recursion is O(2ⁿ); memoisation or tabulation makes it linear.
- **Space O(n)** as written, **O(1)** with the rolling version.

### Try next
[Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) — same recurrence with costs ·
[House Robber](https://leetcode.com/problems/house-robber/) — the same shape: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` ·
[Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) ·
[Decode Ways](https://leetcode.com/problems/decode-ways/)

---

## Recall drill

1. What is the structural relationship between tree DFS and backtracking?
2. In Combinations, why is `output.append(curr[:])` written with `[:]` while Subsets writes
   `result.append(path)` with no copy?
3. In grid BFS, why mark a cell visited when you **enqueue** it rather than when you dequeue it?
4. Coin Change: why does greedy (always take the largest coin) fail? Give a counterexample.
5. Climbing Stairs uses O(n) space. How would you make it O(1), and when does that trick apply
   generally?

<details>
<summary>Answers</summary>

1. **They are the same algorithm.** Both are DFS. Tree DFS walks children that already exist in
   memory (`node.left`, `node.right`); backtracking walks children it *generates*
   (`for choice in available(...)`). The "tree" in backtracking is the space of partial
   solutions and is never built — only the current root-to-node path exists at any moment,
   which is why the space is O(depth) and not O(2ⁿ).
2. Because of the two different styles. Combinations **mutates one shared list**
   (`curr.append` / `curr.pop`), so storing `curr` itself would store a reference that the
   subsequent `pop()` corrupts — you'd finish with C(n,k) references to one empty list. Subsets
   uses `path + [nums[i]]`, which **creates a new list** on every descent, so the stored object
   is never mutated afterwards and needs no copy. **Mutate ⇒ copy on save.**
3. Otherwise a cell with several land neighbours can be pushed onto the queue multiple times
   before it's first dequeued. Marking on enqueue guarantees each cell enters the queue exactly
   once, which is what keeps the traversal O(rows × cols).
4. Greedy fails because a large coin can force an inefficient remainder.
   **`coins = [1,3,4]`, `amount = 6`:** greedy takes 4, then 1, then 1 → **3 coins**. The
   optimum is 3 + 3 → **2 coins**. Local optimality doesn't compose here, which is exactly the
   condition that calls for DP.
5. Keep two rolling variables instead of the array:
   `prev, curr = curr, prev + curr`. The reduction applies to **any DP whose recurrence looks
   back a fixed number of positions** — keep only that many values. It does *not* apply when
   the recurrence can reach arbitrarily far back (like Coin Change, where `dp[a - c]` can be
   any distance behind).

</details>

---

## You've finished the week. Now what?

### What you actually have now

Ten patterns that between them cover a very large share of LeetCode's Easy and Medium tiers:

hash map · two pointers · sliding window · binary search (including **on the answer**) ·
heap · monotonic stack · fast & slow pointers · tree DFS/BFS · backtracking · 1-D DP

Plus the thing that matters more than any of them: the habit of asking *"what shape is this
problem?"* before writing code.

### The next two weeks

1. **Spaced review, starting tomorrow.** Re-solve from a blank screen: Two Sum, Minimum Size
   Subarray Sum, Binary Search, Koko Eating Bananas, Daily Temperatures, Reverse Linked List,
   Level Order Traversal, Subsets, Coin Change. Ten minutes a day. Skipping this is how the
   week evaporates.

2. **Work the "Try next" links.** There are roughly 200 of them across the seven days, every
   one chosen because it uses a pattern you now know. That's where 70 becomes 300.

3. **The patterns still missing**, in priority order — each is a day's work using
   [the cheat sheet](./03-pattern-cheatsheet.md) as your guide:
   - **Graphs beyond grids** — adjacency lists, [Course Schedule](https://leetcode.com/problems/course-schedule/) (topological sort), [Clone Graph](https://leetcode.com/problems/clone-graph/)
   - **2-D DP** — [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/), [Unique Paths](https://leetcode.com/problems/unique-paths/), [Edit Distance](https://leetcode.com/problems/edit-distance/)
   - **Intervals** — [Merge Intervals](https://leetcode.com/problems/merge-intervals/), [Insert Interval](https://leetcode.com/problems/insert-interval/), [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
   - **Greedy** — [Jump Game](https://leetcode.com/problems/jump-game/), [Gas Station](https://leetcode.com/problems/gas-station/)
   - **Tries** — [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/), [Word Search II](https://leetcode.com/problems/word-search-ii/)
   - **Union-Find** — [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/), [Redundant Connection](https://leetcode.com/problems/redundant-connection/)
   - **House Robber and friends** — the DP family this guide only touched: [House Robber](https://leetcode.com/problems/house-robber/), [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/), [Word Break](https://leetcode.com/problems/word-break/)

4. **When you're stuck on something new**, work the five questions at the bottom of
   [the cheat sheet](./03-pattern-cheatsheet.md). In order. Every time.

The single highest-value habit from this week: **name the pattern before you write a line of
code.** If you can't name it, you're not ready to type yet — and that's information, not
failure.
