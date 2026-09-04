# Bugs Found in the Original Solutions

Before writing the study guide I executed every file in this repository. Six of them were
broken — three crashed, one would not even import, one silently returned wrong answers, and
one recursed forever. They are all fixed now (each fix carries a `# FIX:` comment in the
source), but the *bugs themselves are worth studying*, because every one of them is a
mistake you will make again under interview pressure.

Read this page once before Day 1. Come back to it whenever your code "looks right" but fails.

---

## 1. `24-permutation.py` — the recursion that never shrank

**Symptom:** `TypeError: can only concatenate list (not "int") to list`

```python
# BROKEN
backtrack(nums[:] + nums[i+1:], path + nums[i])
```

Two separate bugs on one line.

**Bug A — the slice.** `nums[:]` means "a copy of the *whole* list". The author meant
`nums[:i]`, "everything before index i". As written, the recursive call received
*more* elements than it started with, and element `i` was never removed — so the recursion
never approached its base case and never produced a real permutation.

```python
nums = [1, 2, 3]; i = 1
nums[:]  + nums[2:]  # [1, 2, 3, 3]   <-- wrong: nothing removed, 3 duplicated
nums[:1] + nums[2:]  # [1, 3]         <-- right: element at index 1 removed
```

**Bug B — the missing brackets.** `path` is a list and `nums[i]` is an int. `list + int` is
a `TypeError`. You need `path + [nums[i]]` — wrap the single element in a list so `+`
concatenates two lists.

**How to catch it:** in any backtracking function, the recursive call must make the problem
*strictly smaller*. Ask out loud: "is the argument I am passing down shorter than the one I
received?" Here it was longer.

---

## 2. `34-eval_reverse_polish_notation.py` — append takes one argument

**Symptom:** `TypeError: list.append() takes exactly one argument (2 given)`

```python
st.append(first, second)     # BROKEN
st.append(first - second)    # fixed
```

A pure slip, but note *why the tests missed it*: only the `-` branch was wrong, so any test
case built from `+`, `*` and `/` passes. Bugs hide in the branch you did not exercise.

While we are here — the `/` branch is subtle and it is **correct** in the original:

```python
st.append(int(first / second))   # truncates toward zero:  int(-7/2) == -3
# NOT
st.append(first // second)       # floors toward -infinity: -7 // 2 == -4
```

LeetCode asks for truncation toward zero. For negative operands these two differ, so
`//` is a wrong answer here even though it is the usual integer-division idiom.

---

## 3. `37-time_need_buy_ticket.py` — the off-by-one that returned plausible answers

This is the dangerous one: it did not crash, it just answered wrong.

```python
# BROKEN
if tickets[i] <= tickets[k]:
    result += tickets[i]
elif i <= k and tickets[i] >= tickets[k]:
    result += tickets[k]
else:
    result += tickets[k] - 1
```

The correct rule has two cases, keyed on *position*, not on ticket count:

| Position | Tickets that person buys before the answer is fixed |
|---|---|
| `i <= k` (at or ahead of k) | `min(tickets[i], tickets[k])` |
| `i > k` (behind k) | `min(tickets[i], tickets[k] - 1)` |

Behind `k` it is `tickets[k] - 1` because the clock **stops the instant `k` buys their last
ticket** — everyone behind `k` misses that final round.

The broken version tested `tickets[i] <= tickets[k]` *first*, so for `i > k` with
`tickets[i] == tickets[k]` it took the `tickets[i]` branch and over-counted by one.

```
tickets = [2, 2], k = 0
broken  -> 4
correct -> 3     (p0 buys, p1 buys, p0 buys -> done at t=3)
```

`guide/verify.py` now runs this against a brute-force simulator over **every** queue of
length ≤ 4 with values ≤ 4. The old code had 27 mismatches; the fixed code has none.

**How to catch it:** when a solution reduces a simulation to a closed-form formula, write
the ten-line brute force and compare them on small inputs. It takes two minutes and it is
the only way to find an off-by-one that produces believable numbers.

---

## 4. `40_mini_depth_bt.py` — the file that could not even be imported

**Symptom:** `SyntaxError: 'return' outside function`

```python
class Solution:
    def minDepth(self, root):
        def dfs(node):
            ...

    return dfs(root)      # BROKEN: this indentation puts it in the CLASS body
```

`return dfs(root)` was indented four spaces (class-body level) instead of eight
(method-body level). In Python, indentation *is* the syntax, so this is not a style
problem — the file will not compile.

Note that `python3 -c "import ast; ast.parse(src)"` does **not** catch this;
`ast.parse` only builds the parse tree. You need `compile()`, which runs the extra
scope checks:

```bash
python3 -c "compile(open('40_mini_depth_bt.py').read(), 'f', 'exec')"
```

