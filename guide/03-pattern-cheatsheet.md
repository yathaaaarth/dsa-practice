# The Pattern Cheat Sheet

This is the page that turns 70 solved problems into hundreds of solvable ones. Keep it open
while you practise. By Sunday you should be able to reconstruct most of it from memory.

---

## Part 1 — Trigger phrases

Read the problem statement looking for these. The phrase on the left is a very strong hint
for the pattern on the right.

| The problem says… | Reach for | Day |
|---|---|---|
| "contains duplicate", "have we seen", "first repeating" | **Hash set** | 1 |
| "two numbers that sum to", "find the pair" | **Hash map** (complement lookup) | 1 |
| "anagram", "frequency", "how many times" | **Counter / hash map** | 1 |
| "appears twice except one", "single number", constant space | **XOR** | 1 |
| "**sorted** array" + find a pair/triple | **Two pointers**, from both ends | 2 |
| "contiguous **subarray**" / "**substring**" | **Sliding window** | 2 |
| "minimum length subarray with sum ≥ …" | **Variable-size sliding window** | 2 |
| "subarray of size exactly k" | **Fixed-size sliding window** | 2 |
| "maximum subarray sum" | **Kadane** | 2 |
| "sum of range i..j", asked repeatedly | **Prefix sum**, precomputed | 2 |
| "**sorted** array" + find a value/boundary | **Binary search** | 3 |
| "minimum/maximum X such that P(X) is true" | **Binary search on the answer** | 3 |
| "kth largest / smallest", "top k" | **Heap of size k** | 3 |
| "median from a stream" | **Two heaps** | 3 |
| "matching / nesting / valid parentheses" | **Stack** | 4 |
| "**next greater** / next warmer / next smaller" | **Monotonic stack** | 4 |
| "undo", "most recent", "evaluate an expression" | **Stack** | 4 |
| "cycle in a linked list", "middle node" | **Fast & slow pointers** | 5 |
| "reverse a list / part of a list" | **Three-pointer reversal** | 5 |
| "the head might change" | **Dummy node** | 5 |
| "level by level", "shortest path in an unweighted graph" | **BFS with a queue** | 6 |
| "depth", "path from root", "does a path exist" | **DFS / recursion** | 6 |
| "in a BST" | **Binary search on the tree** (left < node < right) | 6-7 |
| "sorted order out of a BST" | **In-order traversal** | 6-7 |
| "islands", "connected regions", "flood fill" | **Grid BFS/DFS** + visited set | 7 |
| "**all** combinations / permutations / subsets" | **Backtracking** | 7 |
| n ≤ 20 in the constraints | **Backtracking** (2ⁿ is affordable) | 7 |
| "how many ways to…", "minimum cost to reach…" | **DP** | 7 |
| "can I make amount X from these coins" | **Unbounded-knapsack DP** | 7 |
| "prerequisites", "ordering", "is it possible to finish" | **Topological sort** | 7+ |

---

## Part 2 — The templates

Learn these ten shapes. Almost everything else is a variation.

### 1. Hash set — "have I seen this?"

```python
seen = set()
for x in nums:
    if x in seen:
        return True
    seen.add(x)
return False
```
**O(n) time, O(n) space.** Solves: Contains Duplicate, Longest Consecutive Sequence,
Happy Number, Intersection of Two Arrays.

### 2. Hash map — "have I seen the thing that completes this?"

```python
seen = {}                       # value -> index
for i, x in enumerate(nums):
    if target - x in seen:      # look for the COMPLEMENT, not the value
        return [seen[target - x], i]
    seen[x] = i
```
**O(n) time, O(n) space.** The insight: instead of asking "is there a pair", ask, for each
element, "have I already passed the exact partner I need?" One pass replaces the double
loop. Solves: Two Sum, Subarray Sum Equals K, Isomorphic Strings.

### 3. Two pointers — opposite ends of a **sorted** array

```python
l, r = 0, len(nums) - 1
while l < r:
    total = nums[l] + nums[r]
    if total == target:  return [l, r]
    elif total < target: l += 1      # need a bigger sum -> move the small end up
    else:                r -= 1      # need a smaller sum -> move the big end down
```
**O(n) time, O(1) space.** Sortedness is what makes the discard sound: if the sum is too
small, no pair using `nums[l]` can work, so `l` is gone forever. Solves: Two Sum II, 3Sum,
Container With Most Water, Valid Palindrome, Squares of a Sorted Array (from the outside in).

### 4. Sliding window — contiguous run, variable size

