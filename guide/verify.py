#!/usr/bin/env python3
"""
Run every solution in this repository against the LeetCode sample cases plus edge cases.

Why this file exists
--------------------
The solutions are written to be pasted into LeetCode, which silently pre-imports
`List`, `Optional`, `deque`, `TreeNode` and `ListNode`. That means they cannot be run
locally as-is -- and six of them were, in fact, broken (see guide/bugs-found.md).
This harness injects those names, executes each file, and asserts real answers, so a
regression cannot hide behind "well, it looked right".

Usage:  python3 guide/verify.py
Exit code 0 means every solution passed.
"""

import io
import contextlib
import os
import sys
from collections import deque
from typing import List, Optional

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --------------------------------------------------------------------------------------
# The stubs LeetCode gives you for free
# --------------------------------------------------------------------------------------
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def load(filename):
    """Execute a solution file with LeetCode's implicit names in scope; return its namespace."""
    path = os.path.join(REPO, filename)
    with open(path) as fh:
        source = fh.read()
    ns = {
        "List": List, "Optional": Optional, "deque": deque,
        "ListNode": ListNode, "TreeNode": TreeNode,
        "__name__": "solution", "__file__": path,
    }
    # 35-stack_sorting.py prints at module level; swallow it so the report stays readable.
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(source, path, "exec"), ns)
    return ns


def sol(filename):
    """Return an instance of the `Solution` class defined in a file."""
    return load(filename)["Solution"]()


