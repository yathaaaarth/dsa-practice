# Complexity — How to Derive It, Not Memorise It

Every problem in this guide states a time and space cost *with the derivation*. This page
teaches you to produce those derivations yourself, which is what an interviewer is actually
testing when they ask "what's the complexity?"

---

## What Big-O means

Big-O describes **how the work grows as the input grows**, ignoring constants and
lower-order terms. `3n + 100` and `n` are both O(n): if you double the input, both roughly
double.

Two things this deliberately throws away:

- **Constants.** Two passes over the array is still O(n). An interviewer will not care that
  you saved one pass; they will care if you turned O(n²) into O(n).
- **Small inputs.** O(n²) can beat O(n log n) for n = 10. Big-O is about the trend.

---

## Deriving time complexity — five rules

### Rule 1: sequential blocks add, and the biggest wins

```python
for x in nums: ...      # O(n)
for x in nums: ...      # O(n)
```
O(n) + O(n) = O(2n) = **O(n)**.

```python
arr.sort()              # O(n log n)
for x in arr: ...       # O(n)
```
O(n log n) + O(n) = **O(n log n)**. The sort dominates. This is `13-Minimum_Absolute_diff.py`.

### Rule 2: nested loops multiply

```python
for i in range(n):
    for j in range(n):
```
**O(n²)**.

But look at the *bounds*, not the nesting depth:

```python
for i in range(n):
    for j in range(i, n):      # runs n, then n-1, then n-2 ...
```
n + (n−1) + … + 1 = n(n+1)/2 = **still O(n²)**. Halving a quadratic leaves a quadratic.

And the reverse — nesting that is *not* quadratic:

```python
while right < len(nums):        # right advances n times total
    ...
    while total >= target:      # left advances n times TOTAL, across all iterations
        left += 1
```
This is `14-Minimum_size_subarray_sum.py`. Two nested `while`s, but **O(n)**: each pointer
moves at most n times over the whole run, so the total work is 2n. This is called
**amortised** analysis, and it is the reason sliding window is fast. When you see nested
loops, ask *"how many times does the inner variable move in total?"* — not *"how many times
per outer iteration?"*

### Rule 3: halving the range gives log n

```python
while lo <= hi:
    mid = (lo + hi) // 2
    ...                        # then discard half
```
n → n/2 → n/4 → … → 1 takes log₂n steps. **O(log n)**.

log₂(1,000,000) ≈ 20. This is why binary search feels like magic: a million-element array
in 20 comparisons.

### Rule 4: for recursion, count the nodes of the recursion tree

Total work = (number of calls) × (work per call).

```python
def dfs(node):                 # each node visited once
    dfs(node.left)
    dfs(node.right)
```
n nodes × O(1) each = **O(n)**.

```python
def backtrack(start, path):
    result.append(path)
    for i in range(start, len(nums)):
        backtrack(i + 1, path + [nums[i]])
```
Each element is either in a subset or not → 2ⁿ subsets. Building each costs O(n) to copy.
**O(n · 2ⁿ)**. That is `22-Subsets.py`.

For permutations: n choices, then n−1, then n−2 → n! leaves, O(n) to build each →
**O(n · n!)**.

### Rule 5: know what the built-ins cost

| Operation | Cost | |
|---|---|---|
| `x in list` | O(n) | the classic accidental O(n²) |
| `x in set` / `x in dict` | O(1) avg | |
| `list.append(x)` | O(1) amortised | |
| `list.pop()` | O(1) | from the end |
| `list.pop(0)` | **O(n)** | shifts everything left |
| `list.insert(0, x)` | **O(n)** | same reason |
| `sorted()` / `.sort()` | O(n log n) | Timsort |
| `heappush` / `heappop` | O(log n) | |
| `heapify` | **O(n)** | not O(n log n) — a common misconception |
| `s[a:b]` slice | O(b−a) | it allocates |
| `"".join(parts)` | O(total) | |
| `s += t` in a loop | **O(n²)** | strings are immutable; each `+=` copies |
| `min(a, b)` | O(1) | |
| `min(iterable)` | O(n) | |

---

## Deriving space complexity

Count **extra** memory you allocate. The input itself doesn't count (it was already there);
what you build does.

```python
seen = set()          # can grow to n elements  -> O(n)
ans = [0] * n         # -> O(n)
l, r = 0, len(nums)-1 # two ints                -> O(1)
```

