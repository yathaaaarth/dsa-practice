# Day 2 — Two Pointers, Sliding Window & Prefix Sums

> **Today's big idea:** yesterday you bought speed with memory. Today you get it almost for
> free by exploiting **structure** — sortedness, contiguity, or the ability to reuse a
> running total. Every technique here replaces a nested loop with two indices that only ever
> move forward.

**Warm-up (10 min, blank screen):** re-solve Two Sum and Single Number from memory.
**Reference:** [Python for DSA §5–7](./01-python-for-dsa.md) · [Complexity Rule 2](./02-complexity.md)

---

## Pattern primer

Three related shapes. Knowing *which* one a problem wants is most of the battle.

### A. Converging pointers — needs a **sorted** array

```python
l, r = 0, len(nums) - 1
while l < r:
    total = nums[l] + nums[r]
    if total == target:  return [l, r]
    elif total < target: l += 1      # need MORE -> raise the low end
    else:                r -= 1      # need LESS -> lower the high end
```

**Why it's correct**, and this is the part to internalise: if `nums[l] + nums[r] < target`,
then `nums[l]` paired with *anything* still available is also too small, because `nums[r]`
is the largest thing left. So `nums[l]` can never be part of the answer, and discarding it
is **sound** — not a heuristic. Sortedness is what licenses the discard.

Each step eliminates one element, so the loop runs at most n times: **O(n), O(1) space**.

### B. Sliding window — a **contiguous** run of variable size

```python
left = 0
window = 0                          # sum, count, or a dict of frequencies
best = float('inf')
for right in range(len(nums)):
    window += nums[right]           # GROW: absorb the new element
    while window >= target:         # SHRINK while the condition holds
        best = min(best, right - left + 1)
        window -= nums[left]        # remove BEFORE moving left
        left += 1
```