# --------------------------------------------------------------------------------------
# Linked-list and tree helpers
# --------------------------------------------------------------------------------------
def build_list(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def read_list(head, limit=1000):
    out = []
    while head and limit:
        out.append(head.val)
        head = head.next
        limit -= 1
    return out


def build_tree(values):
    """LeetCode level-order array, `None` for a missing child."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                q.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                q.append(node.right)
            i += 1
    return root


def find_node(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


def read_tree(root):
    """Level-order with trailing Nones trimmed -- comparable to LeetCode's output format."""
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


# --------------------------------------------------------------------------------------
# Test registry
# --------------------------------------------------------------------------------------
TESTS = []


def check(filename, title):
    def wrap(fn):
        TESTS.append((filename, title, fn))
        return fn
    return wrap


def eq(actual, expected, label=""):
    if actual != expected:
        raise AssertionError(f"{label}expected {expected!r}, got {actual!r}")


# ------------------------------- Day 1: hashing & bits --------------------------------
@check("01-Duplicate_value.py", "Contains Duplicate")
def _():
    f = sol("01-Duplicate_value.py").containsDuplicate
    eq(f([1, 2, 3, 1]), True)
    eq(f([1, 2, 3, 4]), False)
    eq(f([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]), True)
    eq(f([]), False, "empty: ")
    eq(f([7]), False, "single: ")


@check("02-Missing_number.py", "Missing Number")
def _():
    f = sol("02-Missing_number.py").missingNumber
    eq(f([3, 0, 1]), 2)
    eq(f([0, 1]), 2, "missing is n: ")
    eq(f([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8)
    eq(f([1]), 0, "missing is 0: ")


@check("03-Number_Disappered.py", "Find All Numbers Disappeared in an Array")
def _():
    f = sol("03-Number_Disappered.py").findDisappearedNumbers
    eq(f([4, 3, 2, 7, 8, 2, 3, 1]), [5, 6])
    eq(f([1, 1]), [2])
    eq(f([1]), [], "nothing missing: ")


@check("04-Two_sum.py", "Two Sum")
def _():
    f = sol("04-Two_sum.py").twoSum
    eq(f([2, 7, 11, 15], 9), [0, 1])
    eq(f([3, 2, 4], 6), [1, 2])
    eq(f([3, 3], 6), [0, 1], "duplicate values: ")


@check("05-Smaller_than_current.py", "How Many Numbers Are Smaller Than the Current Number")
def _():
    f = sol("05-Smaller_than_current.py").smallerNumbersThanCurrent
    eq(f([8, 1, 2, 2, 3]), [4, 0, 1, 1, 3])
    eq(f([6, 5, 4, 8]), [2, 1, 0, 3])
    eq(f([7, 7, 7, 7]), [0, 0, 0, 0], "all equal: ")


@check("12-Contains_duplicates2.py", "Contains Duplicate II")
def _():
    f = sol("12-Contains_duplicates2.py").containsNearbyDuplicate
    eq(f([1, 2, 3, 1], 3), True)
    eq(f([1, 0, 1, 1], 1), True)
    eq(f([1, 2, 3, 1, 2, 3], 2), False)
    eq(f([1, 2, 1], 0), False, "k=0: ")


@check("15-Single_number.py", "Single Number")
def _():
    f = sol("15-Single_number.py").singleNumber
    eq(f([2, 2, 1]), 1)
    eq(f([4, 1, 2, 1, 2]), 4)
    eq(f([1]), 1, "single element: ")


@check("19-Counting_bits.py", "Counting Bits")
def _():
    f = sol("19-Counting_bits.py").countBits
    eq(f(2), [0, 1, 1])
    eq(f(5), [0, 1, 1, 2, 1, 2])
    eq(f(0), [0], "n=0: ")
    eq(f(16)[16], 1, "power of two: ")


# --------------------- Day 2: two pointers, sliding window, prefix ---------------------
@check("10-Square-sorted_array.py", "Squares of a Sorted Array")
def _():
    f = sol("10-Square-sorted_array.py").sortedSquares
    eq(f([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100])
    eq(f([-7, -3, 2, 3, 11]), [4, 9, 9, 49, 121])
    eq(f([-5]), [25], "single negative: ")


@check("13-Minimum_Absolute_diff.py", "Minimum Absolute Difference")
def _():
    f = sol("13-Minimum_Absolute_diff.py").minimumAbsDifference
    eq(f([4, 2, 1, 3]), [[1, 2], [2, 3], [3, 4]])
    eq(f([1, 3, 6, 10, 15]), [[1, 3]])
    eq(f([3, 8, -10, 23, 19, -4, -14, 27]), [[-14, -10], [19, 23], [23, 27]])


@check("09-Best_time_sell_stock.py", "Best Time to Buy and Sell Stock")
def _():
    f = sol("09-Best_time_sell_stock.py").maxProfit
    eq(f([7, 1, 5, 3, 6, 4]), 5)
    eq(f([7, 6, 4, 3, 1]), 0, "monotonically falling: ")
    eq(f([1]), 0, "single day: ")
    eq(f([2, 4, 1]), 2)


@check("14-Minimum_size_subarray_sum.py", "Minimum Size Subarray Sum")
def _():
    f = sol("14-Minimum_size_subarray_sum.py").minSubArrayLen
    eq(f(7, [2, 3, 1, 2, 4, 3]), 2)
    eq(f(4, [1, 4, 4]), 1)
    eq(f(11, [1, 1, 1, 1, 1, 1, 1, 1]), 0, "unreachable target: ")


@check("11-Longest_mountain_Array.py", "Longest Mountain in Array")
def _():
    f = sol("11-Longest_mountain_Array.py").longestMountain
    eq(f([2, 1, 4, 7, 3, 2, 5]), 5)
    eq(f([2, 2, 2]), 0, "no peak: ")
    eq(f([0, 1, 0]), 3)
    eq(f([1, 2, 3]), 0, "no descent: ")


@check("06-Minimum_time_visit.py", "Minimum Time Visiting All Points")
def _():
    f = sol("06-Minimum_time_visit.py").minTimeToVisitAllPoints
    eq(f([[1, 1], [3, 4], [-1, 0]]), 7)
    eq(f([[3, 2], [-2, 2]]), 5)
    eq(f([[0, 0]]), 0, "single point: ")


@check("18-maximum_subarray.py", "Maximum Subarray")
def _():
    f = sol("18-maximum_subarray.py").maxSubArray
    eq(f([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
    eq(f([1]), 1)
    eq(f([5, 4, -1, 7, 8]), 23)
    eq(f([-3, -1, -2]), -1, "all negative: ")


@check("20-Range_sum_query.py", "Range Sum Query - Immutable")
def _():
    NumArray = load("20-Range_sum_query.py")["NumArray"]
    a = NumArray([-2, 0, 3, -5, 2, -1])
    eq(a.sumRange(0, 2), 1)
    eq(a.sumRange(2, 5), -1)
    eq(a.sumRange(0, 5), -3)
    eq(a.sumRange(3, 3), -5, "single index: ")


@check("07-Spiral_matrix.py", "Spiral Matrix")
def _():
    f = sol("07-Spiral_matrix.py").spiralOrder
    eq(f([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [1, 2, 3, 6, 9, 8, 7, 4, 5])
    eq(f([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])
    eq(f([[7]]), [7], "1x1: ")
    eq(f([[1], [2], [3]]), [1, 2, 3], "single column: ")


# ----------------------------- Day 4: stacks and queues -------------------------------
@check("33-Valid_Parenthese.py", "Valid Parentheses")
def _():
    f = sol("33-Valid_Parenthese.py").isValid
    eq(f("()"), True)
    eq(f("()[]{}"), True)
    eq(f("(]"), False)
    eq(f("([)]"), False, "interleaved: ")
    eq(f("{[]}"), True)
    eq(f("("), False, "unclosed: ")


@check("32-minstack.py", "Min Stack")
def _():
    MinStack = load("32-minstack.py")["MinStack"]
    s = MinStack()
    s.push(-2); s.push(0); s.push(-3)
    eq(s.getMin(), -3)
    s.pop()
    eq(s.top(), 0)
    eq(s.getMin(), -2)


@check("34-eval_reverse_polish_notation.py", "Evaluate Reverse Polish Notation")
def _():
    f = sol("34-eval_reverse_polish_notation.py").evalRPN
    eq(f(["2", "1", "+", "3", "*"]), 9)
    eq(f(["4", "13", "5", "/", "+"]), 6)
    eq(f(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]), 22)
    eq(f(["5", "2", "-"]), 3, "subtraction order: ")
    eq(f(["-7", "2", "/"]), -3, "truncation toward zero: ")


@check("35-stack_sorting.py", "Sort a Stack")
def _():
    f = load("35-stack_sorting.py")["sort_stack"]
    eq(f([34, 3, 31, 98, 92, 23]), [3, 23, 31, 34, 92, 98])
    eq(f([]), [], "empty: ")
    eq(f([1]), [1], "single: ")
    eq(f([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5], "reverse sorted: ")


@check("36-implement_stack_queues.py", "Implement Stack using Queues")
def _():
    MyStack = load("36-implement_stack_queues.py")["MyStack"]
    s = MyStack()
    s.push(1); s.push(2)
    eq(s.top(), 2)
    eq(s.pop(), 2)
    eq(s.empty(), False)
    eq(s.pop(), 1)
    eq(s.empty(), True)


@check("37-time_need_buy_ticket.py", "Time Needed to Buy Tickets")
def _():
    f = sol("37-time_need_buy_ticket.py").timeRequiredToBuy

    def brute(tickets, k):
        t, time, i = list(tickets), 0, 0
        while True:
            if t[i] > 0:
                t[i] -= 1
                time += 1
                if i == k and t[i] == 0:
                    return time
            i = (i + 1) % len(t)

    eq(f([2, 3, 2], 2), 6)
    eq(f([5, 1, 1, 1], 0), 8)
    eq(f([2, 2], 0), 3, "equal tickets after k -- the old off-by-one: ")

    # Exhaustive differential test: every queue of length <= 4 with values <= 4.
    import itertools
    for n in range(1, 5):
        for combo in itertools.product(range(1, 5), repeat=n):
            for k in range(n):
                a, b = f(list(combo), k), brute(combo, k)
                if a != b:
                    raise AssertionError(f"tickets={list(combo)} k={k}: got {a}, brute force says {b}")


@check("38-Reverse_first_k_ele_queue.py", "Reverse First K Elements of Queue")
def _():
    f = sol("38-Reverse_first_k_ele_queue.py").modifyQueue
    eq(list(f(deque([1, 2, 3, 4, 5]), 3)), [3, 2, 1, 4, 5])
    eq(list(f(deque([4, 3, 2, 1]), 4)), [1, 2, 3, 4], "k == len: ")
    eq(list(f(deque([1, 2, 3]), 1)), [1, 2, 3], "k=1 is a no-op: ")


# -------------------------------- Day 5: linked lists ---------------------------------
@check("25-Middle_ll.py", "Middle of the Linked List")
def _():
    f = sol("25-Middle_ll.py").middleNode
    eq(read_list(f(build_list([1, 2, 3, 4, 5]))), [3, 4, 5], "odd length: ")
    eq(read_list(f(build_list([1, 2, 3, 4, 5, 6]))), [4, 5, 6], "even -> second middle: ")
    eq(read_list(f(build_list([1]))), [1], "single: ")


@check("26-Cycle_ll.py", "Linked List Cycle")
def _():
    f = sol("26-Cycle_ll.py").hasCycle
    eq(f(build_list([1, 2, 3, 4])), False, "no cycle: ")
    eq(f(None), False, "empty: ")
    head = build_list([3, 2, 0, -4])
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = head.next          # cycle back to index 1
    eq(f(head), True, "cycle present: ")


@check("27-Reversed_ll.py", "Reverse Linked List")
def _():
    f = sol("27-Reversed_ll.py").reverseList
    eq(read_list(f(build_list([1, 2, 3, 4, 5]))), [5, 4, 3, 2, 1])
    eq(read_list(f(build_list([1, 2]))), [2, 1])
    eq(read_list(f(None)), [], "empty: ")


@check("29-Reversed_ll.py", "Reverse Linked List II")
def _():
    f = sol("29-Reversed_ll.py").reverseBetween
    eq(read_list(f(build_list([1, 2, 3, 4, 5]), 2, 4)), [1, 4, 3, 2, 5])
    eq(read_list(f(build_list([5]), 1, 1)), [5], "single node: ")
    eq(read_list(f(build_list([1, 2, 3]), 1, 3)), [3, 2, 1], "whole list: ")
    eq(read_list(f(build_list([1, 2, 3, 4]), 1, 2)), [2, 1, 3, 4], "left == 1: ")


@check("28-Remove_ll_element.py", "Remove Linked List Elements")
def _():
    f = sol("28-Remove_ll_element.py").removeElements
    eq(read_list(f(build_list([1, 2, 6, 3, 4, 5, 6]), 6)), [1, 2, 3, 4, 5])
    eq(read_list(f(build_list([]), 1)), [], "empty: ")
    eq(read_list(f(build_list([7, 7, 7, 7]), 7)), [], "all removed: ")
    eq(read_list(f(build_list([1, 1, 2]), 1)), [2], "leading run: ")


@check("30-Palindrome.py", "Palindrome Linked List")
def _():
    f = sol("30-Palindrome.py").isPalindrome
    eq(f(build_list([1, 2, 2, 1])), True)
    eq(f(build_list([1, 2])), False)
    eq(f(build_list([1])), True, "single: ")
    eq(f(build_list([1, 2, 1])), True, "odd palindrome: ")
    eq(f(build_list([1, 0, 1])), True)


@check("31-Merg_sorted_ll.py", "Merge Two Sorted Lists")
def _():
    f = sol("31-Merg_sorted_ll.py").mergeTwoLists
    eq(read_list(f(build_list([1, 2, 4]), build_list([1, 3, 4]))), [1, 1, 2, 3, 4, 4])
    eq(read_list(f(None, None)), [], "both empty: ")
    eq(read_list(f(None, build_list([0]))), [0], "one empty: ")


# --------------------------------- Day 6: binary trees --------------------------------
@check("41-Max_depth_bt.py", "Maximum Depth of Binary Tree")
def _():
    f = sol("41-Max_depth_bt.py").maxDepth
    eq(f(build_tree([3, 9, 20, None, None, 15, 7])), 3)
    eq(f(build_tree([1, None, 2])), 2)
    eq(f(None), 0, "empty: ")


@check("40_mini_depth_bt.py", "Minimum Depth of Binary Tree")
def _():
    f = sol("40_mini_depth_bt.py").minDepth
    eq(f(build_tree([3, 9, 20, None, None, 15, 7])), 2)
    eq(f(build_tree([2, None, 3, None, 4, None, 5, None, 6])), 5, "right-skewed: ")
    eq(f(None), 0, "empty: ")
    eq(f(build_tree([1])), 1, "single node: ")


@check("43-Same_tree.py", "Same Tree")
def _():
    f = sol("43-Same_tree.py").isSameTree
    eq(f(build_tree([1, 2, 3]), build_tree([1, 2, 3])), True)
    eq(f(build_tree([1, 2]), build_tree([1, None, 2])), False, "same values, different shape: ")
    eq(f(build_tree([1, 2, 1]), build_tree([1, 1, 2])), False)
    eq(f(None, None), True, "both empty: ")


@check("46-Invert_bt.py", "Invert Binary Tree")
def _():
    f = sol("46-Invert_bt.py").invertTree
    eq(read_tree(f(build_tree([4, 2, 7, 1, 3, 6, 9]))), [4, 7, 2, 9, 6, 3, 1])
    eq(read_tree(f(build_tree([2, 1, 3]))), [2, 3, 1])
    eq(read_tree(f(None)), [], "empty: ")


@check("44-Path_sum.py", "Path Sum")
def _():
    f = sol("44-Path_sum.py").hasPathSum
    eq(f(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]), 22), True)
    eq(f(build_tree([1, 2, 3]), 5), False)
    eq(f(None, 0), False, "empty tree, target 0: ")
    eq(f(build_tree([1, 2]), 1), False, "must reach a LEAF: ")


@check("45-Diameter_bt.py", "Diameter of Binary Tree")
def _():
    f = sol("45-Diameter_bt.py").diameterOfBinaryTree
    eq(f(build_tree([1, 2, 3, 4, 5])), 3)
    eq(f(build_tree([1, 2])), 1)
    eq(f(build_tree([1])), 0, "single node: ")


@check("39-avg_level_bt.py", "Average of Levels in Binary Tree")
def _():
    f = sol("39-avg_level_bt.py").averageOfLevels
    eq(f(build_tree([3, 9, 20, None, None, 15, 7])), [3.0, 14.5, 11.0])
    eq(f(build_tree([3, 9, 20, 15, 7])), [3.0, 14.5, 11.0])
    eq(f(build_tree([1])), [1.0], "single node: ")


@check("42-Level_order_traversal_bt.py", "Binary Tree Level Order Traversal")
def _():
    f = sol("42-Level_order_traversal_bt.py").levelOrder
    eq(f(build_tree([3, 9, 20, None, None, 15, 7])), [[3], [9, 20], [15, 7]])
    eq(f(build_tree([1])), [[1]])
    eq(f(None), [], "empty: ")


@check("47-LCA.py", "Lowest Common Ancestor of a Binary Tree")
def _():
    f = sol("47-LCA.py").lowestCommonAncestor
    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    eq(f(root, find_node(root, 5), find_node(root, 1)).val, 3)
    eq(f(root, find_node(root, 5), find_node(root, 4)).val, 5, "one is an ancestor of the other: ")
    eq(f(root, find_node(root, 7), find_node(root, 4)).val, 2)


# ---------------------------- Day 7: BST, graphs, recursion ---------------------------
@check("48-Search_bt.py", "Search in a Binary Search Tree")
def _():
    f = sol("48-Search_bt.py").searchBST
    root = build_tree([4, 2, 7, 1, 3])
    eq(read_tree(f(root, 2)), [2, 1, 3])
    eq(f(root, 5), None, "absent value: ")


@check("49-Insert_into_BST.py", "Insert into a Binary Search Tree")
def _():
    f = sol("49-Insert_into_BST.py").insertIntoBST
    eq(read_tree(f(build_tree([4, 2, 7, 1, 3]), 5)), [4, 2, 7, 1, 3, 5])
    eq(read_tree(f(None, 5)), [5], "insert into empty: ")


@check("50-convert_sorted_array_BST.py", "Convert Sorted Array to BST")
def _():
    f = sol("50-convert_sorted_array_BST.py").sortedArrayToBST

    def is_bst_with(node, values, lo=float("-inf"), hi=float("inf")):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return is_bst_with(node.left, values, lo, node.val) and \
               is_bst_with(node.right, values, node.val, hi)

    def height(node):
        return 0 if not node else 1 + max(height(node.left), height(node.right))

    def inorder(node, out):
        if node:
            inorder(node.left, out)
            out.append(node.val)
            inorder(node.right, out)
        return out

    for values in ([-10, -3, 0, 5, 9], [1, 3], [0], list(range(20))):
        tree = f(values)
        eq(inorder(tree, []), values, f"inorder for {values}: ")
        if not is_bst_with(tree, values):
            raise AssertionError(f"not a valid BST for {values}")
        n = len(values)
        expected_height = n.bit_length()          # a balanced tree of n nodes
        if height(tree) > expected_height:
            raise AssertionError(f"unbalanced for {values}: height {height(tree)} > {expected_height}")
    eq(f([]), None, "empty array: ")


@check("08-Number_of_Island.py", "Number of Islands")
def _():
    f = sol("08-Number_of_Island.py").numIslands
    eq(f([list("11110"), list("11010"), list("11000"), list("00000")]), 1)
    eq(f([list("11000"), list("11000"), list("00100"), list("00011")]), 3)
    eq(f([list("000"), list("000")]), 0, "all water: ")
    eq(f([list("1")]), 1, "single cell: ")


@check("21-letterCase.py", "Letter Case Permutation")
def _():
    f = sol("21-letterCase.py").letterCasePermutation
    eq(sorted(f("a1b2")), sorted(["a1b2", "a1B2", "A1b2", "A1B2"]))
    eq(sorted(f("3z4")), sorted(["3z4", "3Z4"]))
    eq(f("12345"), ["12345"], "no letters: ")


@check("22-Subsets.py", "Subsets")
def _():
    f = sol("22-Subsets.py").subsets
    eq(sorted(f([1, 2, 3])), sorted([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]))
    eq(f([0]), [[], [0]])
    eq(len(f([1, 2, 3, 4, 5])), 32, "2^n subsets: ")


@check("23-Combinations.py", "Combinations")
def _():
    f = sol("23-Combinations.py").combine
    eq(sorted(f(4, 2)), sorted([[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]))
    eq(f(1, 1), [[1]])
    eq(len(f(5, 3)), 10, "C(5,3): ")


@check("24-permutation.py", "Permutations")
def _():
    f = sol("24-permutation.py").permute
    eq(sorted(f([1, 2, 3])),
       sorted([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]))
    eq(f([1]), [[1]])
    eq(sorted(f([0, 1])), sorted([[0, 1], [1, 0]]))
    eq(len(f([1, 2, 3, 4])), 24, "4! permutations: ")


@check("16-Coin_change.py", "Coin Change")
def _():
    f = sol("16-Coin_change.py").coinChange
    eq(f([1, 2, 5], 11), 3)
    eq(f([2], 3), -1, "impossible: ")
    eq(f([1], 0), 0, "amount 0: ")
    eq(f([186, 419, 83, 408], 6249), 20)


@check("17-climbing_stairs.py", "Climbing Stairs")
def _():
    f = sol("17-climbing_stairs.py").climbStairs
    eq(f(2), 2)
    eq(f(3), 3)
    eq(f(1), 1, "n=1 edge case: ")
    eq(f(10), 89)
    eq(f(45), 1836311903, "upper constraint: ")


# --------------------------------------------------------------------------------------
def main():
    covered = {t[0] for t in TESTS}
    all_py = {f for f in os.listdir(REPO) if f.endswith(".py")}
    missing = all_py - covered

    passed, failed = 0, []
    for filename, title, fn in TESTS:
        try:
            fn()
            passed += 1
            print(f"  PASS  {filename:<40} {title}")
        except Exception as exc:
            failed.append((filename, title, exc))
            print(f"  FAIL  {filename:<40} {title}")
            print(f"        {type(exc).__name__}: {exc}")

    print()
    print(f"{passed}/{len(TESTS)} solutions passed.")
    if missing:
        print(f"WARNING: {len(missing)} .py files have no test: {sorted(missing)}")
    if failed:
        print(f"{len(failed)} FAILED")
        return 1
    if missing:
        return 1
    print("All solution files are covered and correct.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
