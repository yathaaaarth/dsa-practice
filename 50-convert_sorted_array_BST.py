# Question Link -> https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/

class Solution(object):
    def sortedArrayToBST(self, nums):
        def recursive(start, end):
            # FIX: there was no base case at all, so the recursion never terminated.
            # start > end means the slice is empty -> that child is None.
            if start > end:
                return None

            # Picking the MIDDLE element as the root is what keeps the tree height-balanced:
            # equal counts go left and right.
            mid = (start + end) // 2
            node = TreeNode(nums[mid])

            # FIX: these used to be called as `recursive(nums, 0, mid-1)` -- three arguments
            # to a two-parameter function (TypeError), and the `0` restarted the left bound
            # every time instead of narrowing it. `nums` is already visible via closure.
            node.left = recursive(start, mid - 1)
            node.right = recursive(mid + 1, end)
            return node

        return recursive(0, len(nums) - 1)
