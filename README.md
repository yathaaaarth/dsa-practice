# DSA Practice — 50 Solved Problems + a 7-Day Study Guide

Python solutions to 50 LeetCode problems, worked through alongside the
[Stoney Codes "70 LeetCode problems in 5+ hours" tutorial](https://www.youtube.com/results?search_query=stoney+codes+70+leetcode+problems),
plus a complete study guide built around them.

> **📖 Start here → [`guide/`](./guide/README.md)** — a 7-day, 70-problem course with a
> LeetCode link, an annotated solution, a hand dry-run and derived complexity for every
> problem. Or open [`guide/study-guide.html`](./guide/study-guide.html) in a browser for the
> whole thing on one page (Ctrl/Cmd-P → Save as PDF).

---

## The guide

| | |
|---|---|
| [**Index & progress tracker**](./guide/README.md) | the 7-day calendar, tick problems off as you go |
| [How to use this guide](./guide/00-how-to-use.md) | the study loop, daily shape, spaced-review schedule |
| [Python for DSA](./guide/01-python-for-dsa.md) | why `set` not `list`, `//` not `/`, `deque` not `pop(0)`, `heapq`, slicing, sentinels |
| [Complexity](./guide/02-complexity.md) | deriving Big-O instead of memorising it; reading the intended solution off the constraints |
| [**Pattern cheat sheet**](./guide/03-pattern-cheatsheet.md) | trigger phrase → pattern → template. 15 templates covering most of LeetCode |
| [Bugs found in this repo](./guide/bugs-found.md) | six of these solutions were broken. What went wrong, and how to catch each class of mistake |

**The seven days:** [1 · Hashing](./guide/day-1-hashing.md) ·
[2 · Two Pointers & Sliding Window](./guide/day-2-two-pointers-sliding-window.md) ·
[3 · Binary Search & Heaps](./guide/day-3-binary-search-heaps.md) ·
[4 · Stacks & Queues](./guide/day-4-stacks-queues.md) ·
[5 · Linked Lists](./guide/day-5-linked-lists.md) ·
[6 · Binary Trees](./guide/day-6-trees.md) ·
[7 · BST, Graphs, Backtracking & DP](./guide/day-7-bst-graphs-backtracking-dp.md)

The guide covers **70 problems**: the 50 in this repo, plus 20 added to fill gaps the
original set left open — there was no binary search, no heap, and no monotonic stack
anywhere in it.

## Verifying the solutions

Every solution here is executed against LeetCode's sample cases plus edge cases:

```bash
python3 guide/verify.py        # 50/50 expected
```

These files are written to be pasted into LeetCode, which silently pre-imports `List`,
`Optional`, `deque`, `TreeNode` and `ListNode` — so they can't just be run locally. The
harness injects those names, which is also how six broken solutions were found and fixed
(see [`guide/bugs-found.md`](./guide/bugs-found.md)).

To rebuild the single-page HTML after editing the Markdown:

```bash
pip install markdown && python3 guide/build_html.py
```

---

## The problems

### Arrays & Hashing
- [Contains Duplicate](./01-Duplicate_value.py) — [LC 217](https://leetcode.com/problems/contains-duplicate/)
- [Missing Number](./02-Missing_number.py) — [LC 268](https://leetcode.com/problems/missing-number/)
- [Find All Numbers Disappeared in an Array](./03-Number_Disappered.py) — [LC 448](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)
- [Two Sum](./04-Two_sum.py) — [LC 1](https://leetcode.com/problems/two-sum/)
- [How Many Numbers Are Smaller Than the Current Number](./05-Smaller_than_current.py) — [LC 1365](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/)
- [Minimum Time Visiting All Points](./06-Minimum_time_visit.py) — [LC 1266](https://leetcode.com/problems/minimum-time-visiting-all-points/)
- [Spiral Matrix](./07-Spiral_matrix.py) — [LC 54](https://leetcode.com/problems/spiral-matrix/)
- [Number of Islands](./08-Number_of_Island.py) — [LC 200](https://leetcode.com/problems/number-of-islands/)
- [Best Time to Buy and Sell Stock](./09-Best_time_sell_stock.py) — [LC 121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
- [Squares of a Sorted Array](./10-Square-sorted_array.py) — [LC 977](https://leetcode.com/problems/squares-of-a-sorted-array/)
- [Longest Mountain in Array](./11-Longest_mountain_Array.py) — [LC 845](https://leetcode.com/problems/longest-mountain-in-array/)
- [Contains Duplicate II](./12-Contains_duplicates2.py) — [LC 219](https://leetcode.com/problems/contains-duplicate-ii/)
- [Minimum Absolute Difference](./13-Minimum_Absolute_diff.py) — [LC 1200](https://leetcode.com/problems/minimum-absolute-difference/)
- [Minimum Size Subarray Sum](./14-Minimum_size_subarray_sum.py) — [LC 209](https://leetcode.com/problems/minimum-size-subarray-sum/)
- [Single Number](./15-Single_number.py) — [LC 136](https://leetcode.com/problems/single-number/)

### Dynamic Programming & Bits
- [Coin Change](./16-Coin_change.py) — [LC 322](https://leetcode.com/problems/coin-change/)
- [Climbing Stairs](./17-climbing_stairs.py) — [LC 70](https://leetcode.com/problems/climbing-stairs/)
- [Maximum Subarray](./18-maximum_subarray.py) — [LC 53](https://leetcode.com/problems/maximum-subarray/)
- [Counting Bits](./19-Counting_bits.py) — [LC 338](https://leetcode.com/problems/counting-bits/)
- [Range Sum Query — Immutable](./20-Range_sum_query.py) — [LC 303](https://leetcode.com/problems/range-sum-query-immutable/)

### Backtracking
- [Letter Case Permutation](./21-letterCase.py) — [LC 784](https://leetcode.com/problems/letter-case-permutation/)
- [Subsets](./22-Subsets.py) — [LC 78](https://leetcode.com/problems/subsets/)
- [Combinations](./23-Combinations.py) — [LC 77](https://leetcode.com/problems/combinations/)
- [Permutations](./24-permutation.py) — [LC 46](https://leetcode.com/problems/permutations/) ⚙️ *fixed*

### Linked Lists
- [Middle of the Linked List](./25-Middle_ll.py) — [LC 876](https://leetcode.com/problems/middle-of-the-linked-list/)
- [Linked List Cycle](./26-Cycle_ll.py) — [LC 141](https://leetcode.com/problems/linked-list-cycle/)
- [Reverse Linked List](./27-Reversed_ll.py) — [LC 206](https://leetcode.com/problems/reverse-linked-list/)
- [Remove Linked List Elements](./28-Remove_ll_element.py) — [LC 203](https://leetcode.com/problems/remove-linked-list-elements/)
- [Reverse Linked List II](./29-Reversed_ll.py) — [LC 92](https://leetcode.com/problems/reverse-linked-list-ii/) ⚙️ *newly written*
- [Palindrome Linked List](./30-Palindrome.py) — [LC 234](https://leetcode.com/problems/palindrome-linked-list/)
- [Merge Two Sorted Lists](./31-Merg_sorted_ll.py) — [LC 21](https://leetcode.com/problems/merge-two-sorted-lists/)

### Stacks & Queues
- [Min Stack](./32-minstack.py) — [LC 155](https://leetcode.com/problems/min-stack/)
- [Valid Parentheses](./33-Valid_Parenthese.py) — [LC 20](https://leetcode.com/problems/valid-parentheses/)
- [Evaluate Reverse Polish Notation](./34-eval_reverse_polish_notation.py) — [LC 150](https://leetcode.com/problems/evaluate-reverse-polish-notation/) ⚙️ *fixed*
- [Sort a Stack](./35-stack_sorting.py) — [GfG](https://www.geeksforgeeks.org/problems/sort-a-stack/1)
- [Implement Stack using Queues](./36-implement_stack_queues.py) — [LC 225](https://leetcode.com/problems/implement-stack-using-queues/)
- [Time Needed to Buy Tickets](./37-time_need_buy_ticket.py) — [LC 2073](https://leetcode.com/problems/time-needed-to-buy-tickets/) ⚙️ *fixed*
- [Reverse First K Elements of a Queue](./38-Reverse_first_k_ele_queue.py) — [GfG](https://www.geeksforgeeks.org/problems/reverse-first-k-elements-of-queue/1)

### Binary Trees
- [Average of Levels in Binary Tree](./39-avg_level_bt.py) — [LC 637](https://leetcode.com/problems/average-of-levels-in-binary-tree/)
- [Minimum Depth of Binary Tree](./40_mini_depth_bt.py) — [LC 111](https://leetcode.com/problems/minimum-depth-of-binary-tree/) ⚙️ *fixed*
- [Maximum Depth of Binary Tree](./41-Max_depth_bt.py) — [LC 104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
- [Binary Tree Level Order Traversal](./42-Level_order_traversal_bt.py) — [LC 102](https://leetcode.com/problems/binary-tree-level-order-traversal/)
- [Same Tree](./43-Same_tree.py) — [LC 100](https://leetcode.com/problems/same-tree/)
- [Path Sum](./44-Path_sum.py) — [LC 112](https://leetcode.com/problems/path-sum/)
- [Diameter of Binary Tree](./45-Diameter_bt.py) — [LC 543](https://leetcode.com/problems/diameter-of-binary-tree/)
- [Invert Binary Tree](./46-Invert_bt.py) — [LC 226](https://leetcode.com/problems/invert-binary-tree/)
- [Lowest Common Ancestor of a Binary Tree](./47-LCA.py) — [LC 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) ⚙️ *fixed*

### Binary Search Trees
- [Search in a Binary Search Tree](./48-Search_bt.py) — [LC 700](https://leetcode.com/problems/search-in-a-binary-search-tree/)
- [Insert into a Binary Search Tree](./49-Insert_into_BST.py) — [LC 701](https://leetcode.com/problems/insert-into-a-binary-search-tree/)
- [Convert Sorted Array to BST](./50-convert_sorted_array_BST.py) — [LC 108](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) ⚙️ *fixed*

⚙️ marks files that were broken (or missing) and have been corrected — each carries a
`# FIX:` comment, and [`guide/bugs-found.md`](./guide/bugs-found.md) explains what went
wrong and why it's worth studying.
