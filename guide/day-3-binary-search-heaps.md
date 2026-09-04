# Day 3 — Binary Search & Heaps

> **Today's big idea:** two structures that turn "check everything" into "check log n
> things" or "keep only the k that matter". The original 50 problems in this repo contained
> **zero** binary search and **zero** heap problems — this is the largest gap in the set, and
> closing it unlocks a large share of LeetCode's Medium tier.

**Warm-up (10 min, blank screen):** re-solve Best Time to Buy and Sell Stock and Minimum
Size Subarray Sum.
**Reference:** [Python for DSA §10 (heapq)](./01-python-for-dsa.md) · [Complexity Rule 3](./02-complexity.md)

All ten problems today are new — you'll solve them directly on LeetCode. Today is the
heaviest day of the week. If you're short on time, problems 1, 2, 5, 6, 8 are the
non-negotiable core.

---

## Pattern primer

### Part A — Binary search on an index

The idea is trivial; the *implementation* is where everyone bleeds. Two things cause every
bug: mismatched loop bounds, and forgetting `mid ± 1`. **Pick one template and use it every
single time.**

```python
lo, hi = 0, len(nums) - 1        # INCLUSIVE bounds: hi is a real, searchable index
while lo <= hi:                  # <=  because lo == hi is still one live candidate
    mid = (lo + hi) // 2         # // not / -- indices must be ints
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        lo = mid + 1             # mid is ruled out, so +1 -- this GUARANTEES progress
    else:
        hi = mid - 1
return -1                        # not found. `lo` is where it WOULD go (insertion point)
```

**Why `mid + 1` and not `mid`:** if you write `lo = mid`, then when `hi == lo + 1` you get
`mid == lo`, and `lo = mid` changes nothing — **infinite loop**. The ±1 is what shrinks the
range every iteration.

**Why `<=` and not `<`:** with `<`, the loop exits while `lo == hi`, leaving one candidate
untested. On a single-element array you'd never look at it.

**The invariant to say out loud:** *"If the target exists, it is inside `[lo, hi]`."* Every
line must preserve that. When you're unsure whether to write `mid` or `mid ± 1`, ask: does
this preserve the invariant, and does the range definitely shrink?

**Two facts worth banking:**
- When the loop ends without a hit, `lo` is the **insertion point** — the index where the
  target belongs. Problems 2 and 3 are that fact wearing costumes.
- `mid = (lo + hi) // 2` rounds **down**, so `mid` can equal `lo` but never `hi` (when
  `lo < hi`). That asymmetry matters when you write the `lo < hi` variant below.

### Part B — Binary search on the **answer**

This is the highest-leverage idea of the week, and the one most people never learn.

Sometimes you're not searching an array — you're searching a **range of possible answers**.
It works when two conditions hold:

1. The answer is an integer in a known range `[lo, hi]`.
2. There's a **feasibility check** `feasible(x)` that is **monotonic**: if `x` works, then
   every larger `x` also works. (Or the mirror image.)

That monotonicity is a sorted boolean array — `F F F F T T T T` — and finding the first `T`
is binary search.

```python
lo, hi = min_possible, max_possible
while lo < hi:                   # <  and hi = mid: converges on the FIRST true
    mid = (lo + hi) // 2
    if feasible(mid):
        hi = mid                 # mid works -> keep it as a candidate, try smaller
    else:
        lo = mid + 1             # mid fails -> discard it
return lo                        # lo == hi == the smallest feasible answer
```

Note this is the **`lo < hi`** variant, not `lo <= hi`. Here `hi = mid` (not `mid - 1`)
because `mid` might *be* the answer. That's safe from infinite looping only because
`mid` rounds down and so `mid < hi` whenever `lo < hi`.

Recognise it from phrasing like *"minimum X such that…"*, *"minimum speed/capacity/time to
achieve…"*, *"smallest divisor such that the sum is at most…"*.

### Part C — Heaps

A heap is a binary tree kept in an array where **every parent is ≤ its children**. So the
minimum is always at index 0 — O(1) to peek — and inserting or removing costs O(log n)
because you only walk one root-to-leaf path.

```python
import heapq

h = []
heapq.heappush(h, x)      # O(log n)
heapq.heappop(h)          # O(log n) -- ALWAYS returns the minimum
h[0]                      # peek at the minimum, O(1)
heapq.heapify(lst)        # list -> heap IN PLACE, O(n)  (not O(n log n) -- worth knowing)
heapq.heappushpop(h, x)   # push then pop as one op, cheaper than doing both
```

**`heapq` is a min-heap only.** For a max-heap, negate going in and coming out:
```python
heapq.heappush(h, -val)
largest = -heapq.heappop(h)
```

**The size-k trick — "kth largest".** Keep a min-heap holding only the k largest elements
seen. The smallest thing in that heap is, by construction, the kth largest overall. When it
grows past k, pop the smallest.

```python
for x in nums:
    heapq.heappush(h, x)
    if len(h) > k:
        heapq.heappop(h)     # evict the smallest -> the k largest survive
return h[0]
```
**O(n log k)** — better than sorting's O(n log n) whenever k ≪ n, and it works on a stream
where sorting cannot.

