# Day 1 — Hashing, Sets & Bit Tricks

> **Today's big idea:** almost every "did I already see this?" problem has a brute-force
> O(n²) answer and an O(n) answer, and the only difference between them is a hash set.
> You are trading memory for time. Today is about making that trade automatic.

**Prerequisites:** [How to use this guide](./00-how-to-use.md) · [Python for DSA §1–2](./01-python-for-dsa.md)
**Also read before you start:** [bugs-found.md](./bugs-found.md) — six solutions in this repo were broken.

---

## Pattern primer

### Why a hash set is O(1)

A `list` stores elements in a row. `x in my_list` walks the row until it finds `x` — O(n).

A `set` stores elements in buckets chosen by `hash(x)`. `x in my_set` computes `hash(x)`,
jumps straight to that bucket, and looks at the handful of things there — O(1) on average.

That is the whole mechanism. The consequence:

```python
seen = []      # `x in seen` is O(n)  → the enclosing loop is O(n²)
seen = set()   # `x in seen` is O(1)  → the enclosing loop is O(n)
```

**The price:** memory. A set of n integers costs roughly 32–60 bytes each. You are buying
time with space, and saying that out loud is half of a good complexity answer.

**The requirement:** elements must be hashable, i.e. immutable. `int`, `str`, `tuple` yes;
`list`, `dict`, `set` no. That is why grid coordinates go in as `(r, c)` tuples.

### Template A — "have I seen this?"

```python
seen = set()
for x in nums:
    if x in seen:
        return True
    seen.add(x)
return False
```

### Template B — "have I seen the thing that *completes* this?"

```python
seen = {}                          # value -> index
for i, x in enumerate(nums):
    if target - x in seen:         # look for the COMPLEMENT
        return [seen[target - x], i]
    seen[x] = i
```

The mental shift in Template B is the important one. The brute force asks, for every pair,
"do these two add up?" — n²/2 questions. Template B asks, for each element, one question:
"have I already walked past my exact partner?" One pass instead of n passes.

### Template C — frequency counting

```python
from collections import Counter
counts = Counter(s)                    # {'a': 2, 'b': 1}
counts = Counter(s) == Counter(t)      # anagram check, one line
```

### Template D — XOR, when you need O(1) *space*

```python
result = 0
for x in nums:
    result ^= x
```

Two facts do all the work: `x ^ x == 0` (a value cancels itself) and `x ^ 0 == x` (zero is
the identity). XOR is also commutative, so order doesn't matter. Everything paired
annihilates; the unpaired survivor is left.

Copy these four templates out by hand before you start. Yes, by hand.

---

## 1. Contains Duplicate

