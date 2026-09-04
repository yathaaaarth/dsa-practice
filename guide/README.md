# DSA in 7 Days — 70 Problems, Pattern by Pattern

A complete self-study guide built around the 50 solutions in this repository, plus 20
problems added to fill genuine gaps. Every problem gets a LeetCode link, an annotated
solution explaining *why each line is written the way it is*, a hand dry-run, and a derived
complexity.

**Start here → [How to use this guide](./00-how-to-use.md)** — it takes four minutes and it
is the difference between finishing the week able to solve new problems and finishing it
able to recite old ones.

---

## Reference pages (keep these open all week)

| Page | What it's for |
|---|---|
| [00 · How to use this guide](./00-how-to-use.md) | The study loop, the daily shape, the spaced-review schedule |
| [01 · Python for DSA](./01-python-for-dsa.md) | Why `set` not `list`, why `//` not `/`, why `deque` not `pop(0)`, `heapq`, slicing, sentinels |
| [02 · Complexity](./02-complexity.md) | How to *derive* Big-O rather than memorise it; reading the intended solution off the constraints |
| [03 · Pattern cheat sheet](./03-pattern-cheatsheet.md) | **The most important page.** Trigger phrase → pattern → template. 15 templates that cover most of LeetCode |
| [Bugs found in the original code](./bugs-found.md) | Six solutions in this repo were broken. What went wrong, and how to catch each class of mistake |

Single-page version for reading offline or printing to PDF:
**[study-guide.html](./study-guide.html)** — open it in a browser, then Ctrl/Cmd-P → Save as PDF.

---

## The seven days

| Day | Theme | Problems | New patterns |
|---|---|---|---|
| [1](./day-1-hashing.md) | Hashing, Sets & Bit Tricks | 10 | hash set, hash map, frequency counting, XOR |
| [2](./day-2-two-pointers-sliding-window.md) | Two Pointers, Sliding Window & Prefix Sums | 10 | converging pointers, variable window, Kadane, prefix sums |
| [3](./day-3-binary-search-heaps.md) | Binary Search & Heaps | 10 | binary search, **search on the answer**, size-k heap |
| [4](./day-4-stacks-queues.md) | Stacks, Queues & Monotonic Stack | 10 | LIFO/FIFO, auxiliary stack, **monotonic stack** |
| [5](./day-5-linked-lists.md) | Linked Lists | 10 | fast & slow pointers, dummy node, in-place reversal |
| [6](./day-6-trees.md) | Binary Trees | 10 | tree DFS, level-order BFS, BST invariant |
| [7](./day-7-bst-graphs-backtracking-dp.md) | BST, Graphs, Backtracking & DP | 10 | grid BFS, backtracking, 1-D DP |

Days 3 and 4 carry the most new material — binary search, heaps and the monotonic stack
were entirely absent from the original 50, and they unlock a large share of LeetCode's
medium tier.

---

## Progress tracker

Tick these off as you go. Re-solving from a blank screen counts; reading does not.

### Day 1 — Hashing, Sets & Bit Tricks
- [ ] Contains Duplicate `#01`
- [ ] Two Sum `#04`
- [ ] Find All Numbers Disappeared in an Array `#03`
- [ ] Valid Anagram `LC-242`
- [ ] Group Anagrams `LC-49`
- [ ] How Many Numbers Are Smaller Than the Current Number `#05`
- [ ] Contains Duplicate II `#12`
- [ ] Missing Number `#02`
- [ ] Single Number `#15`
- [ ] Counting Bits `#19`

### Day 2 — Two Pointers, Sliding Window & Prefix Sums
- [ ] Squares of a Sorted Array `#10`
- [ ] Minimum Absolute Difference `#13`
- [ ] 3Sum `LC-15`
- [ ] Best Time to Buy and Sell Stock `#09`
- [ ] Minimum Size Subarray Sum `#14`
- [ ] Longest Mountain in Array `#11`
- [ ] Minimum Time Visiting All Points `#06`
- [ ] Maximum Subarray `#18`
- [ ] Range Sum Query – Immutable `#20`
- [ ] Spiral Matrix `#07`

### Day 3 — Binary Search & Heaps
- [ ] Binary Search `LC-704`
- [ ] Search Insert Position `LC-35`
- [ ] First Bad Version `LC-278`
- [ ] Search a 2D Matrix `LC-74`
- [ ] Find Minimum in Rotated Sorted Array `LC-153`
- [ ] Koko Eating Bananas `LC-875`
- [ ] Last Stone Weight `LC-1046`
- [ ] Kth Largest Element in an Array `LC-215`
- [ ] Kth Largest Element in a Stream `LC-703`
- [ ] Top K Frequent Elements `LC-347`

### Day 4 — Stacks, Queues & Monotonic Stack
- [ ] Valid Parentheses `#33`
- [ ] Min Stack `#32`
- [ ] Evaluate Reverse Polish Notation `#34`
- [ ] Sort a Stack `#35`
- [ ] Implement Stack using Queues `#36`
- [ ] Time Needed to Buy Tickets `#37`
- [ ] Reverse First K Elements of a Queue `#38`
- [ ] Remove All Adjacent Duplicates In String `LC-1047`
- [ ] Daily Temperatures `LC-739`
- [ ] Next Greater Element I `LC-496`

### Day 5 — Linked Lists
- [ ] Middle of the Linked List `#25`
- [ ] Linked List Cycle `#26`
- [ ] Linked List Cycle II `LC-142`
- [ ] Reverse Linked List `#27`
- [ ] Reverse Linked List II `#29`
- [ ] Remove Linked List Elements `#28`
- [ ] Remove Nth Node From End of List `LC-19`
- [ ] Palindrome Linked List `#30`
- [ ] Merge Two Sorted Lists `#31`
- [ ] Add Two Numbers `LC-2`

### Day 6 — Binary Trees
- [ ] Maximum Depth of Binary Tree `#41`
- [ ] Minimum Depth of Binary Tree `#40`
- [ ] Same Tree `#43`
- [ ] Invert Binary Tree `#46`
- [ ] Path Sum `#44`
- [ ] Diameter of Binary Tree `#45`
- [ ] Average of Levels in Binary Tree `#39`
- [ ] Binary Tree Level Order Traversal `#42`
- [ ] Lowest Common Ancestor of a Binary Tree `#47`
- [ ] Validate Binary Search Tree `LC-98`

### Day 7 — BST, Graphs, Backtracking & DP
- [ ] Search in a Binary Search Tree `#48`
- [ ] Insert into a Binary Search Tree `#49`
- [ ] Convert Sorted Array to BST `#50`
- [ ] Number of Islands `#08`
- [ ] Letter Case Permutation `#21`
- [ ] Subsets `#22`
- [ ] Combinations `#23`
- [ ] Permutations `#24`
- [ ] Coin Change `#16`
- [ ] Climbing Stairs `#17`

---

## Notation

- **`#NN`** — a solution already in this repository, at `NN-*.py`. The guide annotates
  *your* code.
- **`LC-###`** — a problem added to fill a gap. Full annotated solution provided.

## Verifying the code

Every solution in this repo is executed against LeetCode's sample cases plus edge cases:

```bash
python3 guide/verify.py        # expects 50/50
```

Six solutions were broken when this guide was written and are now fixed — see
[bugs-found.md](./bugs-found.md), which is worth reading as study material in its own right.