```python
left = 0
window = 0                       # whatever you're tracking: sum, count, set...
best  = float('inf')
for right in range(len(nums)):
    window += nums[right]        # GROW: absorb the new right element
    while window >= target:      # SHRINK while the window is valid/invalid
        best = min(best, right - left + 1)
        window -= nums[left]     # remove the left element before moving left
        left += 1
return 0 if best == float('inf') else best
```
**O(n) time, O(1) space** — each pointer moves at most n times *in total*. The two nested
loops are not O(n²); see `02-complexity.md` Rule 2. Solves: Minimum Size Subarray Sum,
Longest Substring Without Repeating Characters, Longest Repeating Character Replacement,
Permutation in String.

The one decision: **when do I shrink?** Shrink while the window is *valid* if you want the
smallest valid window; shrink while it is *invalid* if you want the largest valid one.

### 5. Binary search — on an index

```python
lo, hi = 0, len(nums) - 1        # INCLUSIVE bounds
while lo <= hi:                  # <= because lo == hi is still a live candidate
    mid = (lo + hi) // 2
    if nums[mid] == target: return mid
    elif nums[mid] < target: lo = mid + 1   # the +1/-1 guarantee progress
    else:                    hi = mid - 1
return -1                        # or `lo`, which is the insertion point
```
**O(log n) time, O(1) space.** Two things cause every binary-search bug: mismatched bounds
(`<` vs `<=`), and forgetting `mid ± 1`, which makes the loop spin forever. Pick the
inclusive form above and use it every single time.

### 6. Binary search on the **answer**

When the answer is a number in a range, and "is X good enough?" is easy to check and
**monotonic** (if X works, everything bigger works):

```python
lo, hi = 1, max(candidates)
while lo < hi:                   # < , and hi = mid, converges on the FIRST true
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid       # mid works -- keep it, try smaller
    else:             lo = mid + 1   # mid fails -- discard it
return lo
```
**O(n log(range)).** This is the highest-leverage idea in the whole guide. Solves: Koko
Eating Bananas, Capacity to Ship Packages, Split Array Largest Sum, Minimum Speed to Arrive
on Time — a whole family that looks impossible until you see it.

### 7. Heap — "top k"

```python
import heapq
h = []
for x in nums:
    heapq.heappush(h, x)
    if len(h) > k:
        heapq.heappop(h)         # evict the smallest -> the heap keeps the k largest
return h[0]                      # the kth largest
```
**O(n log k) time, O(k) space.** Beats sorting's O(n log n) when k ≪ n. `heapq` is a
**min**-heap; for a max-heap push `-x`. Solves: Kth Largest Element, Top K Frequent,
K Closest Points, Merge K Sorted Lists.

### 8. Monotonic stack — "next greater element"

```python
stack = []                       # holds INDICES; values in it stay decreasing
res = [0] * len(nums)
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:    # x is the answer for everything smaller
        j = stack.pop()
        res[j] = i - j
    stack.append(i)
return res
```
**O(n) time, O(n) space** — each index is pushed once and popped once, so the inner `while`
is O(n) *in total*. Solves: Daily Temperatures, Next Greater Element I/II, Largest Rectangle
in Histogram, Trapping Rain Water.

### 9. Fast & slow pointers (linked list)

```python
slow = fast = head
while fast and fast.next:        # check BOTH: fast.next.next must be legal
    slow = slow.next             # 1 step
    fast = fast.next.next        # 2 steps
    if slow == fast: return True # they met -> there is a cycle
return slow                      # when fast falls off the end, slow is the middle
```
**O(n) time, O(1) space.** One traversal answers "middle?" and "cycle?" with no extra
memory. Solves: Middle of the Linked List, Linked List Cycle I/II, Palindrome Linked List,
Remove Nth Node From End.

### 10. Linked-list reversal

```python
prev, curr = None, head
while curr:
    nxt = curr.next          # SAVE the rest of the list before you destroy the link
    curr.next = prev         # flip the arrow backwards
    prev = curr              # both pointers step forward
    curr = nxt
return prev                  # curr is None; prev is the new head
```
**O(n) time, O(1) space.** The `nxt` save is the whole trick: `curr.next = prev` erases your
only route to the rest of the list, so you must grab it first.

### 11. Tree DFS (recursion)

```python
def dfs(node):
    if not node:                       # base case FIRST, always
        return 0                       # the identity for whatever you're combining
    left  = dfs(node.left)
    right = dfs(node.right)
    return combine(left, right, node.val)
```
**O(n) time, O(h) space** for the call stack — O(log n) balanced, O(n) skewed. Change only
`combine` and you get: max depth (`max+1`), min depth, diameter, path sum, same tree, invert,
LCA, validate BST.

