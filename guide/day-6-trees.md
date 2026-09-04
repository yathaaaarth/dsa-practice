# Day 6 — Binary Trees

> **Today's big idea:** almost every binary-tree problem is the *same six-line recursion* with
> one line changed. Once you see that, a topic that looks like twenty separate problems
> collapses into one template plus a lookup table. Nine of today's ten are your own solutions.

**Warm-up (10 min, blank screen):** re-solve Reverse Linked List and Merge Two Sorted Lists.

---

## Pattern primer

### The node

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

A tree is defined **recursively**: a node, plus a left subtree, plus a right subtree — each of
which is itself a tree, possibly empty. That recursive *definition* is why recursive *code*
fits so naturally.

### Template 1 — DFS, the universal shape

```python
def dfs(node):
    if not node:                     # BASE CASE, always first
        return identity              # 0, True, None -- whatever "nothing" means here
    left  = dfs(node.left)           # solve the left subtree
    right = dfs(node.right)          # solve the right subtree
    return combine(left, right, node.val)     # <-- ONLY THIS LINE CHANGES
```

That is the whole topic. Look at what `combine` becomes:

| Problem | `identity` | `combine(left, right, val)` |
|---|---|---|
| Max depth | `0` | `max(left, right) + 1` |
| Min depth | `0` | `min(left, right) + 1` *(plus a leaf guard — see problem 2)* |
| Count nodes | `0` | `left + right + 1` |
| Sum of values | `0` | `left + right + val` |
| Same tree | `True` | `left and right and p.val == q.val` |
| Invert | `None` | swap the children, return node |
| Diameter | `0` | return height; record `left + right` on the side |
| Path sum | `False` | `left or right` |

**Write the base case first. Every time.** If you find yourself typing the recursive call
before `if not node:`, stop and go back. That habit alone would have prevented one of the six
bugs in this repo (see [bugs-found.md §6](./bugs-found.md)).

**Why `if not node` and not `if node is None`:** a `TreeNode` object is always truthy — even
one holding `val = 0` — so there's no falsy-zero trap here. `if not node` is the idiom.

### Template 2 — BFS, level by level

```python
from collections import deque

q, out = deque([root]), []
while q:
    level = []
    for _ in range(len(q)):          # <-- snapshot the size FIRST
        node = q.popleft()
        level.append(node.val)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    out.append(level)
```

**`for _ in range(len(q))` is the entire trick.** `len(q)` is evaluated **once**, before the
loop starts, capturing exactly how many nodes are on the current level. The queue grows during
the loop as children are added, but the loop count is already fixed — so it processes exactly
one level per outer iteration.

Without that snapshot, levels bleed into each other and you get a flat traversal.

### DFS or BFS?

| Use | When |
|---|---|
| **DFS** | depth, paths from root to leaf, comparing or transforming whole subtrees |
| **BFS** | anything "level by level", or **shortest** path in an unweighted graph |

**Space differs and interviewers ask:** DFS is O(h) for the call stack — O(log n) balanced,
O(n) for a degenerate skewed tree. BFS is O(w) where w is the widest level, which is up to n/2
at the bottom of a complete tree. Neither is universally cheaper.

### Traversal orders (for DFS)

```python
def inorder(node):    # LEFT, node, RIGHT   -- on a BST this yields SORTED order
    if not node: return
    inorder(node.left); print(node.val); inorder(node.right)

def preorder(node):   # node, LEFT, RIGHT   -- copying/serialising a tree
def postorder(node):  # LEFT, RIGHT, node   -- deleting, or when children must resolve first
```

The name says **where the node itself is visited** relative to its subtrees. **In-order on a
BST gives sorted output** — bank that; it's the answer to a whole family of BST problems.

Copy both templates out by hand.

---

## 1. Maximum Depth of Binary Tree