**Three things people forget:**

**1. The recursion stack is space.** Every pending call holds a frame.

```python
def dfs(node):
    dfs(node.left); dfs(node.right)
```
Space is O(h) where h is the tree height — **O(log n)** for a balanced tree, **O(n)** for a
degenerate one (a linked list). Always state which: "O(h), which is O(n) worst case."

**2. Output space is usually excluded** — but say so. Subsets returns 2ⁿ lists; you report
"O(n) auxiliary space, not counting the O(n·2ⁿ) output". Being explicit is the mark of
someone who has thought about it.

**3. Slices allocate.** `nums[i+1:]` inside a recursion is O(n) space *per level*.

---

## The ladder — get a feel for the numbers

For n = 1,000,000, at roughly 10⁸ simple operations per second:

| Complexity | Operations | Feels like | Typical source |
|---|---|---|---|
| O(1) | 1 | instant | hash lookup, arithmetic |
| O(log n) | 20 | instant | binary search, balanced-tree descent |
| O(n) | 10⁶ | ~0.01 s | one pass, hash map, sliding window |
| O(n log n) | 2×10⁷ | ~0.2 s | sorting, heap of n |
| O(n²) | 10¹² | **~3 hours** | nested loops |
| O(2ⁿ) | astronomically large | never | subsets, naive recursion |
| O(n!) | worse | never | permutations |

**Reading the constraints tells you the intended complexity.** This is a genuinely useful
exam trick:

| `n` up to | Intended solution |
|---|---|
| 10¹⁸ | O(log n) or O(1) — maths or binary search |
| 10⁶ – 10⁸ | O(n) or O(n log n) |
| 10⁵ | O(n log n), sometimes O(n √n) |
| ~5,000 | O(n²) is fine |
| ~500 | O(n³) is fine |
| ~20 | **O(2ⁿ)** — they want backtracking or bitmask DP |
| ~10 | O(n!) — permutations |

If a problem says `1 <= nums.length <= 20`, it is *telling* you to enumerate subsets. If it
says `10^5`, an O(n²) double loop will time out and you need the hash-map or two-pointer
version.

---

## Worked examples from this repo

**`01-Duplicate_value.py`**
```python
seen = set()                 # O(n) space
for num in nums:             # n iterations
    if num in seen:          # O(1) each -- because it is a SET
        return True
    seen.add(num)            # O(1)
```
n × O(1) = **O(n) time, O(n) space.** Swap `set()` for `[]` and it becomes O(n²) with no
other change — that is the whole lesson.

**`02-Missing_number.py`**
```python
sum_n = n * (n + 1) // 2     # O(1)
for i in range(n):           # O(n)
    sum_arr += nums[i]
```
**O(n) time, O(1) space** — strictly better than the set version, which is O(n) space. Same
time, less memory, because it exploits a mathematical property instead of storing anything.

**`10-Square-sorted_array.py`**
```python
while left <= right:         # the two pointers together cover n positions
```
Each iteration moves exactly one pointer, and they meet after n steps. **O(n) time**,
**O(n) space** for the output array (unavoidable — you must return n squares). Compare with
`sorted(x*x for x in nums)`: also correct, but O(n log n). The two-pointer version exploits
the fact that the input is already sorted.

**`16-Coin_change.py`**
```python
for a in range(1, amount + 1):      # `amount` iterations
    for c in coins:                 # len(coins) iterations
```
**O(amount × len(coins)) time, O(amount) space.** Note this is *not* O(n²) in the array
length — the complexity is driven by the numeric value of `amount`, which is why this is
called *pseudo-polynomial*. Worth saying out loud; it impresses.

**`22-Subsets.py`**
2ⁿ subsets, O(n) to build each → **O(n · 2ⁿ) time**. Space: O(n) for the recursion depth
plus the path, O(n · 2ⁿ) if you count the output.

---

## What to say in an interview

Not: *"it's O(n)."*

But: *"It's O(n) time — one pass, and each lookup is O(1) because `seen` is a hash set.
O(n) space in the worst case, when every element is distinct and ends up in the set. I'm
trading memory for time; the alternative is sorting first, which is O(1) extra space but
O(n log n) time."*

Three sentences: the number, the reason, the trade-off. That is a complete answer.