**The algorithm itself is worth a second look too.** Minimum depth is *not* the mirror
image of maximum depth:

```python
if left == 0:  return right + 1     # this node has no left child, so it is NOT a leaf
if right == 0: return left + 1
return min(left, right) + 1
```

`min(left, right)` on a node with one missing child would return `0 + 1`, reporting a path
that ends at a node which still has a child. Minimum depth must end at a **leaf** — a node
with no children at all. Max depth has no such trap, which is why `maxDepth` is three lines
and `minDepth` is six.

---

## 5. `47-LCA.py` — the missing `self.`

**Symptom:** `NameError: name 'lowestCommonAncestor' is not defined`

```python
l = lowestCommonAncestor(root.left, p, q)        # BROKEN
l = self.lowestCommonAncestor(root.left, p, q)   # fixed
```

Methods defined in a class body are **not** module-level functions. Inside a method, the
only way to reach a sibling method is through the instance: `self.name(...)`.

This is why so many LeetCode solutions define an inner helper instead:

```python
def lowestCommonAncestor(self, root, p, q):
    def helper(node):            # a plain closure -- callable by bare name
        ...
        return helper(node.left)
    return helper(root)
```

Both work. The closure version is usually faster to write and avoids exactly this mistake.

---

## 6. `50-convert_sorted_array_BST.py` — two bugs, one line apart

**Symptom:** `TypeError: recursive() takes 2 positional arguments but 3 were given`
— and, once that was fixed, infinite recursion.

```python
def recursive(start, end):
    mid = (start + end) // 2                  # BROKEN: no base case above this
    node = TreeNode(nums[mid])
    node.left  = recursive(nums, 0, mid - 1)  # BROKEN: 3 args, and `0` not `start`
    node.right = recursive(nums, mid + 1, end)
```

**Bug A — arity.** `recursive` takes `(start, end)` but is called with `(nums, 0, mid-1)`.
`nums` does not need passing at all: the inner function closes over it from the enclosing
scope. That is the whole point of defining the helper inside the method.

**Bug B — no base case.** Nothing stops the recursion when the range becomes empty.
Every recursive function needs the "nothing left to do" branch *first*:

```python
if start > end:
    return None
```

**Bug C — the reset to `0`.** Even with the right arity, `recursive(0, mid-1)` restarts the
left bound from the beginning of the array on every level instead of narrowing it, so the
left subtree would be rebuilt from the whole prefix each time.

**How to catch it:** write the base case before you write the recursive call. Always. If you
find yourself typing the recursive call first, stop and type `if <empty>: return <identity>`
above it.

---

## Also worth knowing (these were *not* bugs, but they are not what you should write)

| File | What it does | What to prefer, and why |
|---|---|---|
| `33-Valid_Parenthese.py` | Repeatedly `str.replace("()","")` until the string stops shrinking | Works, but it is **O(n²)** — each pass rebuilds the whole string. The stack solution is O(n) and is what an interviewer expects. Both are shown on Day 4. |
| `39-avg_level_bt.py`, `42-Level_order_traversal_bt.py` | `q.pop(0)` on a plain list | `list.pop(0)` shifts every remaining element: **O(n)** per call, so BFS becomes O(n²). Use `collections.deque` and `popleft()`, which is O(1). |
| `39-avg_level_bt.py` | Enqueues `node.right` before `node.left` | Harmless *here* (a sum does not care about order), but it is the wrong habit — the same code in `levelOrder` would output every level backwards. |
| `07-Spiral_matrix.py` | `matrix.pop(0)` and `row.pop(0)` | Correct, and elegant, but it **destroys the input matrix** and each `pop(0)` is O(n). Interviewers often ask you not to mutate the input. The four-boundary version is shown on Day 2. |
| `08-Number_of_Island.py`, `36-implement_stack_queues.py` | Use `deque` with no import | LeetCode pre-imports it. Locally you need `from collections import deque` — which is why `guide/verify.py` injects it. |

---

## The checklist these six bugs add up to

Before you submit anything:

1. **Base case first.** Write `if <empty>: return <identity>` before the recursive call.
2. **Does the argument shrink?** Say the recursive call out loud and confirm the input got smaller.
3. **Types on both sides of `+`.** `list + list`, never `list + int`.
4. **Exercise every branch.** A test suite that never subtracts will never find a broken `-`.
5. **`self.` for sibling methods**, or use an inner closure and avoid the question.
6. **Formula instead of simulation? Brute-force it.** Ten lines, small inputs, compare.
7. **`compile()`, not `ast.parse()`**, when you want to know if a file is really valid.

---

Run the harness any time:

```bash
python3 guide/verify.py     # 50/50 expected
```