**[LeetCode 104 →](https://leetcode.com/problems/maximum-depth-of-binary-tree/)** · Easy · DFS · [`41-Max_depth_bt.py`](../41-Max_depth_bt.py)

### In one line
Number of nodes on the longest root-to-leaf path.

```
    3
   / \      → 3
  9  20
     / \
    15  7
```

### Recognise it
The simplest possible tree recursion, and the base template for everything today.

### Intuition
The depth of a tree is *one more than* the depth of its deeper subtree. That sentence is the
code.

### Dry run — the tree above

| call | left | right | returns |
|---|---|---|---|
| `dfs(15, d=2)` | `dfs(None, 3)` → 3 | `dfs(None, 3)` → 3 | 3 |
| `dfs(7, d=2)` | 3 | 3 | 3 |
| `dfs(20, d=1)` | `dfs(15,2)` → 3 | `dfs(7,2)` → 3 | 3 |
| `dfs(9, d=1)` | 2 | 2 | 2 |
| `dfs(3, d=0)` | `dfs(9,1)` → 2 | `dfs(20,1)` → 3 | **3** |

### The code

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(root,depth):                                  # (1)
            if not root:
                return depth                                  # (2)
            return max(dfs(root.left,depth + 1),
                       dfs(root.right, depth + 1))            # (3)

        return dfs(root,0)                                    # (4)
```

This is the **accumulator** style: the depth is passed *down* and returned back up unchanged
at the leaves.

**(1)** An inner function, closing over nothing here but keeping the public signature clean.
It also sidesteps the `self.` requirement that broke [`47-LCA.py`](../47-LCA.py) — see
[bugs-found.md §5](./bugs-found.md).

**(2)** Base case: an empty subtree contributes the depth accumulated so far.

**(3)** `max` of both branches. Both are explored fully — you cannot know which is deeper
without looking.

**(4)** Start at depth 0, so a single node returns 1.

### The bottom-up form — worth writing too

```python
def maxDepth(self, root):
    if not root:
        return 0
    return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
```

Three lines, no accumulator, no helper. Depth is computed on the way **back up** rather than
carried down. This is the template from the primer, and it's what you should write.

### Complexity
- **Time O(n)** — every node visited exactly once, O(1) work each.
- **Space O(h)** — the recursion stack, where h is the height. **O(log n)** for a balanced
  tree, **O(n)** for a degenerate one (a tree that's really a linked list). Always state both.

### Try next
[Minimum Depth (next)](https://leetcode.com/problems/minimum-depth-of-binary-tree/) ·
[Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) ·
[Count Complete Tree Nodes](https://leetcode.com/problems/count-complete-tree-nodes/)

---

## 2. Minimum Depth of Binary Tree

**[LeetCode 111 →](https://leetcode.com/problems/minimum-depth-of-binary-tree/)** · Easy · DFS with a leaf guard · [`40_mini_depth_bt.py`](../40_mini_depth_bt.py)

> ⚠️ **This file would not even compile** — `return dfs(root)` sat at class-body indentation,
> giving `SyntaxError: 'return' outside function`. Fixed; see
> [bugs-found.md §4](./bugs-found.md).

### In one line
Nodes on the **shortest** root-to-**leaf** path. A leaf has **no children at all**.

```
1→2→3→4→5 (a right-skewed chain) → 5, not 2
```

### Recognise it
It looks like problem 1 with `max` swapped for `min`. **It is not**, and that trap is the
entire point of the problem.

### Intuition
`min(left, right) + 1` is wrong. Consider a node with a left child but no right child. The
right subtree returns 0, so `min(left, 0) + 1 = 1` — claiming the path ends here. But this
node **is not a leaf**; it has a child. The path must continue.

So: if one side is empty, you must go down the **other** side. Only when both children exist
do you take the minimum.

### Dry run — the right-skewed chain `2→3→4→5→6`

| node | left | right | rule applied | returns |
|---|---|---|---|---|
| 6 (leaf) | 0 | 0 | `right == 0` → `left + 1` | 1 |
| 5 | 0 | 1 | **`left == 0` → `right + 1`** | 2 |
| 4 | 0 | 2 | `left == 0` → `right + 1` | 3 |
| 3 | 0 | 3 | same | 4 |
| 2 | 0 | 4 | same | **5** ✓ |

With a naive `min(left, right) + 1` every node would return 1 and the answer would be a very
confident **1**.

### The code (fixed)

```python
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0                     # (1)
            left = dfs(node.left)
            right = dfs(node.right)

            if left == 0:                    # (2)
                return right + 1
            if right == 0:                   # (3)
                return left + 1

            return min(right, left) + 1      # (4)

        return dfs(root)                     # (5)
```

**(1)** An empty subtree has depth 0 — used as a *signal* by (2) and (3), not just a value.

**(2)–(3)** **The leaf guard.** `left == 0` means there's no left child, so this node isn't a
leaf and the shortest path must descend right. Fall through to the other side rather than
letting the 0 win the `min`.

Note both guards firing simultaneously is fine: a true leaf has `left == right == 0`, so (2)
returns `0 + 1 = 1` ✓

**(4)** Both children exist → genuinely take the smaller.

**(5)** **This is the line that was broken** — it was indented four spaces (class body) instead
of eight (method body). Python's indentation *is* its syntax, so this was a compile error, not
a style issue. Note that `ast.parse()` does **not** catch it; you need `compile()`. See
[bugs-found.md §4](./bugs-found.md).

### The BFS solution — actually better here

```python
from collections import deque

def minDepth(self, root):
    if not root:
        return 0
    q, depth = deque([root]), 1
    while q:
        for _ in range(len(q)):
            node = q.popleft()
            if not node.left and not node.right:
                return depth                  # first leaf found = shallowest leaf
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        depth += 1
```

BFS finds the shallowest leaf and **returns immediately** — it never explores the deep
branches. On a tree with one shallow leaf and a million-node deep branch, DFS visits every
node and BFS visits a handful. This is the general principle: **BFS is the right tool for
"shortest"**, DFS for "longest".

### Complexity
- **DFS: O(n) time, O(h) space.**
- **BFS: O(n) worst case but often far less, O(w) space.**

### Try next
[Maximum Depth](https://leetcode.com/problems/maximum-depth-of-binary-tree/) ·
[Binary Tree Level Order Traversal (problem 8)](https://leetcode.com/problems/binary-tree-level-order-traversal/) ·
[Sum of Left Leaves](https://leetcode.com/problems/sum-of-left-leaves/)

---

## 3. Same Tree

**[LeetCode 100 →](https://leetcode.com/problems/same-tree/)** · Easy · Parallel DFS · [`43-Same_tree.py`](../43-Same_tree.py)

### In one line
Are two trees structurally identical **and** value-identical?

```
[1,2,3] vs [1,2,3]      → True
[1,2]   vs [1,null,2]   → False    (same values, different shape)
```

### Recognise it
Comparing two trees → recurse on **both simultaneously**, passing a pair of nodes instead of
one. Same template, doubled.

### Intuition
Two trees are the same if: both roots are empty, or both exist with equal values **and** their
left subtrees match **and** their right subtrees match. Read that sentence — it's literally the
code, including the order of the checks.

### Dry run — `p = [1,2]`, `q = [1,null,2]`

| call | p | q | result |
|---|---|---|---|
| `(1, 1)` | node | node | values equal → recurse |
| `(p.left=2, q.left=None)` | node 2 | **None** | one is None → **False** |

Short-circuits immediately. `and` means the right subtree is never even examined.

### The code

```python
class Solution:
    def isSameTree(self, p, q) -> bool:
        if p == None and q == None:      # (1)
            return True
        if p == None or q == None:       # (2)
            return False
        if p.val != q.val:               # (3)
            return False
        return self.isSameTree(p.left,q.left) and \
               self.isSameTree(p.right,q.right)      # (4)
```

**(1)** Both empty → trivially identical. The base case, first.

**(2)** Exactly one empty (the first check already ruled out both) → different shapes. **This
guard is what makes (3) safe** — without it, `p.val` on a `None` raises `AttributeError`. Order
is load-bearing.

**(3)** Both exist; compare values.

**(4)** Both subtrees must match. **`and` short-circuits**: if the left subtrees differ, the
right ones are never visited — a real optimisation on large mismatched trees, not just style.

*(Style note: `p is None` is preferred over `p == None` — `is` tests identity, which is what
you mean, and it can't be overridden by a custom `__eq__`. Functionally identical here.)*

**And `self.`** — this method calls itself through the instance. Omitting it is exactly the bug
that broke [`47-LCA.py`](../47-LCA.py); see [bugs-found.md §5](./bugs-found.md).

### Complexity
- **Time O(min(n, m))** — it stops at the first difference, so it's bounded by the smaller
  tree.
- **Space O(h)** for the recursion stack.

### Try next
[Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) — the same idea, comparing a tree with its **mirror** ·
[Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) — calls `isSameTree` at every node ·
[Merge Two Binary Trees](https://leetcode.com/problems/merge-two-binary-trees/)

---

## 4. Invert Binary Tree

**[LeetCode 226 →](https://leetcode.com/problems/invert-binary-tree/)** · Easy · DFS mutation · [`46-Invert_bt.py`](../46-Invert_bt.py)

### In one line
Mirror the tree — swap every node's children.

```
    4              4
   / \            / \
  2   7    →     7   2
 / \ / \        / \ / \
1  3 6  9      9  6 3  1
```

### Recognise it
"Mirror", "flip", "reflect". Famous as the problem that got the author of Homebrew rejected
by Google. It is four lines.

### Intuition
Swap the children of every node. Order doesn't matter — do it top-down or bottom-up, the result
is identical, because swapping is independent at every node.

### The code

```python
class Solution(object):
    def invertTree(self, root):
        if not root:
            return root                                  # (1)

        self.invertTree(root.left)                       # (2)
        self.invertTree(root.right)

        root.left , root.right = root.right ,root.left   # (3)
        return root                                      # (4)
```

**(1)** Base case. `return root` rather than `return None` — same value, and it keeps the
return type consistent.

**(2)** Invert both subtrees first (post-order). The return values are **discarded**, which is
fine because the function mutates in place rather than building anything new.

**(3)** **The swap.** Python evaluates the entire right-hand side into a tuple *before*
assigning, so no temporary variable is needed. In C you'd need `tmp`. See
[Python §12](./01-python-for-dsa.md).

**(4)** Return the root so the caller gets the tree back.

### The order genuinely doesn't matter
```python
root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
```
Swap first then recurse, or recurse then swap — both correct. Contrast with problem 5
(Diameter), where the children **must** be resolved before the parent can compute anything.
Knowing which problems have that dependency is the useful distinction.

### Complexity
- **Time O(n)** — one visit per node.
- **Space O(h)** for the stack.

### The iterative version (for the "no recursion" follow-up)
```python
from collections import deque
q = deque([root])
while q:
    node = q.popleft()
    if node:
        node.left, node.right = node.right, node.left
        q.append(node.left)
        q.append(node.right)
return root
```

### Try next
[Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) ·
[Binary Tree Upside Down](https://leetcode.com/problems/binary-tree-upside-down/) ·
[Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/)

---

## 5. Path Sum

**[LeetCode 112 →](https://leetcode.com/problems/path-sum/)** · Easy · DFS with a running target · [`44-Path_sum.py`](../44-Path_sum.py)

### In one line
Is there a **root-to-leaf** path whose values sum to `targetSum`?

```
[5,4,8,11,null,13,4,7,2,null,null,null,1], target = 22 → True   (5→4→11→2)
```

### Recognise it
"Root to leaf" + "sum". Two things to get right: the definition of a **leaf**, and how to
carry the target down.

### Intuition
Instead of accumulating a sum on the way down and comparing at the bottom, **subtract as you
descend**. At each node, the remaining target becomes `target − node.val`. At a leaf, ask: does
this node's value exactly equal what's left?

Subtracting is cleaner than accumulating — one parameter instead of two.

### Dry run — path `5→4→11→2`, target 22

| node | target on entry | leaf? | action |
|---|---|---|---|
| 5 | 22 | no | recurse with `22 − 5 = 17` |
| 4 | 17 | no | recurse with `17 − 4 = 13` |
| 11 | 13 | no | recurse with `13 − 11 = 2` |
| 2 | 2 | **yes** | `targetSum == root.val` → `2 == 2` → **True** |

### The code

```python
class Solution:
    def hasPathSum(self, root, targetSum: int) -> bool:
        if not root:
            return False                          # (1)
        if not root.left and not root.right:      # (2)
            return targetSum == root.val          # (3)

        leftSum = self.hasPathSum(root.left, targetSum - root.val)    # (4)
        rightSum = self.hasPathSum(root.right, targetSum - root.val)

        return leftSum or rightSum                # (5)
```

**(1)** An empty tree has no paths. **`False`, not `targetSum == 0`** — this is the subtle
point. If you returned `targetSum == 0` here, then a node with only a left child would let the
*missing* right child claim success whenever the remaining target happened to be 0. That would
report a path ending at a non-leaf. The leaf test must happen at (2), on a real node.

**(2)** **The leaf definition: no left child AND no right child.** Same trap as problem 2's
minimum depth — a node with one child is not a leaf, and the path is not allowed to stop there.

**(3)** At a leaf, the whole path sums to the target exactly when this last value equals what's
left. Returns a `bool` directly, no `if`.

**(4)** Subtract on the way down.

**(5)** `or` — one qualifying path is enough. It also **short-circuits**: if the left subtree
finds a path, the right is never explored.

*(Minor: naming them `leftSum`/`rightSum` is misleading — they're booleans, not sums. `left`
and `right`, or inlining `return self.hasPathSum(...) or self.hasPathSum(...)`, reads better
and preserves the short-circuit.)*

### Complexity
- **Time O(n)** worst case — every node visited. Often much less thanks to short-circuiting.
- **Space O(h)**.

### Try next
[Path Sum II](https://leetcode.com/problems/path-sum-ii/) — return **all** such paths (backtracking, Day 7!) ·
[Path Sum III](https://leetcode.com/problems/path-sum-iii/) — paths that don't start at the root ·
[Sum Root to Leaf Numbers](https://leetcode.com/problems/sum-root-to-leaf-numbers/)

---

## 6. Diameter of Binary Tree

**[LeetCode 543 →](https://leetcode.com/problems/diameter-of-binary-tree/)** · Easy · DFS returning one thing, recording another · [`45-Diameter_bt.py`](../45-Diameter_bt.py)

### In one line
Length (in **edges**) of the longest path between any two nodes. The path need not pass through
the root.

```
    1
   / \       → 3    (the path 4→2→1→3, which is 3 edges)
  2   3
 / \
4   5
```

### Recognise it
"Longest path between **any** two nodes" — the path can be anywhere. This introduces the most
important structural idea in tree recursion: **return one value up, record a different value on
the side.**

### Intuition
For any node, the longest path *through that node* is `height(left) + height(right)` — go as
deep as possible one way, come back, go as deep as possible the other way.

But you can't *return* that, because your parent needs your **height** to compute its own
answer. So:

- **Return** the height (what the parent needs).
- **Record** `left + right` into a shared variable at every node (the answer you actually want).

The final answer is the maximum recorded across all nodes. This "compute two things, return one"
pattern shows up constantly in harder tree problems.

### Dry run — the tree above

| node | left height | right height | `left + right` | recorded max | returns `max+1` |
|---|---|---|---|---|---|
| 4 | 0 | 0 | 0 | 0 | 1 |
| 5 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 1 | **2** | 2 | 2 |
| 3 | 0 | 0 | 0 | 2 | 1 |
| 1 | 2 | 1 | **3** | **3** | 3 |

→ **3** ✓ — and note the winning path (through node 1) is *not* the one through node 2.

### The code

```python
class Solution:
    def diameterOfBinaryTree(self, root) -> int:
        def diameter(node,res):
            if not node:
                return 0                              # (1)
            left = diameter(node.left,res)
            right = diameter(node.right,res)

            res[0] = max(res[0], left + right)        # (2)
            return max(left,right) + 1                # (3)

        res = [0]                                     # (4)
        diameter(root,res)
        return res[0]                                 # (5)
```

**(1)** An empty subtree has height 0. Measuring in **edges** means a single node also has
height… 1 by this function's convention, and its diameter contribution is `0 + 0 = 0` — correct,
since one node spans zero edges. The off-by-one works out because heights are counted in nodes
while `left + right` counts edges.

**(2)** **Record, don't return.** The best path through *this* node.

**(3)** **Return the height** — one branch (the deeper) plus this node. You can only go down
one way from the parent's perspective; the parent cannot route *through* you.

That difference between (2) and (3) is the whole problem. Returning `left + right` instead
would let a parent build an impossible path that goes down, back up, and down again.

**(4)** **`res = [0]`, a one-element list, used as a mutable box.** Python closures can *read*
outer variables but assigning `res = ...` inside the inner function would create a new local
instead. Three ways around it:

```python
res = [0];  res[0] = ...          # mutate a list -- what this code does
self.res = 0;  self.res = ...     # an instance attribute
nonlocal res                      # the modern, explicit keyword (Python 3)
```
`nonlocal` is clearest; the list box is the most commonly seen. Know both.

**(5)** The recursion's return value is discarded — the answer lives in `res`.

### Complexity
- **Time O(n)** — one visit per node. The naive version (compute height separately at every
  node) is O(n²); computing height and diameter in the *same* pass is what makes it linear.
- **Space O(h)**.

### Try next
[Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) — hard, and it's this exact pattern ·
[Longest Univalue Path](https://leetcode.com/problems/longest-univalue-path/) ·
[Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/)

---

## 7. Average of Levels in Binary Tree

**[LeetCode 637 →](https://leetcode.com/problems/average-of-levels-in-binary-tree/)** · Easy · BFS · [`39-avg_level_bt.py`](../39-avg_level_bt.py)

### In one line
Return the average value at each level, top to bottom.

```
[3,9,20,null,null,15,7] → [3.0, 14.5, 11.0]
```

### Recognise it
"Each level" → BFS. This is the level-order template with a sum instead of a list.

### Dry run — `[3,9,20,null,null,15,7]`

| level | queue at start | `n` | nodes processed | sum | average |
|---|---|---|---|---|---|
| 0 | `[3]` | 1 | 3 | 3 | 3.0 |
| 1 | `[9,20]` | 2 | 9, 20 | 29 | 14.5 |
| 2 | `[15,7]` | 2 | 15, 7 | 22 | 11.0 |

### The code

```python
class Solution:
    def averageOfLevels(self, root) -> List[float]:
        ans = []
        if not root:
            return ans                    # (1)

        q = [root]
        while q:
            n = len(q)                    # (2)
            s = 0

            for i in range(n):
                node = q.pop(0)           # (3)
                s += node.val

                if node.right:            # (4)
                    q.append(node.right)
                if node.left:
                    q.append(node.left)
            ans.append(s/n)               # (5)

        return ans
```

**(1)** Empty tree → empty result.

**(2)** **`n = len(q)` captured before the inner loop.** The queue grows as children are
enqueued, but `n` is already fixed — so exactly one level is processed per outer iteration.
This is the single most important line in any BFS.

**(3)** ⚠️ **`q.pop(0)` on a list is O(n)** — it shifts every remaining element. Over n
dequeues that makes this BFS **O(n²)**. The fix is one import:

```python
from collections import deque
q = deque([root])
node = q.popleft()          # O(1)
```
It passes on LeetCode, but it's the wrong habit. See [Python §3](./01-python-for-dsa.md).

**(4)** ⚠️ **Right is enqueued before left.** For an *average* this is harmless — addition is
commutative, so the sum per level is unchanged. But it's a bad habit to build: the identical
code in problem 8 (Level Order Traversal) would output every level **backwards**. Enqueue left
first, always, so the muscle memory is right when order matters.

**(5)** `s/n` — **`/` not `//`.** The problem wants a float average; `29/2 = 14.5`, whereas
`29//2 = 14` would be wrong. This is one of the few places where `/` is the correct choice —
see [Python §4](./01-python-for-dsa.md).

### Complexity
- **Time O(n)** with a `deque`; **O(n²)** as written, because of `pop(0)`.
- **Space O(w)** — the widest level, up to n/2.

### Try next
[Binary Tree Level Order Traversal (next)](https://leetcode.com/problems/binary-tree-level-order-traversal/) ·
[Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) — take the last node of each level ·
[Maximum Level Sum of a Binary Tree](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/)

---

## 8. Binary Tree Level Order Traversal

**[LeetCode 102 →](https://leetcode.com/problems/binary-tree-level-order-traversal/)** · Medium · BFS · [`42-Level_order_traversal_bt.py`](../42-Level_order_traversal_bt.py)

### In one line
Return the node values grouped by level.

```
[3,9,20,null,null,15,7] → [[3],[9,20],[15,7]]
```

### Recognise it
**The** BFS template. Master this one and Right Side View, Zigzag Traversal, Maximum Level Sum,
and half a dozen others are trivial variations.

### The code

```python
class Solution:
    def levelOrder(self, root) -> List[List[int]]:
        if not root:
            return []

        ans = []
        q = [root]

        while q:
            level_size = len(q)           # (1)
            level = []
            for i in range(level_size):
                node = q.pop(0)           # (2)
                level.append(node.val)
                if node.left:             # (3)
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            ans.append(level)             # (4)
        return ans
```

**(1)** The snapshot, with a better name than problem 7's `n`.

**(2)** Same `pop(0)` performance issue — use `deque.popleft()`.

**(3)** **Left before right — and here it genuinely matters.** Level order means left to right.
Reversing these two lines gives `[[3],[20,9],[7,15]]`, a wrong answer. (Problem 7 got away with
it only because summation is order-independent.)

The `if node.left:` guards prevent `None`s entering the queue, which would crash `node.val` on
the next round.

**(4)** One list per level.

### Complexity
- **Time O(n)** with `deque`.
- **Space O(w)** for the queue, plus O(n) for the output.

### The variations, for free
```python
ans.append(level[::-1] if len(ans) % 2 else level)   # Zigzag (LC 103)
ans.append(level[-1])                                # Right Side View (LC 199)
ans.append(max(level))                               # Largest Value per Row (LC 515)
return ans[::-1]                                     # Bottom-Up Order (LC 107)
```
One template, four accepted solutions. This is what "learn patterns, not problems" means.

### Try next
[Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) ·
[Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) ·
[Populating Next Right Pointers in Each Node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/)

---

## 9. Lowest Common Ancestor of a Binary Tree

**[LeetCode 236 →](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)** · Medium · DFS with bubbling · [`47-LCA.py`](../47-LCA.py)

> ⚠️ **This file raised `NameError`** — the recursive calls were missing `self.`. Fixed; see
> [bugs-found.md §5](./bugs-found.md).

### In one line
The deepest node that has both `p` and `q` as descendants (a node may be its own ancestor).

### Recognise it
"Lowest common ancestor" in a **general** binary tree — no BST ordering to exploit. The
solution is six lines and genuinely elegant; it repays understanding rather than memorising.

### Intuition
Recurse and let information **bubble up**. Each call returns "what did I find in my subtree?":

- Found nothing → `None`
- Found `p` or `q` → return that node
- Found **both** (one from each side) → **this node is the LCA**; return it

The clever part: once a subtree returns a non-`None` node, every ancestor just passes it along
untouched — unless *both* of its children returned something, in which case it is the split
point and returns itself.

**Why returning early at `root == p` is correct** even without checking whether `q` is below:
if `q` *is* in `p`'s subtree, then `p` is the LCA (a node is its own ancestor). If `q` is
elsewhere, `p` bubbles up and meets `q`'s branch at the true split point. Both cases work; you
never need to look deeper.

### Dry run — tree `[3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 1`

| node | left returns | right returns | action |
|---|---|---|---|
| 6 | None | None | None |
| 7, 4 | | | None each |
| 2 | None | None | None |
| **5** | — | — | **`root == p` → return 5** (early) |
| 0, 8 | | | None |
| **1** | — | — | **`root == q` → return 1** |
| **3** | **5** | **1** | both non-None → **return 3** ✓ |

### The code (fixed)

```python
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        if not root or root == p or root == q:
            return root                                    # (1)

        l = self.lowestCommonAncestor(root.left, p, q)      # (2)
        r = self.lowestCommonAncestor(root.right, p, q)

        if l and r:                                        # (3)
            return root
        return l or r                                      # (4)
```

**(1)** Three base cases in one line: empty subtree (returns `None`), or we've found `p` or `q`
(return it and stop descending).

`==` on `TreeNode` objects compares **identity**, which is what we want — LeetCode passes the
actual node objects. Comparing `.val` would break on trees with duplicate values.

**(2)** ⚠️ **`self.`** — these were bare calls, which raise `NameError` because a method is not
a module-level function. See [bugs-found.md §5](./bugs-found.md). Defining an inner helper
closure sidesteps the issue entirely, which is why so many solutions do that.

**(3)** **The split point.** `p` came up one side and `q` the other, so this is the deepest node
containing both. Return it, and (4) at every ancestor will pass it up unchanged.

**(4)** `return l or r` — Python's `or` returns the **first truthy operand**, or the last one if
all are falsy. So this reads as: "whichever side found something, or `None` if neither did."
It's three cases in four characters. See [Python §11](./01-python-for-dsa.md).

### Complexity
- **Time O(n)** — each node visited at most once.
- **Space O(h)**.

### The BST version is simpler
When the tree is a **BST** ([LC 235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)),
you can navigate instead of searching: if both `p` and `q` are smaller than the current node, go
left; if both larger, go right; otherwise they've split and you're at the LCA. **O(h) time, no
full traversal.** Tomorrow's problems lean on exactly this ordering property.

### Try next
[LCA of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) ·
[LCA of a Binary Tree III](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/) (with parent pointers) ·
[Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

---

## 10. Validate Binary Search Tree `LC-98`

**[LeetCode 98 →](https://leetcode.com/problems/validate-binary-search-tree/)** · Medium · DFS with bounds · *new*

### In one line
Is this a valid BST? Every node's **entire** left subtree must be smaller, and its **entire**
right subtree larger.

```
    5
   / \      → False!   3 is in 5's right subtree, so it must be > 5
  1   4
     / \
    3   6
```

### Recognise it
The problem is designed around one specific wrong answer, and it's the one nearly everyone
writes first.

### Intuition — the trap
The natural attempt:

```python
# WRONG
return node.left.val < node.val < node.right.val and validate(left) and validate(right)
```

This only checks **immediate** children. In the tree above, node 4 has children 3 and 6, and
`3 < 4 < 6` ✓ locally. But 3 sits in the right subtree of 5, so it must be greater than 5 —
and it isn't. The local check misses it entirely.

**The fix:** a node's valid range is constrained by *every* ancestor, not just its parent.
Carry `(low, high)` bounds down the recursion:

- Going **left**, the upper bound tightens to the current node's value.
- Going **right**, the lower bound tightens to the current node's value.

### Dry run — the broken tree above

| node | valid range | check | result |
|---|---|---|---|
| 5 | (−∞, +∞) | −∞ < 5 < +∞ | ok |
| 1 | (−∞, 5) | −∞ < 1 < 5 | ok |
| 4 | (5, +∞) | 5 < 4? **no** | **False** |

Caught at node 4 — the ancestor bound from node 5 propagated down two levels, which is exactly
what the local check couldn't do.

### The code

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node, low, high):                 # (1)
            if not node:
                return True                            # (2)

            if not (low < node.val < high):            # (3)
                return False

            return validate(node.left, low, node.val) and \
                   validate(node.right, node.val, high)     # (4)

        return validate(root, float('-inf'), float('inf'))  # (5)
```

**(1)** The helper carries the bounds. The public method can't, so an inner function is the
clean way to add parameters.

**(2)** An empty subtree is vacuously a valid BST.

**(3)** **Chained comparison** — `low < node.val < high` means `low < node.val and node.val < high`,
with `node.val` evaluated once. Strict `<` on both sides because BSTs here contain **no
duplicates**; `<=` would wrongly accept them.

**(4)** **The bound tightening — the heart of the solution.**

- Left child: range becomes `(low, node.val)` — everything left must stay below this node.
- Right child: range becomes `(node.val, high)` — everything right must stay above it.

The old bound is *carried through* as well, which is what propagates ancestor constraints
arbitrarily far down.

**(5)** Start unbounded. `float('-inf')` and `float('inf')` compare correctly against any
integer, so the root is unconstrained — see [Python §7](./01-python-for-dsa.md).

*(Aside: if node values could be `float('inf')` you'd use `None` as the sentinel and test
`low is None or low < node.val`. LeetCode's constraints are within int range, so `inf` is safe.)*

### The in-order alternative — also worth knowing
**In-order traversal of a valid BST produces sorted output.** So:

```python
def isValidBST(self, root):
    self.prev = None
    def inorder(node):
        if not node:
            return True
        if not inorder(node.left):
            return False
        if self.prev is not None and node.val <= self.prev:   # <= catches duplicates
            return False
        self.prev = node.val
        return inorder(node.right)
    return inorder(root)
```
Same O(n)/O(h) complexity. The bounds version is easier to explain; the in-order version
generalises to "kth smallest in a BST" and "minimum absolute difference in a BST".

### Complexity
- **Time O(n)** — each node checked once. Short-circuits on the first violation.
- **Space O(h)**.

### Try next
[Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) (in-order + counter) ·
[Recover Binary Search Tree](https://leetcode.com/problems/recover-binary-search-tree/) ·
[Binary Search Tree Iterator](https://leetcode.com/problems/binary-search-tree-iterator/)

---

## Recall drill

1. Write the universal tree-DFS template. What are the two things you must always write first?
2. Why is minimum depth **not** just maximum depth with `min` instead of `max`?
3. In BFS, what does `for _ in range(len(q))` accomplish, and what breaks without it?
4. In Diameter, why does the function *return* `max(left,right)+1` but *record* `left+right`?
5. Why does checking only `left.val < node.val < right.val` fail to validate a BST?

<details>
<summary>Answers</summary>

1. ```python
   def dfs(node):
       if not node:
           return identity
       left  = dfs(node.left)
       right = dfs(node.right)
       return combine(left, right, node.val)
   ```
   First: the **base case** (`if not node`). Second: the **identity value** it returns — 0 for
   counts and depths, `True` for universal conditions, `None` for node-returning problems.
2. Because a node with only one child would take `min(depth, 0) + 1` and report that the path
   ends there — but a **leaf has no children at all**, so the path must continue down the
   non-empty side. Max depth has no equivalent trap because the 0 from a missing child never
   wins a `max`.
3. It **snapshots the number of nodes on the current level before any children are enqueued**,
   so exactly one level is processed per outer iteration. Without it the loop consumes newly
   added children too, levels bleed together, and you get a flat traversal instead of grouped
   levels.
4. The parent needs your **height** to compute its own answer — it can only descend through you
   one way, so it needs the deeper single branch. But the longest path *through* you goes down
   both sides, `left + right`, and no ancestor can use that. So it's recorded on the side
   rather than returned.
5. Because it only checks **immediate** children. A node's valid range is constrained by
   **every ancestor**: in `5 → right 4 → left 3`, the 3 is locally fine under 4 but must also be
   greater than 5. The fix is to pass `(low, high)` bounds down, tightening `high` when
   descending left and `low` when descending right.

</details>

---

**Tomorrow:** [Day 7 — BST, Graphs, Backtracking & DP](./day-7-bst-graphs-backtracking-dp.md).
The final day ties everything together and reveals the biggest connection in the guide:
**backtracking is DFS on a tree that doesn't exist yet.** You already know how to write it.

**Warm-up:** re-solve **Maximum Depth** and **Level Order Traversal** from a blank screen.
