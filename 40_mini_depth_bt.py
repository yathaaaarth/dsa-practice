# Question Link -> https://leetcode.com/problems/minimum-depth-of-binary-tree/description/

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)

            # A "leaf" has NO children. If one side is empty this node is not a leaf, so we
            # must not take min(0, other) == 0 -- that would report a depth that ends at a
            # node with a child. Fall through to the non-empty side instead.
            if left == 0:
                return right + 1
            if right == 0:
                return left + 1

            return min(right, left) + 1

        # FIX: this `return` used to sit at class-body indentation, outside the method.
        # Python rejects that at compile time: SyntaxError: 'return' outside function --
        # the whole file failed to import.
        return dfs(root)