### 12. Tree BFS (level order)

```python
from collections import deque
q, out = deque([root]), []
while q:
    level = []
    for _ in range(len(q)):        # snapshot the size FIRST -- q grows inside the loop
        node = q.popleft()
        level.append(node.val)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    out.append(level)
```
**O(n) time, O(w) space** (w = widest level, up to n/2). `for _ in range(len(q))` is the
entire trick that separates the levels. Solves: Level Order, Average of Levels, Right Side
View, Minimum Depth, Zigzag Traversal.

### 13. Grid BFS/DFS

```python
rows, cols = len(grid), len(grid[0])
visit = set()

def bfs(r, c):
    q = deque([(r, c)])
    visit.add((r, c))
    while q:
        row, col = q.popleft()
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols \
               and (nr, nc) not in visit and grid[nr][nc] == "1":
                visit.add((nr, nc))          # mark on ENQUEUE, not on dequeue
                q.append((nr, nc))
```
**O(rows × cols)** time and space. Marking on enqueue is what stops a cell being added twice.
Solves: Number of Islands, Max Area of Island, Rotting Oranges, Flood Fill, Walls and Gates.

### 14. Backtracking

```python
def backtrack(start, path):
    if is_complete(path):
        result.append(path[:])       # the [:] copy is MANDATORY if you mutate `path`
        return
    for choice in choices(start):
        path.append(choice)          # CHOOSE
        backtrack(start + 1, path)   # EXPLORE
        path.pop()                   # UN-CHOOSE  <-- this is the "backtracking"
```
**O(branching^depth)** — typically O(n·2ⁿ) for subsets, O(n·n!) for permutations. Backtracking
*is* DFS on a tree you never build. Solves: Subsets, Permutations, Combinations, Combination
Sum, Word Search, N-Queens, Palindrome Partitioning.

### 15. 1-D DP

```python
dp = [base] * (n + 1)          # dp[i] = the answer for input size i
dp[0] = known_answer
for i in range(1, n + 1):
    dp[i] = f(dp[i - 1], dp[i - 2], ...)      # the recurrence
return dp[n]
```
**O(n) time, O(n) space** — and O(1) space if the recurrence only looks back a fixed number
of steps (keep two variables instead of the array). The hard part is never the code, it is
writing down the recurrence. Solves: Climbing Stairs, House Robber, Coin Change, Min Cost
Climbing Stairs, Decode Ways.

---

## Part 3 — Decision flowchart

```
Is the input SORTED?
├─ yes → need a specific value or boundary?    → BINARY SEARCH
│        need a pair/triple summing to X?      → TWO POINTERS
│        need adjacent differences?            → one linear scan
└─ no  → could sorting help?  (costs n log n, often still a win)

Is it a CONTIGUOUS subarray / substring?       → SLIDING WINDOW
Is it "have I seen…" / counting / pairing?     → HASH SET or MAP
Is it "kth largest" / "top k"?                 → HEAP of size k
Is it "next greater/smaller"?                  → MONOTONIC STACK
Is it nesting / matching / evaluation?         → STACK
Is it a LINKED LIST?                           → FAST & SLOW, or DUMMY NODE
Is it a TREE?
├─ level by level, or shortest path            → BFS
├─ depth / paths / compare / transform         → DFS
└─ it's a BST (left < node < right)            → binary search the tree; in-order = sorted
Is it a GRID or GRAPH?                         → BFS/DFS + visited set
Is it "find ALL the ways/combinations"?        → BACKTRACKING
Is it "how MANY ways" or "min/max cost"?       → DP
Are there prerequisites / an ordering?         → TOPOLOGICAL SORT

None of the above?
→ Write the brute force. Name its cost.
→ Ask: "what am I recomputing?"    (repeated work → hash map, prefix sum, or DP)
→ Ask: "what can I discard?"       (a sound discard rule → two pointers or binary search)
```

---

## Part 4 — The five questions, in order

When you are stuck on something genuinely new:

1. **What is the brute force, and what does it cost?** You cannot optimise an unnamed cost.
2. **What am I recomputing?** Repeated *lookups* → hash map. Repeated *sums* → prefix sum.
   Repeated *subproblems* → DP or memoisation.
3. **What can I safely throw away?** If you can prove an element will never be part of the
   answer, you have a two-pointer or binary-search solution.
4. **Would sorting unlock a linear scan?** Paying O(n log n) to escape O(n²) is nearly
   always worth it.
5. **What do the constraints say?** n ≤ 20 means exponential is intended. n = 10⁵ means
   O(n²) will time out. The constraints are a hint, not decoration.