**Why it's O(n) despite the nested loop:** `right` advances n times. `left` also advances at
most n times *across the entire run* — it never resets, never goes backwards. Total pointer
movement is 2n, so the work is O(n). (See [Complexity Rule 2](./02-complexity.md); this is
amortised analysis and it's the most commonly misunderstood point in the whole topic.)

**The one design decision:** *when do I shrink?*
- Want the **smallest valid** window → shrink **while valid**, recording as you go.
- Want the **largest valid** window → shrink **while invalid**, recording after.

### C. Prefix sums — many range queries over a fixed array

```python
prefix = []
cur = 0
for n in nums:
    cur += n
    prefix.append(cur)              # prefix[i] = nums[0] + ... + nums[i]

# sum of nums[l..r] in O(1):
prefix[r] - (prefix[l-1] if l > 0 else 0)
```

Pay O(n) once, answer every range query in O(1). Use it when queries are **repeated** and
the array **doesn't change**.

Copy all three out by hand.

---

## 1. Squares of a Sorted Array

**[LeetCode 977 →](https://leetcode.com/problems/squares-of-a-sorted-array/)** · Easy · Converging pointers · [`10-Square-sorted_array.py`](../10-Square-sorted_array.py)

### In one line
Given a **sorted** array that may contain negatives, return the squares in sorted order.

```
[-4,-1,0,3,10] → [0,1,9,16,100]
```

### Recognise it
"Sorted array" + a transformation that breaks the sort. Squaring makes `-4` bigger than
`3`, so the order is destroyed — but only in a *predictable* way, which is the opening.

### Intuition
The obvious answer is `sorted(x*x for x in nums)` — O(n log n). The problem wants O(n).

Here's the key observation: after squaring, the **largest** value must come from one of the
two ends — either the most negative number or the most positive one. Nothing in the middle
can beat both ends. So compare the two ends, take the bigger square, and **fill the answer
array from the back forwards**.

Filling backwards is what makes this work: you always know the largest remaining value, so
you always know what goes in the rightmost empty slot.

### Dry run — `nums = [-4,-1,0,3,10]`

| left | right | `|nums[l]|` vs `|nums[r]|` | winner | index | `ans` |
|---|---|---|---|---|---|
| 0 (-4) | 4 (10) | 4 < 10 | right | 4 | `[_,_,_,_,100]` |
| 0 (-4) | 3 (3) | 4 > 3 | **left** | 3 | `[_,_,_,16,100]` |
| 1 (-1) | 3 (3) | 1 < 3 | right | 2 | `[_,_,9,16,100]` |
| 1 (-1) | 2 (0) | 1 > 0 | **left** | 1 | `[_,1,9,16,100]` |
| 2 (0) | 2 (0) | equal | right | 0 | `[0,1,9,16,100]` |

`left = 3 > right = 1` → stop.

### The code

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        left = 0
        right = n - 1
        ans = [0] * n                        # (1)
        index = n - 1                        # (2)
        while left <= right:                 # (3)
            if abs(nums[left]) > abs(nums[right]):   # (4)
                ans[index] = nums[left] ** 2         # (5)
                left += 1
            else:
                ans[index] = nums[right] ** 2
                right -= 1
            index -= 1                       # (6)
        return ans
```

**(1)** `[0] * n` pre-allocates all n slots. Necessary because we write to arbitrary
positions — you cannot `ans[3] = x` on an empty list. Building with `append` and reversing
at the end also works but costs an extra pass.

**(2)** `index` starts at the **end**. We fill right-to-left because we discover the
*largest* value first.

**(3)** `<=`, not `<`. When `left == right` there is still one unprocessed element (the
middle one). With `<` you'd leave `ans[0]` as 0 — a silent wrong answer on odd-length input.

**(4)** Compare **absolute values**, because we're deciding which *square* is bigger and
`(-4)² > 3²`. Comparing `nums[left] > nums[right]` directly would always be false for a
sorted array — the comparison would be meaningless.

**(5)** `** 2` is exponentiation. `nums[left] * nums[left]` is identical and marginally
faster; both are fine.

**(6)** `index` decrements exactly once per loop iteration, regardless of which branch ran —
one slot is filled either way.

### Complexity
- **Time O(n)** — each iteration moves exactly one of `left`/`right`, and they cover n
  positions between them.
- **Space O(n)** for the output. **O(1) auxiliary** — the pointers and index are constant.
  Say it that way; the output array is required, so it isn't "your" space.

### Try next
[Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) (same fill-from-the-back trick) ·
[Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) ·
[Sort Colors](https://leetcode.com/problems/sort-colors/)

---

## 2. Minimum Absolute Difference

**[LeetCode 1200 →](https://leetcode.com/problems/minimum-absolute-difference/)** · Easy · Sort + linear scan · [`13-Minimum_Absolute_diff.py`](../13-Minimum_Absolute_diff.py)

### In one line
Find every pair with the smallest possible absolute difference, in ascending order.

```
[4,2,1,3] → [[1,2],[2,3],[3,4]]      (min difference is 1)
```

### Recognise it
"Minimum difference between any two elements." Checking all pairs is O(n²) — but after
sorting, **the closest pair must be adjacent**, so only n−1 pairs matter.

### Intuition
Why must the minimum-difference pair be adjacent after sorting? Because if `a < b < c`, then
`c − a > c − b` and `c − a > b − a`. Skipping over an element can only *increase* the gap.
So sorting reduces n²/2 candidate pairs to n−1.

Then two passes: one to find the minimum gap, one to collect every pair achieving it. (One
pass with a "reset the result list when you find a smaller gap" is also possible — the
two-pass version is clearer and the same complexity.)

### Dry run — `arr = [4,2,1,3]`

After `arr.sort()` → `[1,2,3,4]`

Pass 1, adjacent differences: `2−1=1`, `3−2=1`, `4−3=1` → `min_diff = 1`

Pass 2, collect pairs where the difference equals 1: `[1,2]`, `[2,3]`, `[3,4]`

### The code

```python
class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()                                   # (1)
        min_diff = float("inf")                      # (2)
        for i in range(1,len(arr)):                  # (3)
            min_diff = min(min_diff,arr[i]-arr[i-1]) # (4)

        result = []
        for i in range(1,len(arr)):                  # (5)
            if arr[i] - arr[i-1] == min_diff:
                result.append([arr[i-1],arr[i]])     # (6)

        return result
```

**(1)** `arr.sort()` sorts **in place** and returns `None`. `arr = arr.sort()` would set
`arr` to `None` — a very common bug. Here in-place is right: we don't need the original
order, and it saves O(n) space versus `sorted()`.

**(2)** `float("inf")` — any real difference beats it, so the first comparison always wins.
Starting at `0` would be wrong (nothing is smaller) and starting at `arr[1]-arr[0]` requires
a length guard.

**(3)** Start at **1** and look *backwards* to `i-1`. The alternative — start at 0 and look
forward to `i+1` — needs `range(len(arr)-1)` and is easier to get wrong by one.

**(4)** No `abs()` needed: the array is sorted, so `arr[i] >= arr[i-1]` and the difference is
already non-negative. Dropping the `abs` is only safe *because* of the sort.

**(5)** Second pass over the same adjacent pairs. Since the array is sorted ascending, the
pairs come out in ascending order automatically — satisfying the problem's ordering
requirement for free.

**(6)** `[arr[i-1], arr[i]]` — smaller element first, as required.

### Complexity
- **Time O(n log n)** — the sort dominates; the two scans are O(n) each. See
  [Complexity Rule 1](./02-complexity.md): sequential blocks add and the biggest wins.
- **Space O(1) auxiliary** with in-place sort (technically O(log n) for Timsort's stack),
  plus O(n) for the output.

### Try next
[Minimum Absolute Difference in BST](https://leetcode.com/problems/minimum-absolute-difference-in-bst/) (in-order traversal = sorted!) ·
[Maximum Gap](https://leetcode.com/problems/maximum-gap/) ·
[Array Partition](https://leetcode.com/problems/array-partition/)

---

## 3. 3Sum `LC-15`

**[LeetCode 15 →](https://leetcode.com/problems/3sum/)** · Medium · Sort + converging pointers · *new*

### In one line
Find all **unique** triplets summing to zero.

```
[-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]]
```

### Recognise it
Two Sum, one dimension up. The technique: **fix one element, then two-pointer the rest.**
That reduction — turning a k-sum into a (k−1)-sum inside a loop — generalises all the way up.

This is the first genuinely Medium problem in the guide. Take your time on the duplicate
handling; that's where everyone loses.

### Intuition
Brute force is O(n³). Sort first, then for each index `i`, look for two numbers in the
*remainder* summing to `-nums[i]` — which is exactly the converging-pointer scan from the
primer, at O(n). One outer loop × O(n) inner = **O(n²)**.

The hard part is **uniqueness**. Sorting puts equal values next to each other, which makes
duplicates skippable with a simple neighbour check — that's the second reason to sort.

### Dry run — `nums = [-1,0,1,2,-1,-4]` → sorted `[-4,-1,-1,0,1,2]`

| i | `nums[i]` | l | r | sum | action |
|---|---|---|---|---|---|
| 0 | -4 | 1 | 5 | -4+-1+2 = -3 | < 0 → `l++` |
| 0 | -4 | 2 | 5 | -4+-1+2 = -3 | < 0 → `l++` |
| 0 | -4 | 3 | 5 | -4+0+2 = -2 | < 0 → `l++` |
| 0 | -4 | 4 | 5 | -4+1+2 = -1 | < 0 → `l++` → l meets r, done |
| 1 | -1 | 2 | 5 | -1+-1+2 = **0** | **record `[-1,-1,2]`**, move both |
| 1 | -1 | 3 | 4 | -1+0+1 = **0** | **record `[-1,0,1]`**, move both |
| 2 | -1 | — | — | — | **skipped**: `nums[2] == nums[1]` |
| 3 | 0 | 4 | 5 | 0+1+2 = 3 | > 0 → `r--` → done |

Result: `[[-1,-1,2],[-1,0,1]]`

### The code

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()                                  # (1)
        res = []

        for i in range(len(nums) - 2):               # (2)
            if nums[i] > 0:                          # (3)
                break
            if i > 0 and nums[i] == nums[i - 1]:     # (4)
                continue

            l, r = i + 1, len(nums) - 1              # (5)
            while l < r:
                total = nums[i] + nums[l] + nums[r]
                if total < 0:
                    l += 1                           # (6)
                elif total > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1                           # (7)
                    while l < r and nums[l] == nums[l - 1]:   # (8)
                        l += 1
        return res
```

**(1)** Sorting does **two** jobs: it enables the converging-pointer scan, and it groups
duplicates so they can be skipped by comparing neighbours. Without it, deduplication would
need a set of tuples.

**(2)** `len(nums) - 2` because we need at least two more elements to the right of `i`.

**(3)** Early exit. The array is sorted, so once `nums[i] > 0` the two larger numbers to its
right are positive too — the sum can never be zero. Not required for correctness, but a real
speedup and it shows you're thinking.

**(4)** **Skip duplicate first elements.** `i > 0` guards the very first iteration
(`nums[-1]` would wrap to the end of the list — a silent bug). If `nums[i] == nums[i-1]`,
every triplet starting here was already found starting at `i-1`.

**(5)** The window starts at `i + 1` — strictly to the right of `i`, so no element is reused
and each triplet is generated in exactly one order.

**(6)** The sound-discard logic from the primer: sum too small → the only way to grow it is
to raise the small end.

**(7)** On a hit, move **both** pointers. Moving only one guarantees the next sum is wrong
(you'd change the total in one direction with the other end fixed), so it wastes an iteration.

**(8)** **Skip duplicate second elements.** After recording, if `nums[l] == nums[l-1]` we'd
produce the identical triplet again. The `l < r` guard keeps `l` from running past `r`.
(A matching skip on `r` is optional — once `l` is unique, the third element is determined.)

### Complexity
- **Time O(n²)** — O(n log n) sort + n outer iterations × O(n) inner scan. The inner `while`
  is O(n) not O(n²) because `l` and `r` only ever move toward each other.
- **Space O(1) auxiliary** (in-place sort), excluding the output.

### Pitfalls
- **Forgetting `i > 0` in (4)** — `nums[-1]` is Python's last element, so the very first
  iteration silently compares against the wrong thing.
- Using a `set` of tuples to dedupe instead of the neighbour checks: correct, but O(n) extra
  space and it hides the fact that you understood why sorting helps.
- Moving only one pointer at (7).

### Try next
[3Sum Closest](https://leetcode.com/problems/3sum-closest/) ·
[4Sum](https://leetcode.com/problems/4sum/) (same reduction, one more loop) ·
[Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

---

## 4. Best Time to Buy and Sell Stock

**[LeetCode 121 →](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)** · Easy · Two pointers / running minimum · [`09-Best_time_sell_stock.py`](../09-Best_time_sell_stock.py)

### In one line
One buy, one later sell. Maximum profit, or 0 if there's no profitable trade.

```
[7,1,5,3,6,4] → 5      (buy at 1, sell at 6)
[7,6,4,3,1]   → 0      (prices only fall)
```

### Recognise it
"Maximum difference where the smaller element comes **first**." The ordering constraint is
what stops you from just doing `max(prices) - min(prices)`.

### Intuition
You only need one thing as you scan: **the cheapest price seen so far**. At every day, the
best possible sale today is `today − cheapest_so_far`. Track the running best of that.

Your file frames it as two pointers, `l` (buy day) and `r` (sell day), where `l` jumps
forward whenever a new low appears — which is the same algorithm wearing different clothes.

### Dry run — `prices = [7,1,5,3,6,4]`

| r | `prices[l]` | `prices[r]` | `l < r`? | profit | `max_profit` | action |
|---|---|---|---|---|---|---|
| 1 | 7 | 1 | no (7 > 1) | — | 0 | **`l = 1`** (new low) |
| 2 | 1 | 5 | yes | 4 | **4** | |
| 3 | 1 | 3 | yes | 2 | 4 | |
| 4 | 1 | 6 | yes | 5 | **5** | |
| 5 | 1 | 4 | yes | 3 | 5 | |

→ **5**

### The code

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l,r = 0,1                              # (1)
        max_profit = 0                         # (2)
        while r != len(prices):                # (3)
            if(prices[l] < prices[r]):         # (4)
                profit = prices[r] - prices[l]
                max_profit = max(max_profit,profit)
            else:
                l = r                          # (5)
            r += 1                             # (6)
        return max_profit
```

**(1)** `l` is the buy day, `r` the sell day, starting adjacent. `r` starts at 1 because you
cannot buy and sell on the same day.

**(2)** Initialised to **0**, not `-inf`, because "do nothing" is always allowed — the
problem says return 0 if no profit is possible. This is a case where the sentinel should
*not* be infinity; the identity here is the do-nothing profit.

**(3)** `while r != len(prices)` — `<` would read better and be safer (identical here since
`r` increases by exactly 1).

**(4)** Only a *lower* buy price than the current sell price can produce profit.

**(5)** **The key line.** If `prices[r] <= prices[l]`, then day `r` is a new cheapest day.
Every future sale should reference `r`, not `l` — a lower buy price beats the old one for
*every* future sell day. So `l` jumps straight to `r`. It never moves backwards, which is
why this stays O(n).

**(6)** `r` advances unconditionally, one day at a time.

### The running-minimum form — same algorithm, clearer

```python
min_price = float('inf')
max_profit = 0
for price in prices:
    min_price = min(min_price, price)             # cheapest so far
    max_profit = max(max_profit, price - min_price)
return max_profit
```
Four lines, no pointer bookkeeping. Worth writing both and noticing they're identical.

### Complexity
- **Time O(n)** — one pass; `l` only jumps forward.
- **Space O(1)** — a handful of integers regardless of input size.

### Try next
[Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) (greedy) ·
[Maximum Subarray (later today)](https://leetcode.com/problems/maximum-subarray/) — note how similar the shape is ·
[Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

---

## 5. Minimum Size Subarray Sum

**[LeetCode 209 →](https://leetcode.com/problems/minimum-size-subarray-sum/)** · Medium · **Variable sliding window** · [`14-Minimum_size_subarray_sum.py`](../14-Minimum_size_subarray_sum.py)

### In one line
Shortest **contiguous** subarray whose sum is ≥ `target`. Return 0 if none exists.

```
target = 7, nums = [2,3,1,2,4,3] → 2      ([4,3])
```

### Recognise it
"**Contiguous** subarray" + "minimum length" + "sum at least X". This is the canonical
variable-size sliding window. Learn this one cold — it is the template for a large family
of Medium problems.

### Intuition
Grow the window on the right, adding elements until the sum reaches `target`. The moment
it does, the window is *valid* — so record its length and then **shrink from the left** as
far as you can while it stays valid, since a shorter valid window is a better answer. Then
resume growing.

Both pointers only move right. Nothing is ever recomputed. That's the whole trick.

### Dry run — `target = 7`, `nums = [2,3,1,2,4,3]`

| right | added | total | ≥ 7? | window | `min_len` | shrink |
|---|---|---|---|---|---|---|
| 0 | 2 | 2 | no | `[2]` | ∞ | |
| 1 | 3 | 5 | no | `[2,3]` | ∞ | |
| 2 | 1 | 6 | no | `[2,3,1]` | ∞ | |
| 3 | 2 | 8 | **yes** | `[2,3,1,2]` len 4 | **4** | drop 2 → total 6, left=1 |
| 4 | 4 | 10 | **yes** | `[3,1,2,4]` len 4 | 4 | drop 3 → 7, left=2 |
| 4 | | 7 | **yes** | `[1,2,4]` len 3 | **3** | drop 1 → 6, left=3 |
| 5 | 3 | 9 | **yes** | `[2,4,3]` len 3 | 3 | drop 2 → 7, left=4 |
| 5 | | 7 | **yes** | `[4,3]` len **2** | **2** | drop 4 → 3, left=5 |

→ **2**

### The code

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left,right,total = 0,0,0
        min_len = len(nums) + 1              # (1)

        while right < len(nums):
            total += nums[right]             # (2)
            right += 1                       # (3)
            while total >= target:           # (4)
                min_len = min(min_len,right-left)   # (5)
                total -= nums[left]          # (6)
                left += 1

        if min_len == len(nums) + 1:         # (7)
            return 0
        else:
            return min_len
```

**(1)** Sentinel: `len(nums) + 1` is an impossible length, so "still equal to it at the end"
means "never found one". `float('inf')` would work identically — see
[Python §7](./01-python-for-dsa.md).

**(2)–(3)** Add the new element, *then* advance `right` past it. Because `right` is
incremented immediately, it becomes an **exclusive** bound — the window is `nums[left:right]`.
That's what makes (5) work without a `+1`.

**(4)** `while`, not `if`. After removing one element the window may *still* be valid, and
you want to keep shrinking to find the shortest. An `if` here is a classic bug — it would
find a valid window but not the minimal one.

**(5)** `right - left` is the length, with no `+1`, precisely because `right` is exclusive
(see (3)). If you increment `right` at the *bottom* of the loop instead, you need
`right - left + 1`. Pick one convention and stick to it; mixing them is where off-by-ones
come from.

**(6)** Subtract *before* moving `left`. `nums[left]` is still in the window at this point.
Reversing these two lines removes the wrong element.

**(7)** Unchanged sentinel → no valid subarray exists.

### Complexity
- **Time O(n)** — and this is the point of the day. It *looks* like O(n²) because of the
  nested `while`, but `left` and `right` each advance at most n times **in total** across
  the whole run. Total pointer movement ≤ 2n. See [Complexity Rule 2](./02-complexity.md).
- **Space O(1)**.

### Why this needs non-negative numbers
The problem guarantees positive integers. That guarantee is load-bearing: it means adding an
element can only *increase* the sum and removing one can only *decrease* it — so the window
is monotonic and shrinking is safe. With negatives, the sliding window breaks entirely and
you need prefix sums plus a hash map (see Subarray Sum Equals K).

### Try next
[Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) ·
[Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) ·
[Permutation in String](https://leetcode.com/problems/permutation-in-string/) ·
[Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) (where the window fails)

---

## 6. Longest Mountain in Array

**[LeetCode 845 →](https://leetcode.com/problems/longest-mountain-in-array/)** · Medium · Expand from centre · [`11-Longest_mountain_Array.py`](../11-Longest_mountain_Array.py)

### In one line
Longest subarray that strictly rises then strictly falls (both sides non-empty).

```
[2,1,4,7,3,2,5] → 5      ([1,4,7,3,2])
[2,2,2]         → 0      (no strict rise)
```

### Recognise it
"Rises then falls", "peak", "valley", "mountain". The pattern is **find the special point,
then expand outwards in both directions** — the same shape as expand-around-centre for
palindromes.

### Intuition
Every mountain has exactly one peak, and a peak is trivially detectable locally:
`arr[i-1] < arr[i] > arr[i+1]`. So scan for peaks, and at each one walk left while the
values keep decreasing and right while they keep decreasing. The span is the mountain.

### Dry run — `arr = [2,1,4,7,3,2,5]`

| i | `arr[i-1] < arr[i] > arr[i+1]`? | walk left | walk right | length | `result` |
|---|---|---|---|---|---|
| 1 (val 1) | 2 < 1? no | | | | 0 |
| 2 (val 4) | 1 < 4 > 7? no | | | | 0 |
| 3 (val 7) | **4 < 7 > 3 yes** | l: 3→2→1 (stops, `arr[1]=1 < arr[0]=2`… wait: `arr[1] > arr[0]`? 1 > 2 false → stop at l=1) | r: 3→4→5 (`arr[5]=2 > arr[6]=5`? no → stop at r=5) | 5−1+1 = **5** | **5** |
| 4 (val 3) | 7 < 3? no | | | | 5 |
| 5 (val 2) | 3 < 2? no | | | | 5 |

→ **5** (the subarray `[1,4,7,3,2]`, indices 1..5)

### The code

```python
class Solution:
    def longestMountain(self, arr: List[int]) -> int:
        result = 0
        n = len(arr)

        for i in range(1, n - 1):                    # (1)
            if arr[i - 1] < arr[i] > arr[i + 1]:     # (2)
                l = r = i                            # (3)

                while l > 0 and arr[l] > arr[l - 1]: # (4)
                    l -= 1

                while r < n - 1 and arr[r] > arr[r + 1]:  # (5)
                    r += 1

                result = max(result, r - l + 1)      # (6)

        return result
```

**(1)** `range(1, n-1)` — a peak needs a neighbour on both sides, so indices 0 and n−1 can
never be peaks. This range also makes `arr[i-1]` and `arr[i+1]` always in bounds, so no
guard is needed inside.

**(2)** **Python chained comparison.** `a < b > c` means `(a < b) and (b > c)` — and `b` is
evaluated only once. Most languages don't allow this; in Python it reads exactly like the
mathematical statement. Note the comparisons are **strict** (`<`, `>`), which is what
enforces "strictly increasing then strictly decreasing" — a plateau like `[1,2,2,1]` is
correctly rejected.

**(3)** `l = r = i` binds both names to the same integer, then they diverge. (For an
immutable `int` this is completely safe — see [Python §12](./01-python-for-dsa.md).)

**(4)** Walk left while values keep *decreasing* as you go left (i.e. `arr[l] > arr[l-1]`).
`l > 0` prevents running off the front.

**(5)** Symmetrically to the right. `r < n-1` prevents running off the back.

**(6)** `r - l + 1` — inclusive length, `+1` because both endpoints are part of the mountain.
(Contrast with problem 5, where `right` was exclusive and there was no `+1`. Always know
which convention you're in.)

### Complexity
- **Time O(n)** — it *looks* quadratic, but mountains don't overlap: the descending slope of
  one mountain can't be the ascending slope of another. Across the whole array the walks
  visit each element O(1) times amortised.
- **Space O(1)**.

### The one-pass state-machine alternative
```python
res = up = down = 0
for i in range(1, len(arr)):
    if (down and arr[i-1] < arr[i]) or arr[i-1] == arr[i]:
        up = down = 0                      # mountain ended, or a plateau -> reset
    up   += arr[i-1] < arr[i]
    down += arr[i-1] > arr[i]
    if up and down:
        res = max(res, up + down + 1)
return res
```
Strictly O(n), single pass. Harder to get right under pressure; the peak-expansion version
is the one to reach for.

### Try next
[Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) (expand around centre) ·
[Peak Index in a Mountain Array](https://leetcode.com/problems/peak-index-in-a-mountain-array/) ·
[Valid Mountain Array](https://leetcode.com/problems/valid-mountain-array/)

---

## 7. Minimum Time Visiting All Points

**[LeetCode 1266 →](https://leetcode.com/problems/minimum-time-visiting-all-points/)** · Easy · Greedy / Chebyshev distance · [`06-Minimum_time_visit.py`](../06-Minimum_time_visit.py)

### In one line
Visit points **in the given order**. Each second you move 1 unit horizontally, vertically, or
diagonally. Minimum total seconds.

```
[[1,1],[3,4],[-1,0]] → 7
```

### Recognise it
Geometry with **diagonal moves allowed**. The whole problem collapses to one formula; the
skill is deriving it, not coding it.

### Intuition
To go from `(x1,y1)` to `(x2,y2)`, let `dx = |x2−x1|` and `dy = |y2−y1|`.

A diagonal step covers **one unit of x and one unit of y simultaneously** — it's two units
of progress for one second. So use diagonals to knock out the smaller of the two gaps, then
straight steps for the remainder:

- `min(dx, dy)` diagonal steps, then
- `|dx − dy|` straight steps

Total = `min(dx,dy) + |dx−dy|` = **`max(dx, dy)`**.

That's the Chebyshev distance. The order is fixed, so there's no routing decision — just sum
the leg costs.

### Dry run — `[[1,1],[3,4],[-1,0]]`

| leg | dx | dy | `max` |
|---|---|---|---|
| (1,1) → (3,4) | 2 | 3 | 3 |
| (3,4) → (-1,0) | 4 | 4 | 4 |

3 + 4 = **7**

### The code

```python
class Solution:
    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        result = 0
        x1,y1 = points.pop()                          # (1)
        while points:                                 # (2)
            x2,y2 = points.pop()
            result += max(abs(y2-y1),abs(x2-x1))      # (3)
            x1,y1 = x2,y2                             # (4)
        return result
```

**(1)** **Tuple unpacking**: `x1, y1 = [3, 4]` assigns both at once. `points.pop()` with no
argument removes from the **end** — O(1). (`pop(0)` would be O(n) — see
[Python §3](./01-python-for-dsa.md).) The code walks the list backwards, which is fine:
distance is symmetric, so traversing the route in reverse costs the same.

**(2)** `while points:` — a non-empty list is truthy, empty is falsy. Idiomatic Python for
"while there's anything left".

**(3)** The formula. `max` of the two absolute differences.

**(4)** Slide the "previous point" forward. The right-hand side is fully evaluated before
assignment, so no temporary is needed.

### Complexity
- **Time O(n)** — one `max` and two `abs` per point, all O(1).
- **Space O(1)** auxiliary — though note this **destroys the input list** via `pop()`. If
  that matters, iterate with `zip(points, points[1:])` instead.

### Try next
[Queries on Number of Points Inside a Circle](https://leetcode.com/problems/queries-on-number-of-points-inside-a-circle/) ·
[Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) ·
[K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)

---

## 8. Maximum Subarray (Kadane's Algorithm)

**[LeetCode 53 →](https://leetcode.com/problems/maximum-subarray/)** · Medium · Kadane · [`18-maximum_subarray.py`](../18-maximum_subarray.py)

### In one line
Largest sum of any **contiguous** non-empty subarray.

```
[-2,1,-3,4,-1,2,1,-5,4] → 6      ([4,-1,2,1])
[-3,-1,-2]              → -1     (must pick something)
```

### Recognise it
"Maximum sum contiguous subarray" — this exact phrasing means Kadane. It's one of the
handful of named algorithms worth memorising outright.

### Intuition
Walk left to right carrying a running sum. The one insight:

> **If the running sum ever drops below zero, throw it away and start fresh.**

Why? A negative prefix can only *hurt* whatever comes next. If the sum so far is −5, then
starting over at 0 is strictly better than dragging −5 along. So reset.

Meanwhile, track the best sum ever seen. That's the whole algorithm.

### Dry run — `nums = [-2,1,-3,4,-1,2,1,-5,4]`

| i | `nums[i]` | `total_sum` after add | `max_sum` | reset? |
|---|---|---|---|---|
| 0 | -2 | -2 | -2 | **yes** → 0 |
| 1 | 1 | 1 | 1 | no |
| 2 | -3 | -2 | 1 | **yes** → 0 |
| 3 | 4 | 4 | 4 | no |
| 4 | -1 | 3 | 4 | no |
| 5 | 2 | 5 | 5 | no |
| 6 | 1 | **6** | **6** | no |
| 7 | -5 | 1 | 6 | no |
| 8 | 4 | 5 | 6 | no |

→ **6**

### The code

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        total_sum = 0
        max_sum = nums[0]                      # (1)
        for i in range(len(nums)):
            total_sum += nums[i]               # (2)
            max_sum = max(total_sum,max_sum)   # (3)
            if total_sum < 0:                  # (4)
                total_sum = 0

        return max_sum
```

**(1)** **`nums[0]`, not `0`.** This is the critical initialisation. If every element is
negative, no subarray has a positive sum, and the answer is the single largest (least
negative) element. Starting `max_sum` at `0` would return 0 for `[-3,-1,-2]` — but the
problem requires a *non-empty* subarray, so the answer is −1. Try it: this is the single
most common wrong answer on this problem.

**(2)** Extend the current run.

**(3)** Record before any reset, so a subarray ending exactly here is always considered.

**(4)** The reset. Note it happens **after** recording — if you reset first you'd never
record a negative maximum, breaking the all-negative case from (1).

### Complexity
- **Time O(n)** — one pass. (The divide-and-conquer solution is O(n log n); Kadane is
  strictly better and worth naming if asked.)
- **Space O(1)** — two integers.

### To also return the indices
```python
best = cur = nums[0]
start = end = tmp = 0
for i in range(1, len(nums)):
    if cur < 0:
        cur, tmp = nums[i], i      # restart here
    else:
        cur += nums[i]
    if cur > best:
        best, start, end = cur, tmp, i
return best, start, end
```
Interviewers ask for this follow-up often.

### Try next
[Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) (the negative-flips-sign twist) ·
[Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) — the same shape ·
[Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/)

---

## 9. Range Sum Query — Immutable

**[LeetCode 303 →](https://leetcode.com/problems/range-sum-query-immutable/)** · Easy · Prefix sums · [`20-Range_sum_query.py`](../20-Range_sum_query.py)

### In one line
Answer many `sum(nums[left..right])` queries on an array that never changes.

```
NumArray([-2,0,3,-5,2,-1])
sumRange(0,2) → 1        sumRange(2,5) → -1
```

### Recognise it
"**Multiple** queries" + "the array is immutable". The word *immutable* in the title is the
hint: precomputation is safe because nothing will invalidate it.

### Intuition
Answering each query by summing the range is O(n) per query — fine once, terrible for
100,000 queries.

Instead, precompute `prefix[i] = nums[0] + nums[1] + … + nums[i]` in one O(n) pass. Then

```
sum(left..right) = prefix[right] − prefix[left−1]
```

because `prefix[right]` includes everything up to `right`, and subtracting everything before
`left` leaves exactly the range you want. **O(1) per query** after an O(n) setup.

This is a design pattern, not just a trick: pay once, query cheaply, forever.

### Dry run — `nums = [-2,0,3,-5,2,-1]`

`prefix = [-2, -2, 1, -4, -2, -3]`

| query | computation | result |
|---|---|---|
| `sumRange(0,2)` | `prefix[2] − 0` (left = 0, nothing to exclude) | `1` |
| `sumRange(2,5)` | `prefix[5] − prefix[1]` = `−3 − (−2)` | `−1` |
| `sumRange(3,3)` | `prefix[3] − prefix[2]` = `−4 − 1` | `−5` |

### The code

```python
class NumArray:
    def __init__(self, nums: List[int]):
        self.prefix = []                  # (1)
        cur = 0
        for n in nums:
            cur += n                      # (2)
            self.prefix.append(cur)

    def sumRange(self, left: int, right: int) -> int:
        rightSum = self.prefix[right]
        leftSum = self.prefix[left - 1] if left > 0 else 0   # (3)
        return rightSum - leftSum         # (4)
```

**(1)** `self.` makes it an **instance attribute** — it survives between method calls, which
is the entire point of a class-based problem. A local `prefix = []` would vanish when
`__init__` returned.

**(2)** One running total, appended each step. O(n) once.

**(3)** **The guard that makes or breaks this.** When `left == 0` there is nothing to
exclude, so subtract 0. Without the guard, `self.prefix[-1]` is Python's *last* element —
so `sumRange(0, 2)` would silently subtract the sum of the entire array and return a plausible
wrong number. Negative indexing making a bug silent instead of loud is exactly why this
guard matters.

The conditional-expression form `a if cond else b` keeps it to one line.

**(4)** The subtraction. O(1).

### Complexity
- **`__init__`: O(n) time, O(n) space.**
- **`sumRange`: O(1) time, O(1) space.**

State it as a trade: O(n) preprocessing to make each of q queries O(1), so q queries cost
O(n + q) instead of O(n·q).

### The sentinel-zero variant (cleaner)
```python
self.prefix = [0]                        # a leading zero
for n in nums:
    self.prefix.append(self.prefix[-1] + n)

def sumRange(self, left, right):
    return self.prefix[right + 1] - self.prefix[left]   # no special case
```
The extra leading 0 makes the `left == 0` case fall out naturally. Worth adopting — fewer
branches, fewer bugs.

### Try next
[Range Sum Query 2D — Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) ·
[Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) (prefix sums + hash map) ·
[Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) (prefix *and* suffix)

---

## 10. Spiral Matrix

**[LeetCode 54 →](https://leetcode.com/problems/spiral-matrix/)** · Medium · Layer peeling / boundaries · [`07-Spiral_matrix.py`](../07-Spiral_matrix.py)

### In one line
Return all elements in spiral order.

```
[[1,2,3],
 [4,5,6],   →  [1,2,3,6,9,8,7,4,5]
 [7,8,9]]
```

### Recognise it
Pure simulation. There's no clever insight — the entire difficulty is **bookkeeping without
revisiting or skipping a cell**, especially on non-square matrices.

### Intuition
Peel the matrix like an onion. Repeat until nothing is left:

1. Take the whole **top row**, remove it.
2. Take the **last element of each remaining row** (the right column), remove them.
3. Take the **bottom row reversed**, remove it.
4. Take the **first element of each remaining row, bottom to top** (the left column).

Each step shrinks the matrix, so the loop terminates.

### Dry run — `[[1,2,3],[4,5,6],[7,8,9]]`

| step | action | taken | matrix after |
|---|---|---|---|
| top | `pop(0)` | `1,2,3` | `[[4,5,6],[7,8,9]]` |
| right | `row.pop()` each | `6,9` | `[[4,5],[7,8]]` |
| bottom | `pop()[::-1]` | `8,7` | `[[4,5]]` |
| left | `row.pop(0)` bottom-up | `4` | `[[5]]` |
| top | `pop(0)` | `5` | `[]` |

→ `[1,2,3,6,9,8,7,4,5]`

### The code

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        ret = []
        while matrix:                        # (1)
            ret += matrix.pop(0)             # (2)

            if matrix and matrix[0]:         # (3)
                for row in matrix:
                    ret.append(row.pop())    # (4)

            if matrix:
                ret += matrix.pop()[::-1]    # (5)

            if matrix and matrix[0]:
                for row in matrix[::-1]:     # (6)
                    ret.append(row.pop(0))

        return ret
```

**(1)** `while matrix:` — loop until every row has been consumed. An emptied list is falsy.

**(2)** `matrix.pop(0)` removes and returns the whole first row. `ret += list` extends in
place (equivalent to `ret.extend(...)`), unlike `ret.append(list)` which would nest a list
inside a list.

**(3)** **These guards are the whole problem.** After popping the top row the matrix may be
empty (`matrix`), or the rows may have been emptied by earlier `pop()` calls (`matrix[0]`).
Skipping either check causes `IndexError` on non-square inputs. Try `[[1],[2],[3]]` on paper
without the guards.

**(4)** `row.pop()` with no argument removes the **last** element — the rightmost column, one
row at a time, top to bottom. O(1) each.

**(5)** `matrix.pop()` takes the last row; `[::-1]` reverses it, because the spiral traverses
the bottom row **right to left**. The slice allocates a new list — O(k) — which is fine here.

**(6)** `matrix[::-1]` iterates the rows **bottom to top**, since the left column is
traversed upward. `row.pop(0)` takes the leftmost element.

### Complexity
- **Time O(m·n)** to produce m·n elements — but with a real constant-factor cost: each
  `pop(0)` shifts every remaining element, so the true bound is closer to **O(m·n + m²)**.
  For LeetCode's constraints it passes comfortably.
- **Space O(1)** auxiliary, excluding the output — but it **destroys the input matrix**.

### The four-boundary version — no mutation, cleaner O(m·n)

Interviewers frequently ask you not to modify the input. This is the version to know:

```python
def spiralOrder(self, matrix):
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):        # top row, left -> right
            res.append(matrix[top][c])
        top += 1

        for r in range(top, bottom + 1):        # right column, top -> bottom
            res.append(matrix[r][right])
        right -= 1

        if top <= bottom:                       # guard: is there still a bottom row?
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1

        if left <= right:                       # guard: is there still a left column?
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1

    return res
```

The two mid-loop guards do the same job as the `if matrix and matrix[0]` checks above: on a
single-row or single-column remainder, the bottom row *is* the top row and re-traversing it
would duplicate elements. **O(m·n) time, O(1) auxiliary space, input untouched.**

### Try next
[Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) (generate one) ·
[Rotate Image](https://leetcode.com/problems/rotate-image/) ·
[Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

---

## Recall drill

1. Two nested `while` loops, and the answer is O(n) not O(n²). Explain why, precisely.
2. In Squares of a Sorted Array, why fill the output array from the **back**?
3. In Minimum Size Subarray Sum, why is the inner loop `while total >= target` and not `if`?
4. In Maximum Subarray, why is `max_sum` initialised to `nums[0]` instead of `0`?
5. Why does the sliding window require non-negative numbers, and what do you use instead
   when negatives are allowed?

<details>
<summary>Answers</summary>

1. Because `left` and `right` each advance **at most n times in total across the entire
   run** — neither ever resets or moves backwards. Total pointer movement is bounded by 2n,
   so total work is O(n). The right question is never "how many inner iterations per outer
   iteration" but "how far does the inner variable travel overall".
2. Because the algorithm discovers the **largest** square first (it must come from one of
   the two ends). The largest value belongs in the last slot, so you fill right-to-left.
   Filling forwards would require knowing the smallest first, which the two ends don't tell you.
3. Because after removing one element the window may **still** be valid, and a shorter valid
   window is a better answer. `if` would shrink once and move on, finding *a* valid window
   but not the minimal one.
4. Because the subarray must be non-empty. If every element is negative, the best answer is
   the least-negative single element — a negative number. Initialising to 0 would wrongly
   return 0 for `[-3,-1,-2]`.
5. Because the window relies on monotonicity: adding an element only increases the sum,
   removing one only decreases it, so shrinking is a safe way to search. With negatives,
   adding an element can *decrease* the sum and that reasoning collapses. The replacement is
   **prefix sums + a hash map** — see Subarray Sum Equals K.

</details>

---

**Tomorrow:** [Day 3 — Binary Search & Heaps](./day-3-binary-search-heaps.md). All ten
problems are new, because the original 50 contained **no binary search and no heap at all** —
the largest gap in the set. Day 3 also has the single highest-leverage idea of the week:
binary search on the *answer*.

**Warm-up:** re-solve **Best Time to Buy and Sell Stock** and **Minimum Size Subarray Sum**
from a blank screen.