**[LeetCode 217 →](https://leetcode.com/problems/contains-duplicate/)** · Easy · Hash set · [`01-Duplicate_value.py`](../01-Duplicate_value.py)

### In one line
Return `True` if any value appears at least twice.

```
[1,2,3,1] → True        [1,2,3,4] → False
```

### Recognise it
"Contains duplicate", "any value appears twice", "are all elements distinct". The instant
you read *have we seen this before*, the answer is a hash set.

### Intuition
Brute force compares every pair: n²/2 comparisons. But you don't need to compare pairs —
you only need to remember what you've walked past. Keep a set of everything seen so far;
the moment the current element is already in it, you're done.

### Dry run — `nums = [1, 2, 3, 1]`

| Step | `num` | `num in seen`? | `seen` after | Action |
|---|---|---|---|---|
| 1 | 1 | no | `{1}` | add |
| 2 | 2 | no | `{1,2}` | add |
| 3 | 3 | no | `{1,2,3}` | add |
| 4 | 1 | **yes** | — | **return True** |

### The code

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()              # (1)
        for num in nums:          # (2)
            if num in seen:       # (3)
                return True       # (4)
            seen.add(num)         # (5)
        return False              # (6)
```

**(1)** `set()` and not `[]`. This single character choice *is* the algorithm — with a list
this code is O(n²) and looks identical. `set()` and not `{}`: bare braces make an empty
**dict**, not a set.

**(2)** Iterating the values directly. No `range(len(nums))` needed since we never use the
index.

**(3)** O(1) average membership test — the hash lookup. This is the line the whole
complexity argument hangs on.

**(4)** Return immediately. No need to see the rest of the array; the answer can't change.

**(5)** Add *after* the check. Adding first would make every element find itself and return
`True` on step 1.

**(6)** Loop finished without a hit → all distinct.

### Complexity
- **Time O(n)** — one pass, n iterations, each doing O(1) work (hash, compare, insert).
- **Space O(n)** — worst case (all distinct) the set holds every element. Best case O(1),
  when the duplicate is at position 2.

*The trade-off to state aloud:* the alternative is `nums.sort()` then check neighbours —
O(1) extra space but O(n log n) time. Hashing buys speed with memory.

### Pitfalls
- `seen = {}` creates a dict. Harmless here (`in` still works on keys) but confusing.
- One-liner `return len(set(nums)) != len(nums)` is correct and fine, but it always builds
  the whole set — no early exit. The loop version bails on the first duplicate.

### Try next
[Contains Duplicate II (#12, later today)](https://leetcode.com/problems/contains-duplicate-ii/) ·
[Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) ·
[Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/)

---

## 2. Two Sum

**[LeetCode 1 →](https://leetcode.com/problems/two-sum/)** · Easy · Hash map (complement) · [`04-Two_sum.py`](../04-Two_sum.py)

### In one line
Return the **indices** of the two numbers adding to `target`. Exactly one answer exists.

```
nums = [2,7,11,15], target = 9  →  [0,1]     because 2 + 7 = 9
```

### Recognise it
"Two numbers that sum to X", "find the pair". Note we need **indices**, not values — that
is why a set won't do and we need a dict.

### Intuition
The brute force checks all pairs, O(n²). Flip the question. At element `x`, the partner you
need is fixed and known: `target - x`. So the only question is *"have I already seen
`target - x`?"* — one O(1) lookup instead of a scan. One pass, and each element gets
checked against everything before it, which covers every pair exactly once.

### Dry run — `nums = [2, 7, 11, 15]`, `target = 9`

| i | `nums[i]` | `complement = 9 - nums[i]` | in `numMap`? | `numMap` after |
|---|---|---|---|---|
| 0 | 2 | 7 | no | `{2: 0}` |
| 1 | 7 | 2 | **yes → `numMap[2] = 0`** | **return `[0, 1]`** |

### The code

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numMap = {}                              # (1)
        n = len(nums)

        for i in range(n):                       # (2)
            complement = target - nums[i]        # (3)
            if complement in numMap:             # (4)
                return [numMap[complement], i]   # (5)
            numMap[nums[i]] = i                  # (6)
        return []                                # (7)
```

**(1)** A **dict**, not a set — we must return positions, so we map `value → index`. This is
the one distinction between problem 1 and problem 2 today.

**(2)** `range(n)` because we need `i` for the answer. `for i, num in enumerate(nums)` is
more idiomatic and equivalent.

**(3)** The complement is pure arithmetic — O(1). Naming it in a variable makes the next
line read as the question you're actually asking.

**(4)** `in` on a dict checks **keys**, in O(1).

**(5)** Order matters: `numMap[complement]` is the earlier index, `i` the current one.
LeetCode accepts either order here, but returning them ascending is the convention.

**(6)** Insert **after** the check. Otherwise, with `target = 6` and `nums = [3, 3]`, the
first `3` would find itself and return `[0, 0]` — the same element used twice, which the
problem forbids. Checking first guarantees the partner is a *different, earlier* element.

**(7)** Unreachable given the problem's guarantee, but Python needs a return and the type
hint promises a list.

### Complexity
- **Time O(n)** — one pass; hashing and lookup are O(1) each.
- **Space O(n)** — the dict holds up to n entries.

### Pitfalls
- **Inserting before checking** is *the* bug in this problem. See (6).
- If the array were sorted and you needed *values* not indices, two pointers would give
  O(1) space — see Day 2.
- Duplicate values are fine: `numMap[3] = 0` then `numMap[3] = 1` overwrites, but we already
  looked up the earlier one before the overwrite.

### Try next
[3Sum (Day 2)](https://leetcode.com/problems/3sum/) ·
[Two Sum II — sorted input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) ·
[Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)

---

## 3. Find All Numbers Disappeared in an Array

**[LeetCode 448 →](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)** · Easy · Hash set · [`03-Number_Disappered.py`](../03-Number_Disappered.py)

### In one line
`nums` has n elements, each in `[1, n]`. Return every value in `[1, n]` that's missing.

```
[4,3,2,7,8,2,3,1] → [5,6]
```

### Recognise it
"Array of size n containing values in range 1..n" is a huge signal. It means the values and
the indices are the *same universe*, which enables both the set solution and a clever
O(1)-space one.

### Intuition
Build a set of what's present, then walk `1..n` and collect what isn't there. The set makes
each "is `i` present?" O(1); without it you'd rescan the array for every `i` — O(n²).

### Dry run — `nums = [4,3,2,7,8,2,3,1]`, n = 8

`set_nums = {1,2,3,4,7,8}` (note: duplicates collapse, so the set has 6 elements, not 8)

| `i` | in set? | `ret` |
|---|---|---|
| 1–4 | yes | `[]` |
| 5 | **no** | `[5]` |
| 6 | **no** | `[5,6]` |
| 7, 8 | yes | `[5,6]` |

### The code

```python
class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        set_nums = set(nums)                 # (1)
        ret = []
        for i in range(1, len(nums) + 1):    # (2)
            if i not in set_nums:            # (3)
                ret.append(i)
        return ret
```

**(1)** `set(nums)` builds the set in one O(n) pass. Duplicates silently collapse, which is
exactly what we want — we only care about presence.

**(2)** `range(1, len(nums) + 1)` — the values are **1-indexed**, so we start at 1 and the
`+1` makes the range inclusive of n. Getting this wrong by one is the most common error
here. Note it uses `len(nums)`, not `len(set_nums)`: n is the array length, and the set is
smaller when there are duplicates.

**(3)** O(1) membership. With a list here the loop would be O(n²).

### Complexity
- **Time O(n)** — O(n) to build the set + O(n) to scan the range = O(2n) = O(n).
- **Space O(n)** for the set. The output list isn't counted as auxiliary space (you're
  required to produce it).

### The O(1)-space follow-up (interviewers ask for this)
Use the array itself as the hash table. For each value `v`, mark index `|v|-1` negative;
afterwards any index still positive was never marked, so `index + 1` is missing.

```python
for num in nums:
    idx = abs(num) - 1              # values are 1..n, indices 0..n-1
    nums[idx] = -abs(nums[idx])     # -abs, not *= -1: idempotent if we hit it twice
return [i + 1 for i, num in enumerate(nums) if num > 0]
```
**O(n) time, O(1) extra space** — at the cost of mutating the input. The `abs()` calls are
what let you read a value you may already have flipped.

### Try next
[Find All Duplicates in an Array](https://leetcode.com/problems/find-all-duplicates-in-an-array/) ·
[First Missing Positive](https://leetcode.com/problems/first-missing-positive/) (hard, same trick) ·
[Set Mismatch](https://leetcode.com/problems/set-mismatch/)

---

## 4. Valid Anagram `LC-242`

**[LeetCode 242 →](https://leetcode.com/problems/valid-anagram/)** · Easy · Frequency count · *new*

### In one line
Is `t` a rearrangement of `s`?

```
s="anagram", t="nagaram" → True        s="rat", t="car" → False
```

### Recognise it
"Anagram", "rearrangement", "same characters". Any question about *what* characters are
present and *how many* — order irrelevant — is a frequency count.

### Intuition
Two strings are anagrams exactly when their character counts match. Build a tally for each
and compare. Length differing is an instant `False` and saves the work.

### Dry run — `s = "rat"`, `t = "car"`

| char | `counts` after |
|---|---|
| `r` (+1 from s) | `{r: 1}` |
| `a` (+1 from s) | `{r: 1, a: 1}` |
| `t` (+1 from s) | `{r: 1, a: 1, t: 1}` |
| `c` (−1 from t) | `{r: 1, a: 1, t: 1, c: -1}` |
| `a` (−1 from t) | `{r: 1, a: 0, t: 1, c: -1}` |
| `r` (−1 from t) | `{r: 0, a: 0, t: 1, c: -1}` |

Not all zero → **False**.

### The code

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):                      # (1)
            return False

        counts = {}
        for c in s:
            counts[c] = counts.get(c, 0) + 1      # (2)
        for c in t:
            counts[c] = counts.get(c, 0) - 1      # (3)

        return all(v == 0 for v in counts.values())   # (4)
```

**(1)** Cheap O(1) rejection. Different lengths can never be anagrams, and this guard also
means the single-dict trick in (3) is sound.

**(2)** `dict.get(c, 0)` returns 0 for a missing key instead of raising `KeyError`. The
alternative, `defaultdict(int)`, does the same thing implicitly.

**(3)** **One dict, not two.** Count up for `s`, down for `t`. Anagrams cancel to all zeros.
Halves the memory and skips the comparison pass.

**(4)** `all(...)` short-circuits on the first non-zero. The generator expression (no
brackets) avoids building an intermediate list.

### The idiomatic one-liner
```python
from collections import Counter
return Counter(s) == Counter(t)
```
Identical complexity. Write this in real code; write the manual version in an interview
when they ask you to show the mechanism.

### Complexity
- **Time O(n)** — two passes over strings of length n.
- **Space O(k)** where k is the alphabet size. For lowercase English, k ≤ 26, so this is
  effectively **O(1)** — worth saying, it shows you read the constraints.

### Pitfalls
- `sorted(s) == sorted(t)` also works and is a legitimate answer — but it's O(n log n).
  Counting is O(n). Know both and know why you'd pick one.
- Unicode follow-up: the counting solution already handles it; a fixed `[0]*26` array does not.

### Try next
[Group Anagrams (next)](https://leetcode.com/problems/group-anagrams/) ·
[Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) ·
[Ransom Note](https://leetcode.com/problems/ransom-note/)

---

## 5. Group Anagrams `LC-49`

**[LeetCode 49 →](https://leetcode.com/problems/group-anagrams/)** · Medium · Hash map with a computed key · *new*

### In one line
Group words that are anagrams of each other.

```
["eat","tea","tan","ate","nat","bat"] → [["eat","tea","ate"],["tan","nat"],["bat"]]
```

### Recognise it
"Group by", "bucket together", "collect all X that share Y". The pattern is always: **find a
key that is identical for everything that belongs together**, then use a dict of lists.

### Intuition
The whole problem is *"what key do anagrams share?"* Two answers:

1. **The sorted word.** `"eat"`, `"tea"`, `"ate"` all sort to `"aet"`. Simple. O(k log k) per word.
2. **The letter-count tuple.** A 26-slot count vector, as a tuple so it's hashable. O(k) per word.

Once you have the key, `defaultdict(list)` does the grouping.

### Dry run — `["eat", "tea", "tan"]` (sorted-key version)

| word | key | `groups` after |
|---|---|---|
| `eat` | `aet` | `{aet: [eat]}` |
| `tea` | `aet` | `{aet: [eat, tea]}` |
| `tan` | `ant` | `{aet: [eat, tea], ant: [tan]}` |

### The code

```python
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)                # (1)

        for word in strs:
            count = [0] * 26                      # (2)
            for c in word:
                count[ord(c) - ord('a')] += 1     # (3)
            groups[tuple(count)].append(word)     # (4)

        return list(groups.values())              # (5)
```

**(1)** `defaultdict(list)` auto-creates an empty list on first touch, so `groups[key].append(w)`
works without a `if key not in groups` guard. With a plain dict you'd need `groups.setdefault(key, []).append(w)`.

**(2)** A fixed 26-slot array — the problem guarantees lowercase English letters. Fixed size
means this is O(1) space per word, not O(k).

**(3)** `ord(c) - ord('a')` maps `'a'→0 … 'z'→25`. `ord()` gives the Unicode code point;
subtracting the base turns a letter into an array index. This is the standard
letter-to-index idiom and you'll use it constantly.

**(4)** **`tuple(count)`, not `count`.** A list is mutable and therefore unhashable —
`groups[[1,0,...]]` raises `TypeError: unhashable type: 'list'`. Converting to a tuple makes
it a legal dict key. This is the single most instructive line in the problem.

**(5)** `.values()` is a view object, not a list; `list(...)` materialises it to match the
return type.

### The shorter version
```python
groups[tuple(sorted(word))].append(word)     # or "".join(sorted(word))
```
Fewer lines, but O(k log k) per word instead of O(k). Both are accepted; mention the
difference and you've shown you understand the trade.

### Complexity
Let n = number of words, k = max word length.
- **Count-key version: O(n · k)** — each word scanned once, and the 26-slot key is O(1) to build and hash.
- **Sorted-key version: O(n · k log k)** — the sort dominates.
- **Space O(n · k)** for the groups.

### Try next
[Valid Anagram](https://leetcode.com/problems/valid-anagram/) ·
[Top K Frequent Elements (Day 3)](https://leetcode.com/problems/top-k-frequent-elements/) ·
[Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/)

---

## 6. How Many Numbers Are Smaller Than the Current Number

**[LeetCode 1365 →](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/)** · Easy · Sort + hash map · [`05-Smaller_than_current.py`](../05-Smaller_than_current.py)

### In one line
For each `nums[i]`, count how many *other* elements are strictly smaller.

```
[8,1,2,2,3] → [4,0,1,1,3]
```

### Recognise it
"How many are smaller/greater than each" → sorting turns rank into position. The extra
wrinkle is duplicates, which the dict handles.

### Intuition
Sort the array. Now **an element's index in the sorted array is exactly the number of
elements smaller than it** — provided you take the *first* index of each distinct value,
so duplicates all report the same (correct) count.

`[1,2,2,3,8]`: `1` sits at index 0 (0 smaller), `2` first appears at index 1 (1 smaller —
and the second `2` also has 1 smaller, not 2, because "strictly smaller" excludes its twin),
`3` at index 3, `8` at index 4.

Then one lookup pass restores the original order.

### Dry run — `nums = [8,1,2,2,3]`

`temp = sorted(nums) = [1,2,2,3,8]`

Building `dic` (first index only):

| i | num | `num in dic`? | `dic` after |
|---|---|---|---|
| 0 | 1 | no | `{1:0}` |
| 1 | 2 | no | `{1:0, 2:1}` |
| 2 | 2 | **yes → skip** | unchanged ← the duplicate guard |
| 3 | 3 | no | `{1:0, 2:1, 3:3}` |
| 4 | 8 | no | `{1:0, 2:1, 3:3, 8:4}` |

Second pass over the original `[8,1,2,2,3]` → `[4,0,1,1,3]`.

### The code

```python
class Solution:
    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        temp = sorted((nums))                # (1)
        dic = {}
        for i, num in enumerate(temp):       # (2)
            if num not in dic:               # (3)
                dic[num] = i

        ret = []
        for i in nums:                       # (4)
            ret.append(dic[i])

        return ret
```

**(1)** `sorted()` returns a **new** list, leaving `nums` untouched — essential, because the
last loop needs the original order. `nums.sort()` would sort in place and destroy it. (The
doubled parentheses are a harmless typo — `sorted((nums))` is just `sorted(nums)`.)

**(2)** `enumerate` gives value and position together; the position *is* the count.

**(3)** **The duplicate guard.** Without it, the second `2` would overwrite `dic[2] = 1`
with `2`, and both `2`s would report 2 smaller instead of 1. Keeping only the *first*
occurrence is what makes "strictly smaller" correct.

**(4)** `i` here is a *value*, not an index — slightly misleading naming, but correct.
`for num in nums: ret.append(dic[num])` reads better.

### Complexity
- **Time O(n log n)** — the sort dominates; the two linear passes are O(n).
- **Space O(n)** — sorted copy plus dict.

### The counting-sort alternative — O(n) when values are bounded
The constraints say `0 <= nums[i] <= 100`. That tiny range unlocks a linear solution:

```python
count = [0] * 101
for x in nums:
    count[x] += 1
prefix = [0] * 101
for v in range(1, 101):
    prefix[v] = prefix[v-1] + count[v-1]      # how many values are < v
return [prefix[x] for x in nums]
```
**O(n + 101) = O(n) time, O(1) space** (101 is a constant). Spotting that a bounded value
range lets you skip the sort is exactly the kind of constraint-reading Day 3 will lean on.

### Try next
[Rank Transform of an Array](https://leetcode.com/problems/rank-transform-of-an-array/) ·
[Sort Array by Increasing Frequency](https://leetcode.com/problems/sort-array-by-increasing-frequency/) ·
[Relative Sort Array](https://leetcode.com/problems/relative-sort-array/)

---

## 7. Contains Duplicate II

**[LeetCode 219 →](https://leetcode.com/problems/contains-duplicate-ii/)** · Easy · Sliding window + hash set · [`12-Contains_duplicates2.py`](../12-Contains_duplicates2.py)

### In one line
Is there a duplicate pair whose indices are **at most `k` apart**?

```
nums=[1,2,3,1], k=3 → True         nums=[1,2,3,1,2,3], k=2 → False
```

### Recognise it
Problem 1 plus a *distance* constraint. "Within k indices", "nearby duplicate". The fix is
to stop remembering things that have fallen out of range — a hash set that also slides.
This is your first sliding window, one day early.

### Intuition
The naive fix is to check `abs(i - j) <= k` for every duplicate — back to O(n²). Instead,
make the set *only ever contain the last k elements*. Then "is it in the set" already
means "is it a duplicate within k". You never check distance explicitly; the window
enforces it.

### Dry run — `nums = [1,2,3,1]`, `k = 3`

| i | num | in `seen`? | after add | `len > k`? | `seen` |
|---|---|---|---|---|---|
| 0 | 1 | no | `{1}` | 1 > 3 no | `{1}` |
| 1 | 2 | no | `{1,2}` | no | `{1,2}` |
| 2 | 3 | no | `{1,2,3}` | no | `{1,2,3}` |
| 3 | 1 | **yes** | — | — | **return True** |

And `nums = [1,2,3,1]`, `k = 2` — the window evicts in time:

| i | num | in `seen`? | after add | `len > 2`? | evict `nums[i-k]` | `seen` |
|---|---|---|---|---|---|---|
| 0 | 1 | no | `{1}` | no | | `{1}` |
| 1 | 2 | no | `{1,2}` | no | | `{1,2}` |
| 2 | 3 | no | `{1,2,3}` | **yes** | remove `nums[0]`=1 | `{2,3}` |
| 3 | 1 | **no** — 1 was evicted | `{1,2,3}` | yes | remove `nums[1]`=2 | `{1,3}` |

→ `False`. Correct: the two `1`s are 3 apart, and `k = 2`.

### The code

```python
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        seen = set()
        for i, num in enumerate(nums):     # (1)
            if num in seen:                # (2)
                return True
            seen.add(num)
            if len(seen) > k:              # (3)
                seen.remove(nums[i - k])   # (4)
        return False
```

**(1)** We need `i` to know which element to evict, so `enumerate`, not a bare `for num in nums`.

**(2)** Same check as problem 1 — but because of (3)–(4) the set only holds the last `k`
elements, so a hit automatically means "within k". The distance test is *structural*, never
written down.

**(3)** After adding, the window holds indices `i-k … i`, which is `k+1` elements. So
`len(seen) > k` is the signal that it's one too big. (It's `len(seen)`, not `i > k`, which
also handles duplicates collapsing in the set.)

**(4)** `nums[i - k]` is the element that just fell out of range. Note we index into `nums`,
not the set — a set has no order, so we must recompute *which value* to drop from the array.

### Complexity
- **Time O(n)** — one pass; add/remove/lookup are O(1).
- **Space O(min(n, k))** — the set never exceeds k+1 elements. Worth stating precisely; it's
  better than O(n) when k is small.

### Pitfalls
- `k = 0`: the set is emptied on every iteration, so nothing is ever found — correct, since
  indices can't be 0 apart and distinct.
- The dict alternative — store `value → last index`, check `i - dic[num] <= k` — also works
  and is O(n) space. The sliding set is tighter.

### Try next
[Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/) ·
[Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) ·
[Minimum Size Subarray Sum (Day 2)](https://leetcode.com/problems/minimum-size-subarray-sum/)

---

## 8. Missing Number

**[LeetCode 268 →](https://leetcode.com/problems/missing-number/)** · Easy · Maths (Gauss sum) · [`02-Missing_number.py`](../02-Missing_number.py)

### In one line
`nums` contains n distinct values from `[0, n]`. One is missing — find it.

```
[3,0,1] → 2         [0,1] → 2         [9,6,4,2,3,5,7,0,1] → 8
```

### Recognise it
"Distinct values from a known contiguous range, one missing." The hash-set answer is
obvious; the point of this problem is the **O(1) space** answer.

### Intuition
You know what the sum *should* be: `0 + 1 + … + n = n(n+1)/2` (Gauss's formula). You can
compute what it *actually* is. The difference is the missing number, because every present
value cancels.

### Dry run — `nums = [3,0,1]`, n = 3

- `sum_n = 3·4/2 = 6` (the sum of 0+1+2+3)
- `sum_arr = 3+0+1 = 4`
- missing = 6 − 4 = **2**

### The code

```python
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        sum_n = n*(n+1)//2            # (1)
        sum_arr = 0
        for i in range(n):            # (2)
            sum_arr += nums[i]

        missing_num = sum_n - sum_arr # (3)
        return missing_num
```

**(1)** `//` and not `/`. `n*(n+1)` is always even so the division is exact, but `/` returns
a **float** — and above 2⁵³ floats lose integer precision, which can return a wrong answer
on large inputs. Use `//` whenever the result must be an integer. Also note `n = len(nums)`
is correct: n elements covering `[0, n]` means exactly one of the n+1 slots is empty.

**(2)** A plain accumulation loop. `sum(nums)` is the same thing and faster (it's C code).

**(3)** Subtraction. Every value present in `nums` appears in both sums and cancels; only
the missing one survives.

### Complexity
- **Time O(n)** — one pass.
- **Space O(1)** — two integers, no matter how large the input. *This is the point.* The set
  version is also O(n) time but O(n) space.

### The XOR alternative — same idea, no overflow risk
```python
result = len(nums)                  # start with n, which range(n) below never produces
for i, num in enumerate(nums):
    result ^= i ^ num
return result
```
Every index `0..n-1` and every value XOR together; matched pairs cancel and the missing
value survives. Immune to integer overflow, which matters in Java or C++ (not in Python,
where ints are arbitrary precision) — good to mention.

### Try next
[Single Number (next)](https://leetcode.com/problems/single-number/) ·
[Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) ·
[Missing Number In Arithmetic Progression](https://leetcode.com/problems/missing-number-in-arithmetic-progression/)

---

## 9. Single Number

**[LeetCode 136 →](https://leetcode.com/problems/single-number/)** · Easy · XOR · [`15-Single_number.py`](../15-Single_number.py)

### In one line
Every element appears twice except one. Find it — in **O(n) time and O(1) space**.

```
[4,1,2,1,2] → 4
```

### Recognise it
"Everything appears twice except one" plus an explicit **constant space** requirement. The
constant-space demand is the tell: a hash set would be O(n) space, so they want XOR.

### Intuition
XOR has exactly the two properties you need:

- `x ^ x = 0` — a value cancels its own duplicate
- `x ^ 0 = x` — zero is the identity

and it's commutative and associative, so **order doesn't matter**. XOR the whole array
together: every pair annihilates regardless of where the partners sit, and the lone element
is XORed with 0, leaving itself.

### Dry run — `nums = [4,1,2,1,2]`

| step | operation | binary | `xor` |
|---|---|---|---|
| start | | `000` | 0 |
| ^4 | `0 ^ 4` | `100` | 4 |
| ^1 | `4 ^ 1` | `101` | 5 |
| ^2 | `5 ^ 2` | `111` | 7 |
| ^1 | `7 ^ 1` | `110` | 6 |
| ^2 | `6 ^ 2` | `100` | **4** |

Rearranged, this is `(1^1) ^ (2^2) ^ 4 = 0 ^ 0 ^ 4 = 4`.

### The code

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        xor = 0                    # (1)
        n = len(nums)
        for i in range(n):
            xor = xor ^ nums[i]    # (2)

        return xor
```

**(1)** Start at **0**, the XOR identity — `0 ^ x == x`, so the first element passes through
untouched. Starting at any other value would corrupt the result.

**(2)** `^` is bitwise XOR. `xor ^= nums[i]` is the shorter form.

### Complexity
- **Time O(n)** — one pass, one O(1) machine instruction per element.
- **Space O(1)** — a single integer. That's the whole reason this solution exists.

### Pitfalls
- This only works when duplicates come in **pairs**. If elements appeared three times you'd
  need bit-by-bit counting mod 3 (see Single Number II).
- Don't confuse `^` with `**` (exponent) — a genuinely common typo.

### Try next
[Single Number II — appears 3×](https://leetcode.com/problems/single-number-ii/) ·
[Single Number III — two singles](https://leetcode.com/problems/single-number-iii/) ·
[Missing Number](https://leetcode.com/problems/missing-number/)

---

## 10. Counting Bits

**[LeetCode 338 →](https://leetcode.com/problems/counting-bits/)** · Easy · Bit DP · [`19-Counting_bits.py`](../19-Counting_bits.py)

### In one line
For every `i` from 0 to n, return how many 1-bits `i` has.

```
n = 5 → [0,1,1,2,1,2]      (0=0b0, 1=0b1, 2=0b10, 3=0b11, 4=0b100, 5=0b101)
```

### Recognise it
"For every i from 0 to n, compute f(i)" — an array of answers where later ones can reuse
earlier ones. That is dynamic programming, and today it's your first taste of it.

### Intuition
Counting bits for each number independently is O(n log n). Instead, notice that `i >> 1`
(i with its last bit chopped off) is a *smaller number you have already solved*. So:

> bits(i) = bits(i without its last bit) + (that last bit)

`i >> 1` is `i // 2`. `i & 1` is the last bit: 1 if odd, 0 if even.

```
i = 5 = 0b101
i >> 1 = 0b10 = 2, which has 1 bit  →  ans[2] = 1
i & 1  = 1                          →  the last bit
bits(5) = 1 + 1 = 2   ✓
```

Because `i >> 1 < i`, the answer you need is always already computed. That's the DP.

### Dry run — `n = 5`

| i | binary | `i >> 1` | `ans[i>>1]` | `i & 1` | `ans[i]` |
|---|---|---|---|---|---|
| 0 | `0` | — | — | — | 0 (base) |
| 1 | `1` | 0 | 0 | 1 | **1** |
| 2 | `10` | 1 | 1 | 0 | **1** |
| 3 | `11` | 1 | 1 | 1 | **2** |
| 4 | `100` | 2 | 1 | 0 | **1** |
| 5 | `101` | 2 | 1 | 1 | **2** |

### The code

```python
class Solution:
    def countBits(self, n: int) -> List[int]:
        ans = [0] * (n+1)                    # (1)
        for i in range(1,n+1):               # (2)
            ans[i] = ans[i >> 1] + (i & 1)   # (3)
        return ans
```

**(1)** `[0] * (n+1)` — **n+1** slots because the answer covers `0..n` inclusive. This also
sets the base case `ans[0] = 0` for free (zero has no 1-bits).

**(2)** Start at 1: index 0 is already correct, and `0 >> 1` would just be 0 again.

**(3)** The recurrence. Three things worth noting:
- `i >> 1` is `i // 2`, but the shift makes the *intent* — "drop the last bit" — explicit.
- `i & 1` isolates the last bit: `5 & 1 = 0b101 & 0b001 = 1`.
- **The parentheses around `(i & 1)` are mandatory.** In Python `+` binds tighter than `&`,
  so `ans[i>>1] + i & 1` parses as `(ans[i>>1] + i) & 1` — completely wrong. Whenever you
  mix bitwise and arithmetic operators, parenthesise. This is a real and frequent bug.

### Complexity
- **Time O(n)** — n iterations of O(1) work. The naive "count bits of each number" is
  O(n log n); this reuses previous answers to get to linear.
- **Space O(n)** for the output, O(1) auxiliary.

### An alternative recurrence
```python
ans[i] = ans[i & (i - 1)] + 1
```
`i & (i-1)` clears the **lowest set bit**, so it's "this number with one bit removed, plus
one". Equally O(n). Worth knowing because `i & (i-1)` is the standard "is this a power of
two?" test (`i & (i-1) == 0`).

### Try next
[Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) ·
[Reverse Bits](https://leetcode.com/problems/reverse-bits/) ·
[Power of Two](https://leetcode.com/problems/power-of-two/)

---

## Recall drill

No scrolling. Write the answers down, then check.

1. You wrote `if x in seen:` inside a loop over n elements. What is the total complexity if
   `seen` is a list? If it's a set? Why?
2. In Two Sum, why must `numMap[nums[i]] = i` come *after* the `if complement in numMap` check?
3. Write the hash-map complement template from memory. Five lines.
4. Why does `groups[count]` throw `TypeError` when `count` is a list, and what's the fix?
5. Give the two XOR identities that make Single Number work, and say why order doesn't matter.

<details>
<summary>Answers</summary>

1. **List → O(n²)**: each `in` scans up to n elements, n times. **Set → O(n)**: each `in` is
   an O(1) hash lookup. Same code, different data structure, quadratic difference.
2. Otherwise an element finds *itself* as its own complement. With `nums=[3,3], target=6`,
   inserting first makes `i=0` look up `3`, find the entry it just wrote, and return `[0,0]`
   — using one element twice, which the problem forbids.
3. ```python
   seen = {}
   for i, x in enumerate(nums):
       if target - x in seen:
           return [seen[target - x], i]
       seen[x] = i
   ```
4. Dict keys must be **hashable**, i.e. immutable. Lists are mutable, so they have no stable
   hash. Fix: `tuple(count)`.
5. `x ^ x = 0` (a value cancels its duplicate) and `x ^ 0 = x` (0 is the identity). XOR is
   commutative *and* associative, so the pairs cancel wherever they sit in the array.

</details>

---

**Tomorrow:** [Day 2 — Two Pointers, Sliding Window & Prefix Sums](./day-2-two-pointers-sliding-window.md).
Today you bought speed with memory. Tomorrow you'll get speed for free by exploiting
*order* — and you'll meet the technique that solves more LeetCode mediums than any other:
the sliding window.

**Warm-up for tomorrow:** re-solve **Two Sum** and **Single Number** from a blank screen
before you read anything. Ten minutes.
