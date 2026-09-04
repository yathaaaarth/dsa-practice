# How to Use This Guide

Read this once. It is the difference between finishing the week able to solve new problems
and finishing the week able to recite 70 old ones.

---

## The core problem with studying solutions

Reading a solution feels like learning. It isn't. When you read worked code your brain
reports "yes, that makes sense" — and that feeling of fluency is produced by *recognition*,
which is a completely different skill from *generation*. In an interview nobody shows you
the code. You have to produce it from an empty screen.

Everything below is designed around one rule:

> **You have not learned a problem until you have written it from scratch on a blank screen.**

---

## The loop, per problem (about 20 minutes)

1. **Open the LeetCode link first. Read the problem. Do not scroll down in this guide.**

2. **Try it for 10 minutes.** Genuinely try. Write something, even something bad, even
   brute force. The 10 minutes of struggle is what makes the solution stick — this is not
   motivational filler, it is the single best-supported finding in the learning literature.
   Set a timer so you actually stop.

3. **Read the guide's "Recognise it" and "Intuition" sections — then stop reading and try
   again.** Very often that is all you needed. Solving it after a nudge is worth far more
   than reading the full answer.

4. **Now read the annotated code and the dry run.** Follow the dry-run table with a pen.
   Do not skip the table because it looks tedious; watching the pointers actually move is
   what converts "I see" into "I could rebuild this".

5. **Close everything. Rewrite the solution from memory.** Blank file. If you get stuck,
   peek, then close it and start the file over from the top. This step is the whole
   exercise. If you skip step 5, you have not studied — you have read.

6. **Say the complexity out loud** before moving on. "O(n) time because one pass, O(n)
   space because the set can hold every element." If you can't say it, you don't have it.

---

## The daily shape (about 3 hours)

| Block | Time | What |
|---|---|---|
| Pattern primer | 15 min | Read the top of the day file. Copy the template code out by hand. |
| Problems 1–5 | 75 min | The loop above, ~15 min each |
| Break | 10 min | Actually leave the desk |
| Problems 6–10 | 75 min | Same |
| Recall drill | 10 min | The questions at the bottom of the day file, from memory, no scrolling |

If you have less time, **cut the number of problems, not the loop.** Six problems done
properly beats ten problems read. The schedule serves you, not the other way round.

---

## Spaced review — the part everyone skips

You will forget Day 1 by Day 4. That is normal and it is fixable, but only if you plan for
it. At the start of each day, before new material, re-solve **two problems from memory**
that you have already done:

| Day | Warm-up: re-solve these from a blank screen |
|---|---|
| 2 | Two Sum, Single Number |
| 3 | Best Time to Buy and Sell Stock, Minimum Size Subarray Sum |
| 4 | Binary Search, Kth Largest Element |
| 5 | Valid Parentheses, Daily Temperatures |
| 6 | Reverse Linked List, Merge Two Sorted Lists |
| 7 | Maximum Depth, Level Order Traversal |
| +3 days | Coin Change, Subsets, Number of Islands |
| +1 week | Any five you flag as shaky |

Ten minutes. Non-negotiable. This is what makes the knowledge survive past the week.

---

## Reading the code annotations

Each solution is annotated with numbered markers:

```python
seen = set()          # (1)
for num in nums:      # (2)
    if num in seen:   # (3)
```

The numbers map to explanations under the block. Every marker answers a **why**, not a
what — why `set()` and not `list()`, why `//` and not `/`, why `path + [x]` and not
`path.append(x)`. The *what* you can already read; the *why* is what transfers to the next
problem.

---

## Which problems are yours, which are new

- **`#NN` — your repo.** These 50 are in this repository as `NN-*.py`. The guide links
  each one to the file and annotates *your* code, warts and all.
- **`LC-###` — added.** 20 problems that fill genuine holes in the original 50 (there was
  no binary search, no heap, no monotonic stack in the whole set). Solve these on LeetCode
  directly; the guide gives you the full annotated solution.

Six of the repo files were broken when I found them. Read
[`bugs-found.md`](./bugs-found.md) before Day 1 — those bugs are a free lesson.

---

## What "done" looks like

By Sunday you should be able to, on a blank screen and without help:

- Write a sliding window, a two-pointer scan, and a binary search from muscle memory.
- Look at a problem statement and name the pattern **before** writing any code.
- Say the time and space complexity of anything you write, and justify it.
- Recognise that backtracking, tree DFS, and graph DFS are the same shape of code.

That last one is the whole game. Ten patterns cover a very large share of LeetCode; the
70 problems here are just the vehicle for internalising them.

---

## When you're stuck on a *new* problem (after this week)

Work down this list in order. It is the same list, every time:

1. **What is the input shape?** Sorted array → two pointers or binary search. Contiguous
   subarray/substring → sliding window. Tree → DFS or BFS. Grid → BFS/DFS. "All
   combinations of" → backtracking.
2. **What would brute force be, and what is it costing me?** Name the O(n²) or O(2ⁿ)
   explicitly. You cannot optimise what you have not measured.
3. **What am I recomputing?** If the answer is "the same sum/count/lookup", the fix is a
   hash map, a prefix sum, or a DP table.
4. **Can I trade memory for time?** That is what a hash set *is*.
5. **Is there an ordering I can exploit?** Sorting costs O(n log n) and often unlocks a
   linear scan — a net win over O(n²).

[`03-pattern-cheatsheet.md`](./03-pattern-cheatsheet.md) is this list in table form. Keep
it open while you practise.