*The direction confuses everyone at first:* to keep the **largest** k, you use a **min**-heap,
because you need cheap access to the *worst* of your current keepers to decide what to evict.

Copy all three templates out by hand.

---

## 1. Binary Search `LC-704`

**[LeetCode 704 →](https://leetcode.com/problems/binary-search/)** · Easy · Binary search · *new*

### In one line
Find `target` in a sorted array; return its index or −1.

```
nums = [-1,0,3,5,9,12], target = 9 → 4
```

### Recognise it
"Sorted array" + "find a value" + a constraint demanding better than O(n). This is the
template itself; get it exactly right today and the next nine problems are variations.

### Intuition
Look at the middle. Three cases: it's the target (done), it's too small (the target must be
in the right half), or it's too big (left half). Each comparison eliminates **half** the
remaining candidates, so n → n/2 → n/4 → … → 1 in log₂n steps. A million elements in 20
comparisons.

### Dry run — `nums = [-1,0,3,5,9,12]`, `target = 9`

| lo | hi | mid | `nums[mid]` | vs 9 | action |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 3 | < | `lo = 3` |
| 3 | 5 | 4 | 9 | **=** | **return 4** |

And a miss — `target = 2`:

| lo | hi | mid | `nums[mid]` | vs 2 | action |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 3 | > | `hi = 1` |
| 0 | 1 | 0 | -1 | < | `lo = 1` |
| 1 | 1 | 1 | 0 | < | `lo = 2` |
| 2 | 1 | — | — | — | `lo > hi` → **return −1** |

Note where `lo` finished: **2**, which is exactly where `2` would be inserted. Remember that
for the next problem.

### The code

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1        # (1)

        while lo <= hi:                  # (2)
            mid = (lo + hi) // 2         # (3)
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1             # (4)
            else:
                hi = mid - 1

        return -1                        # (5)
```

**(1)** `len(nums) - 1` makes `hi` an **inclusive** bound — a real index you're willing to
check. (The alternative convention, `hi = len(nums)` exclusive, needs `while lo < hi` and
`hi = mid`. Both are correct; mixing them is the bug factory. Pick inclusive and never
deviate.)

**(2)** `<=`. When `lo == hi` there is exactly one candidate left and it hasn't been tested.
Using `<` silently fails on single-element arrays.

**(3)** `//` — integer division. `/` gives a float and `nums[2.5]` raises `TypeError`.

In Java or C++ you'd write `lo + (hi - lo) // 2` to avoid `lo + hi` overflowing a 32-bit int.
Python integers are arbitrary precision so it can't overflow — but say the safer form aloud
in an interview; it signals you know the failure mode.

**(4)** `mid + 1`, not `mid`. We just proved `nums[mid] != target`, so `mid` is ruled out and
excluding it is both correct and *necessary*: `lo = mid` can leave the range unchanged and
loop forever.

**(5)** Not found. If you needed the insertion point instead, you'd `return lo` — see the
dry run.

### Complexity
- **Time O(log n)** — the range halves each iteration. See [Complexity Rule 3](./02-complexity.md).
- **Space O(1)** — three integers. (The recursive formulation is O(log n) space for the call
  stack; prefer iterative.)

### Try next
[Search Insert Position (next)](https://leetcode.com/problems/search-insert-position/) ·
[Guess Number Higher or Lower](https://leetcode.com/problems/guess-number-higher-or-lower/) ·
[Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/)

---

## 2. Search Insert Position `LC-35`

**[LeetCode 35 →](https://leetcode.com/problems/search-insert-position/)** · Easy · Binary search (lower bound) · *new*

### In one line
Return the index of `target`, or the index where it should be inserted to keep the array
sorted.

```
[1,3,5,6], target=5 → 2        [1,3,5,6], target=2 → 1        [1,3,5,6], target=7 → 4
```

### Recognise it
Same as problem 1, except a miss must return a *position* rather than −1. This teaches the
most useful fact about binary search.

### Intuition
No new algorithm at all. When the standard loop exits without a hit, `lo` has landed exactly
on the insertion point. Why?

The loop maintains: *everything strictly left of `lo` is `< target`, everything strictly
right of `hi` is `> target`*. When `lo > hi` those two regions meet, so `lo` is the first
index whose value is ≥ target — the definition of the insertion point.

Change `return -1` to `return lo`. That's the whole difference.

### Dry run — `nums = [1,3,5,6]`, `target = 2`

| lo | hi | mid | `nums[mid]` | vs 2 | action |
|---|---|---|---|---|---|
| 0 | 3 | 1 | 3 | > | `hi = 0` |
| 0 | 0 | 0 | 1 | < | `lo = 1` |
| 1 | 0 | — | — | — | exit → **return `lo` = 1** ✓ |

And `target = 7` (past the end):

| lo | hi | mid | `nums[mid]` | action |
|---|---|---|---|---|
| 0 | 3 | 1 | 3 < 7 | `lo = 2` |
| 2 | 3 | 2 | 5 < 7 | `lo = 3` |
| 3 | 3 | 3 | 6 < 7 | `lo = 4` |
| 4 | 3 | — | — | **return 4** = `len(nums)` ✓ |

### The code

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

        return lo                   # (1)
```

**(1)** The only changed line. `lo` can legitimately equal `len(nums)` — appending past the
end — which is correct, not an out-of-bounds bug.

### Complexity
**O(log n) time, O(1) space.**

### This is `bisect_left`
Python's standard library already has it:
```python
import bisect
return bisect.bisect_left(nums, target)
```
`bisect_left` gives the first index where the target could go (before any equal elements);
`bisect_right` gives the last (after them). Knowing these exist is genuinely useful in real
code, and knowing the difference is a common interview follow-up. Write the loop by hand
when asked to demonstrate the mechanism.

### Try next
[First Bad Version (next)](https://leetcode.com/problems/first-bad-version/) ·
[Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) ·
[Sqrt(x)](https://leetcode.com/problems/sqrtx/)

---

## 3. First Bad Version `LC-278`

**[LeetCode 278 →](https://leetcode.com/problems/first-bad-version/)** · Easy · Binary search on a predicate · *new*

### In one line
Versions `1..n`. After some point every version is bad. Find the first bad one, using as few
`isBadVersion(v)` calls as possible.

```
n = 5, first bad = 4  →  isBadVersion: [F,F,F,T,T]  →  answer 4
```

### Recognise it
**There is no array.** This is the bridge between "binary search an array" and "binary search
an answer": what you're searching is a sequence of booleans that is guaranteed to look like
`F F F T T T`. Sortedness of *values* was never the requirement — **monotonicity of a
predicate** is.

### Intuition
`isBadVersion` is monotonic: once true, always true. That's a sorted boolean array, and
finding the first `True` is binary search.

If `mid` is bad, the answer is `mid` **or something earlier** — so keep `mid` as a candidate
(`hi = mid`). If `mid` is good, the answer is strictly after it (`lo = mid + 1`).

### Dry run — `n = 5`, first bad = 4

| lo | hi | mid | `isBadVersion(mid)` | action |
|---|---|---|---|---|
| 1 | 5 | 3 | False | `lo = 4` |
| 4 | 5 | 4 | **True** | `hi = 4` |
| 4 | 4 | — | — | `lo == hi` → **return 4** |

Three API calls instead of five.

### The code

```python
class Solution:
    def firstBadVersion(self, n: int) -> int:
        lo, hi = 1, n                  # (1)

        while lo < hi:                 # (2)
            mid = (lo + hi) // 2
            if isBadVersion(mid):
                hi = mid               # (3)
            else:
                lo = mid + 1           # (4)

        return lo                      # (5)
```

**(1)** Versions are **1-indexed** — `lo = 1`, not 0. Read the problem statement for the
indexing base every time.

**(2)** **`<`, not `<=`.** This is the different template — the one that converges on a
boundary rather than hunting for an exact match. With `hi = mid` at (3), `lo <= hi` would
spin forever when `lo == hi`.

**(3)** `hi = mid`, **not** `mid - 1`. `mid` is bad, so it's a live candidate for "the first
bad one" — discarding it would lose the answer. This is the crucial asymmetry versus the
exact-match template.

**Why this can't loop forever:** `mid = (lo + hi) // 2` rounds down, so whenever `lo < hi`
we get `mid < hi`. Therefore `hi = mid` strictly decreases `hi`, and the range shrinks every
iteration.

**(4)** `mid` is good, so it definitively isn't the answer — safe to exclude with `+1`.

**(5)** The loop ends with `lo == hi`, and the invariant says the answer is in `[lo, hi]`.
Return either.

### Complexity
- **Time O(log n)** — log₂(2³¹) ≈ 31 API calls for the full integer range.
- **Space O(1)**.

### The template to bank
```python
while lo < hi:
    mid = (lo + hi) // 2
    if condition(mid): hi = mid       # keep mid -- it might be the answer
    else:              lo = mid + 1   # discard mid
return lo
```
"**Find the first X where `condition` becomes true.**" Problems 5 and 6 are this exact shape.

### Try next
[Koko Eating Bananas (problem 6)](https://leetcode.com/problems/koko-eating-bananas/) ·
[Find Peak Element](https://leetcode.com/problems/find-peak-element/) ·
[Find Minimum in Rotated Sorted Array (problem 5)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

---

## 4. Search a 2D Matrix `LC-74`

**[LeetCode 74 →](https://leetcode.com/problems/search-a-2d-matrix/)** · Medium · Binary search + index arithmetic · *new*

### In one line
Each row is sorted, and the first element of each row is greater than the last of the
previous. Find `target`.

```
[[1, 3, 5, 7],
 [10,11,16,20],   target = 3 → True
 [23,30,34,60]]
```

### Recognise it
The stated property means the matrix, **read row by row, is one fully sorted list**. Once you
see that, it's problem 1 with an index conversion.

### Intuition
Don't search rows then columns (that works, but it's two searches and more code). Instead
pretend the matrix is a flat array of length `m × n` and binary search *that*, converting
each flat index to a `(row, col)` pair on the fly:

```
row = idx // cols        # how many complete rows fit before idx
col = idx %  cols        # how far into the current row
```

Integer division and modulo are the standard 1-D ↔ 2-D conversion, and worth being fluent in
— they show up in grid problems constantly.

### Dry run — 3×4 matrix above, `target = 3`

Flat length = 12, so `lo = 0`, `hi = 11`.

| lo | hi | mid | row=mid//4 | col=mid%4 | value | vs 3 | action |
|---|---|---|---|---|---|---|---|
| 0 | 11 | 5 | 1 | 1 | 11 | > | `hi = 4` |
| 0 | 4 | 2 | 0 | 2 | 5 | > | `hi = 1` |
| 0 | 1 | 0 | 0 | 0 | 1 | < | `lo = 1` |
| 1 | 1 | 1 | 0 | 1 | 3 | **=** | **True** |

### The code

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])      # (1)
        lo, hi = 0, rows * cols - 1                   # (2)

        while lo <= hi:
            mid = (lo + hi) // 2
            value = matrix[mid // cols][mid % cols]   # (3)
            if value == target:
                return True
            elif value < target:
                lo = mid + 1
            else:
                hi = mid - 1

        return False
```

**(1)** `len(matrix)` is the row count; `len(matrix[0])` the column count. Constraints
guarantee at least one row, so `matrix[0]` is safe — check that guarantee before relying on it.

**(2)** The virtual flat array has `rows * cols` elements, so the last index is
`rows * cols - 1`. Inclusive bound, same convention as always.

**(3)** The conversion. `mid // cols` divides by the **row width** to get the row number;
`mid % cols` is the remainder, i.e. the column. Note it's `cols` in both — a very easy place
to write `rows` by mistake, and on a square matrix your tests would still pass.

### Complexity
- **Time O(log(m·n))** = O(log m + log n) — a single binary search over all cells.
- **Space O(1)**.

### The variant worth knowing
[Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) has rows and
columns each sorted, but **no** relationship between them — so the flat array isn't sorted
and this trick fails. There the answer is the *staircase* walk: start at the top-right
corner; if the value is too big move left, too small move down. **O(m + n)**, elegant, and a
common interview question.

### Try next
[Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) ·
[Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) ·
[Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/)

---

## 5. Find Minimum in Rotated Sorted Array `LC-153`

**[LeetCode 153 →](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)** · Medium · Binary search on a broken sort · *new*

### In one line
A sorted array was rotated at some unknown pivot. Find the minimum in O(log n).

```
[3,4,5,1,2] → 1        [4,5,6,7,0,1,2] → 0        [11,13,15,17] → 11 (not rotated)
```

### Recognise it
"Rotated sorted array" is its own small family. The array isn't sorted overall, but it's
made of **two sorted runs**, and you can always tell which one you're standing in.

### Intuition
Compare `nums[mid]` with `nums[hi]`:

- **`nums[mid] > nums[hi]`** — the values drop somewhere after `mid`, so the pivot (the
  minimum) is strictly to the **right**. Discard `mid`: `lo = mid + 1`.
- **`nums[mid] <= nums[hi]`** — everything from `mid` to `hi` is in order, so the minimum is
  `mid` or something to its **left**. Keep `mid`: `hi = mid`.

**Compare against `hi`, not `lo`.** Comparing with `lo` needs an extra case for the
not-rotated array (where `nums[mid] > nums[lo]` but there's no pivot to the right).
Comparing with `hi` handles it uniformly — that's the trick worth remembering.

### Dry run — `nums = [4,5,6,7,0,1,2]`

| lo | hi | mid | `nums[mid]` | `nums[hi]` | comparison | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | 2 | 7 > 2 | pivot is right → `lo = 4` |
| 4 | 6 | 5 | 1 | 2 | 1 ≤ 2 | sorted here → `hi = 5` |
| 4 | 5 | 4 | 0 | 1 | 0 ≤ 1 | sorted here → `hi = 4` |
| 4 | 4 | — | — | — | — | `lo == hi` → **return `nums[4]` = 0** |

### The code

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1

        while lo < hi:                     # (1)
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:       # (2)
                lo = mid + 1               # (3)
            else:
                hi = mid                   # (4)

        return nums[lo]                    # (5)
```

**(1)** `<`, the boundary-converging template again. We're not matching an exact value, we're
narrowing to a position — so `lo < hi` with `hi = mid`.

**(2)** Against `nums[hi]`, deliberately. See the intuition.

**(3)** `nums[mid] > nums[hi]` proves `mid` is in the *left* (higher) run, so it cannot be the
minimum — safe to exclude.

**(4)** `hi = mid`, **not** `mid - 1`. `mid` might *be* the minimum (it's the smallest thing
in a sorted stretch), so we must keep it.

**(5)** `lo == hi` and points at the minimum.

### Complexity
- **Time O(log n)** — with all-distinct values. (With duplicates — LeetCode 154 — the worst
  case degrades to O(n), because `nums[mid] == nums[hi]` tells you nothing and you can only
  do `hi -= 1`.)
- **Space O(1)**.

### Sanity checks
- Not rotated, `[1,2,3,4]`: every comparison takes the `else` branch, `hi` walks down to 0,
  returns `nums[0] = 1` ✓
- Single element `[5]`: the loop never runs, returns `nums[0]` ✓

### Try next
[Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) (the natural follow-up) ·
[Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) (with duplicates) ·
[Find Peak Element](https://leetcode.com/problems/find-peak-element/)

---

## 6. Koko Eating Bananas `LC-875`

**[LeetCode 875 →](https://leetcode.com/problems/koko-eating-bananas/)** · Medium · **Binary search on the answer** · *new*

> **If you learn one thing this week, learn this problem.** It looks nothing like a binary
> search until you see the trick, and then an entire family of "hard" problems becomes
> mechanical.

### In one line
Piles of bananas, `h` hours. At speed `k` bananas/hour, Koko finishes one pile per hour
(leftovers of a pile don't carry over). Find the minimum `k` that finishes within `h` hours.

```
piles = [3,6,7,11], h = 8 → 4
```

### Recognise it
**"Minimum X such that some condition holds."** Also: "minimum speed", "minimum capacity",
"smallest divisor", "least time". The moment you can write a function
`can_we_do_it_at(x) -> bool` that is monotonic, you have a binary search.

### Intuition
There is no array to search. But there *is* a range of possible answers: `k` is somewhere in
`[1, max(piles)]` — speed 1 is the slowest sensible, and eating the biggest pile in one hour
is the fastest useful.

Now the key observation: **if speed `k` works, then `k+1` also works.** Faster is never
worse. So the feasibility of each speed forms a monotonic sequence:

```
k:        1  2  3  4  5  6  7  ...
works?    F  F  F  T  T  T  T
                   ↑ we want this boundary
```

That's a sorted boolean array. Binary search it for the first `True`.

**Hours at speed k** = `sum(ceil(pile / k))` — ceiling, because a pile of 7 at speed 4 takes
2 hours (4 then 3), with the leftover hour wasted.

### Dry run — `piles = [3,6,7,11]`, `h = 8`

`lo = 1`, `hi = 11`

| lo | hi | mid (speed) | hours = Σ⌈pile/mid⌉ | ≤ 8? | action |
|---|---|---|---|---|---|
| 1 | 11 | 6 | 1+1+2+2 = 6 | yes | `hi = 6` |
| 1 | 6 | 3 | 1+2+3+4 = 10 | no | `lo = 4` |
| 4 | 6 | 5 | 1+2+2+3 = 8 | yes | `hi = 5` |
| 4 | 5 | 4 | 1+2+2+3 = 8 | yes | `hi = 4` |
| 4 | 4 | — | — | — | **return 4** |

### The code

```python
import math

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        lo, hi = 1, max(piles)                       # (1)

        def hours_needed(speed):                     # (2)
            return sum(math.ceil(p / speed) for p in piles)

        while lo < hi:                               # (3)
            mid = (lo + hi) // 2
            if hours_needed(mid) <= h:               # (4)
                hi = mid                             # (5)
            else:
                lo = mid + 1                         # (6)

        return lo                                    # (7)
```

**(1)** The search space. `lo = 1` — speed 0 would never finish. `hi = max(piles)` — any
faster is pointless, since Koko can't start a second pile in the same hour, so
`max(piles)` already achieves one-hour-per-pile. Defining tight, *justified* bounds is half
of solving these; state the reasoning aloud.

**(2)** The feasibility function. `math.ceil(p / speed)` rounds **up** — a partial pile still
costs a whole hour. The integer-only form is `(p + speed - 1) // speed`, which avoids float
imprecision on very large values and is worth knowing.

**(3)–(7)** The boundary template from problem 3, unchanged. `hi = mid` keeps a working
speed as a candidate; `lo = mid + 1` discards one that's too slow; `lo` is the first `True`.

### Complexity
- **Time O(n · log(max(piles)))** — each feasibility check is O(n) over the piles, and there
  are log(max) iterations. With n = 10⁴ and piles up to 10⁹, that's 10⁴ × 30 = 3×10⁵
  operations. Instant.
- **Space O(1)**.

Notice the shape: **O(n · log(range))**, not O(log n). You're paying a linear check per
binary-search step. That's the signature of answer-space binary search.

### The family this unlocks
Once you internalise "define the range, write `feasible()`, binary search the boundary", all
of these become the same problem:

| Problem | Search space | `feasible(x)` |
|---|---|---|
| [Capacity To Ship Packages in D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | `[max(w), sum(w)]` | days needed at capacity x ≤ D |
| [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | `[max(n), sum(n)]` | subarrays needed with cap x ≤ m |
| [Minimum Speed to Arrive on Time](https://leetcode.com/problems/minimum-speed-to-arrive-on-time/) | `[1, 10^7]` | travel time at speed x ≤ hour |
| [Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/) | `[1, max(nums)]` | sum of ⌈n/x⌉ ≤ threshold |
| [Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/) | `[1, max−min]` | can place m balls ≥ x apart |

Same six lines every time. Only `feasible` changes.

### Try next
All five in the table above. Do at least two.

---

## 7. Last Stone Weight `LC-1046`

**[LeetCode 1046 →](https://leetcode.com/problems/last-stone-weight/)** · Easy · Max-heap · *new*

### In one line
Repeatedly smash the two heaviest stones together (`y - x` remains, or nothing if equal).
Return what's left.

```
[2,7,4,1,8,1] → 1
```

### Recognise it
"Repeatedly take the largest/smallest, transform, put the result back." That loop is what a
heap is *for*. Re-sorting after each step would be O(n² log n); a heap makes each step
O(log n).

### Intuition
You need the two largest stones, repeatedly, from a collection that keeps changing. A heap
gives you the extreme in O(log n) and lets you insert the result in O(log n).

Python's `heapq` is a **min**-heap, so negate everything: the "smallest" negative is the
largest original. Negate again on the way out.

### Dry run — `stones = [2,7,4,1,8,1]`

Heap (negated): `[-8,-7,-4,-2,-1,-1]`

| pop 1 | pop 2 | y − x | push back | remaining (as positives) |
|---|---|---|---|---|
| 8 | 7 | 1 | −1 | `7,4,2,1,1` → wait: `4,2,1,1,1` |
| 4 | 2 | 2 | −2 | `2,1,1,1` |
| 2 | 1 | 1 | −1 | `1,1,1` |
| 1 | 1 | 0 | *nothing* | `1` |

One stone left → **1**

### The code

```python
import heapq

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = [-s for s in stones]        # (1)
        heapq.heapify(heap)                # (2)

        while len(heap) > 1:               # (3)
            first  = -heapq.heappop(heap)  # (4)
            second = -heapq.heappop(heap)
            if first != second:            # (5)
                heapq.heappush(heap, -(first - second))

        return -heap[0] if heap else 0     # (6)
```

**(1)** **Negate to simulate a max-heap.** `heapq` only does min-heaps; negating inverts the
ordering, so the numerically smallest negative is the largest original.

**(2)** `heapify` converts an existing list into a valid heap **in place, in O(n)** — not
O(n log n). This surprises people: building a heap bottom-up is genuinely linear, because
most nodes are near the leaves and sift down only a step or two. Pushing n items one at a
time *would* be O(n log n), so prefer `heapify` when you have the data upfront.

**(3)** `> 1` — we need two stones to smash. Ends with 1 or 0 stones.

**(4)** Pop returns the most-negative value; negating restores the true weight. Because the
heap is ordered, `first >= second` automatically — no comparison needed.

**(5)** Equal stones destroy each other, so nothing is pushed. Note: pushing `-0` would be
harmless in value but adds a phantom stone that breaks the count — the guard matters.

**(6)** `if heap else 0` — the heap can be empty if the last pair was equal.

### Complexity
- **Time O(n log n)** — O(n) to heapify, then up to n iterations each doing O(log n) work.
- **Space O(n)** for the heap.

### Try next
[Kth Largest Element in an Array (next)](https://leetcode.com/problems/kth-largest-element-in-an-array/) ·
[Minimum Cost to Connect Sticks](https://leetcode.com/problems/minimum-cost-to-connect-sticks/) ·
[Task Scheduler](https://leetcode.com/problems/task-scheduler/)

---

## 8. Kth Largest Element in an Array `LC-215`

**[LeetCode 215 →](https://leetcode.com/problems/kth-largest-element-in-an-array/)** · Medium · **Size-k min-heap** · *new*

### In one line
Find the kth largest element (in sorted order, not the kth distinct value).

```
[3,2,1,5,6,4], k = 2 → 5
```

### Recognise it
"kth largest", "kth smallest", "top k". This is *the* canonical heap problem, and the
size-k trick here is the one you'll reuse most.

### Intuition
Sorting gives `sorted(nums)[-k]` — correct, O(n log n), and a perfectly acceptable first
answer. But you don't need the whole order; you only need the **k largest**.

Keep a min-heap of size k holding the k largest elements seen so far. Then:

- The smallest thing in that heap (`heap[0]`) is the **kth largest overall**.
- When a new element arrives, push it; if the heap now exceeds k, pop the smallest — it can't
  be in the top k.

**Why a MIN-heap to track the LARGEST k?** Because the operation you perform constantly is
*eviction*, and you need cheap access to the **worst of your keepers** to know what to throw
away. The min-heap puts exactly that at index 0.

### Dry run — `nums = [3,2,1,5,6,4]`, `k = 2`

| element | push | `len > 2`? | pop | heap after | `heap[0]` |
|---|---|---|---|---|---|
| 3 | `[3]` | no | | `[3]` | 3 |
| 2 | `[2,3]` | no | | `[2,3]` | 2 |
| 1 | `[1,3,2]` | **yes** | 1 | `[2,3]` | 2 |
| 5 | `[2,3,5]` | **yes** | 2 | `[3,5]` | 3 |
| 6 | `[3,5,6]` | **yes** | 3 | `[5,6]` | 5 |
| 4 | `[4,6,5]` | **yes** | 4 | `[5,6]` | **5** |

→ **5** ✓ (The heap always holds the 2 largest seen; its minimum is the 2nd largest.)

### The code

```python
import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []                          # (1)

        for num in nums:
            heapq.heappush(heap, num)      # (2)
            if len(heap) > k:              # (3)
                heapq.heappop(heap)        # (4)

        return heap[0]                     # (5)
```

**(1)** A plain list. `heapq` operates *on* lists; there's no separate heap type.

**(2)** Push everything, unconditionally. O(log k), since the heap never exceeds k+1.

**(3)–(4)** The eviction. Once the heap holds k+1 elements, the smallest of them cannot be in
the top k, so drop it. This is what keeps the heap at size k and the complexity at O(n log k).

**(5)** `heap[0]` peeks at the minimum in **O(1)** without removing it — the kth largest.

### The one-liner
```python
return heapq.nlargest(k, nums)[-1]
```
`nlargest` does exactly this internally. Know it; write the loop when asked to show the
mechanism.

### Complexity
- **Time O(n log k)** — n pushes/pops, each O(log k) because the heap is capped at k.
  Compare with sorting's O(n log n). When k = 5 and n = 10⁶, log k ≈ 2 vs log n ≈ 20 — a
  10× win.
- **Space O(k)** — the heap only ever holds k elements. Sorting needs O(n).

**And the streaming argument:** if `nums` arrives as an infinite stream you *cannot* sort it,
but this works unchanged. That's the real reason the heap solution matters, and it's the
setup for the next problem.

### The O(n) average alternative
**Quickselect** — Quicksort's partition step, recursing into only the side containing the
answer — is O(n) *average*, O(n²) worst case. Mention it if asked to beat O(n log k); the
heap is what you should actually write.

### Try next
[Kth Largest Element in a Stream (next)](https://leetcode.com/problems/kth-largest-element-in-a-stream/) ·
[Top K Frequent Elements (problem 10)](https://leetcode.com/problems/top-k-frequent-elements/) ·
[K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)

---

## 9. Kth Largest Element in a Stream `LC-703`

**[LeetCode 703 →](https://leetcode.com/problems/kth-largest-element-in-a-stream/)** · Easy · Size-k min-heap (persistent) · *new*

### In one line
A class: initialised with `k` and a starting array, then `add(val)` returns the kth largest
**after** inserting `val`.

```
KthLargest(3, [4,5,8,2])
add(3) → 4     add(5) → 5     add(10) → 5     add(9) → 8     add(4) → 8
```

### Recognise it
Same as problem 8, but the data **keeps arriving** and you must answer after each arrival.
This is the case where the heap doesn't just beat sorting — sorting isn't an option at all.

### Intuition
Identical trick, made persistent. Store the size-k min-heap as an instance attribute. Each
`add` pushes, evicts if oversized, and returns `heap[0]`.

Sorting on every `add` would be O(n log n) per call. The heap makes it **O(log k)** — for
10⁴ calls and k = 3, that's about 2 operations per call instead of thousands.

### Dry run — `k = 3`, initial `[4,5,8,2]`

Constructor: push all four, keep the largest 3 → heap `[4,5,8]`, minimum 4.

| `add(val)` | push | size > 3? | pop | heap | return `heap[0]` |
|---|---|---|---|---|---|
| 3 | `[3,4,8,5]` | yes | 3 | `[4,5,8]` | **4** |
| 5 | `[4,5,8,5]` | yes | 4 | `[5,5,8]` | **5** |
| 10 | `[5,5,8,10]` | yes | 5 | `[5,8,10]` | **5** |
| 9 | `[5,8,10,9]` | yes | 5 | `[8,9,10]` | **8** |
| 4 | `[4,8,10,9]` | yes | 4 | `[8,9,10]` | **8** |

### The code

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k                              # (1)
        self.heap = nums                        # (2)
        heapq.heapify(self.heap)                # (3)
        while len(self.heap) > k:               # (4)
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)          # (5)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]                     # (6)
```

**(1)–(2)** `self.` makes both survive between calls — the whole point of a stateful class.
`self.heap = nums` aliases the caller's list rather than copying it; `heapify` will then
reorder *their* list in place. LeetCode doesn't care, but `list(nums)` is the polite version
and worth a comment in real code.

**(3)** O(n) heapify, better than n individual pushes.

**(4)** Trim down to exactly k. Note the initial array can be **shorter than k** — the
problem guarantees `add` will be called enough times to make it valid — so this `while` may
not run at all, and `heap[0]` in `add` is only reached once there are k elements.

**(5)** Push first, then trim. Ordering matters: the new value must be considered before you
decide what to evict.

**(6)** O(1) peek at the kth largest.

### Complexity
- **`__init__`: O(n + (n−k) log n)**, dominated by O(n log n) worst case.
- **`add`: O(log k)** — one push, one pop, on a k-element heap.
- **Space O(k)** — constant regardless of how long the stream runs. That's the property that
  makes this viable for unbounded input.

### Try next
[Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) — **two heaps**, the natural next step ·
[Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) ·
[Design Twitter](https://leetcode.com/problems/design-twitter/) (merge k streams with a heap)

---

## 10. Top K Frequent Elements `LC-347`

**[LeetCode 347 →](https://leetcode.com/problems/top-k-frequent-elements/)** · Medium · Hash map + heap · *new*

### In one line
Return the `k` most frequent elements.

```
nums = [1,1,1,2,2,3], k = 2 → [1,2]
```

### Recognise it
**Day 1 + Day 3 combined.** Counting is a hash map; "top k" is a heap. Most Medium problems
are two Easy patterns stacked, and recognising the seam is the skill.

### Intuition
Two phases:

1. **Count** with a `Counter` — O(n).
2. **Select the top k** by count, with a size-k min-heap keyed on frequency — O(m log k),
   where m is the number of distinct values.

The only new mechanic: the heap must order by **count** while you ultimately need the
**value**. Push tuples `(count, value)`; Python compares tuples element by element, so the
first component drives the ordering for free.

### Dry run — `nums = [1,1,1,2,2,3]`, `k = 2`

`counts = {1: 3, 2: 2, 3: 1}`

| entry pushed | heap (as `(count, val)`) | size > 2? | pop | heap after |
|---|---|---|---|---|
| `(3, 1)` | `[(3,1)]` | no | | `[(3,1)]` |
| `(2, 2)` | `[(2,2),(3,1)]` | no | | `[(2,2),(3,1)]` |
| `(1, 3)` | `[(1,3),(3,1),(2,2)]` | **yes** | `(1,3)` | `[(2,2),(3,1)]` |

Extract the values → `[2, 1]` (any order accepted).

### The code

```python
import heapq
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)                       # (1)

        heap = []
        for value, count in counts.items():          # (2)
            heapq.heappush(heap, (count, value))     # (3)
            if len(heap) > k:
                heapq.heappop(heap)                  # (4)

        return [value for count, value in heap]      # (5)
```

**(1)** `Counter(nums)` builds `{value: frequency}` in one O(n) pass — see
[Python §2](./01-python-for-dsa.md).

**(2)** `.items()` yields `(key, value)` pairs, i.e. `(value, count)` here. Note the naming
collision: the *dict's* value is our *count*. Unpacking with explicit names keeps it honest.

**(3)** **`(count, value)` — count first.** Tuples compare lexicographically, so the heap
orders by count, exactly what we want. Reversing the order to `(value, count)` would sort by
value and silently produce the wrong answer with no error. The tuple ordering is the one
thing to get right here.

**(4)** The size-k eviction from problem 8. The smallest *count* in the heap is evicted, so
the k highest-frequency entries survive.

**(5)** A list comprehension unpacking each tuple and keeping the value. LeetCode accepts any
order; if you needed them sorted by frequency you'd pop one at a time and reverse.

### Complexity
Let n = elements, m = distinct values (m ≤ n).
- **Time O(n + m log k)** — O(n) counting, then m heap operations at O(log k). With k small
  this is effectively **O(n)**.
- **Space O(m)** for the counter, O(k) for the heap.

Compare: `sorted(counts, key=counts.get)[-k:]` is O(m log m). The heap wins when k ≪ m.

### The O(n) bucket-sort solution
A frequency can never exceed n, so index *by* frequency:

```python
counts = Counter(nums)
buckets = [[] for _ in range(len(nums) + 1)]     # buckets[f] = values seen f times
for value, freq in counts.items():
    buckets[freq].append(value)

res = []
for freq in range(len(buckets) - 1, 0, -1):      # walk down from the highest frequency
    for value in buckets[freq]:
        res.append(value)
        if len(res) == k:
            return res
```
**O(n) time, O(n) space** — strictly better than the heap. Worth knowing, and the bounded-range
insight is the same one from Day 2's counting sort. Interviewers who ask "can you do better
than O(n log k)?" are fishing for this.

### Try next
[K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) ·
[Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/) ·
[Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)

---

## Recall drill

1. Write the exact-match binary search template from memory. Why `<=` and why `mid + 1`?
2. When the loop exits without finding the target, what does `lo` hold, and why is that useful?
3. What are the two conditions that let you binary search the **answer** instead of an array?
4. To track the k **largest** elements, do you use a min-heap or a max-heap? Explain the
   reasoning, not just the answer.
5. `heapify` on a list of n elements: O(n) or O(n log n)? What about pushing n elements one
   at a time?

<details>
<summary>Answers</summary>

1. ```python
   lo, hi = 0, len(nums) - 1
   while lo <= hi:
       mid = (lo + hi) // 2
       if   nums[mid] == target: return mid
       elif nums[mid] <  target: lo = mid + 1
       else:                     hi = mid - 1
   return -1
   ```
   **`<=`** because `hi` is an inclusive bound, so `lo == hi` still names one untested
   candidate. **`mid + 1`** because `mid` has been ruled out, and more importantly because
   `lo = mid` can leave the range unchanged → infinite loop. The ±1 is what guarantees progress.
2. `lo` is the **insertion point** — the first index whose value is ≥ target. That's the
   entire solution to Search Insert Position, and it's what `bisect_left` returns.
3. (a) The answer is an integer in a range you can bound. (b) There's a **monotonic**
   feasibility check: if x works, every larger x works (or the mirror). Monotonicity turns
   the answer space into a sorted `F F F T T T` array.
4. A **min**-heap. The operation you repeat is *eviction*, and you need O(1) access to the
   **worst of your current keepers** to know what to discard. A min-heap puts the smallest of
   the k largest at index 0 — which is also, conveniently, the kth largest overall.
5. `heapify` is **O(n)** — bottom-up construction, where most nodes are near the leaves and
   sift down only a step or two. Pushing n elements individually is **O(n log n)**. Use
   `heapify` whenever you have all the data upfront.

</details>

---

**Tomorrow:** [Day 4 — Stacks, Queues & Monotonic Stack](./day-4-stacks-queues.md). Back to
mostly-familiar territory (seven of your own solutions), plus the **monotonic stack** — the
other pattern that was entirely missing from your 50, and the answer to every "next greater
element" problem.

**Warm-up:** re-solve **Binary Search** and **Kth Largest Element in an Array** from a blank
screen. If Koko still feels like magic, redo it too — it's worth three of anything else.
