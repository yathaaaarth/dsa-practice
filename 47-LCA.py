# Question Link -> https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        # Base case: an empty subtree contributes nothing; finding p or q means "this
        # subtree contains one of them, and this node is the highest such point".
        if not root or root == p or root == q:
            return root

        # FIX: these two calls used to be bare `lowestCommonAncestor(...)`, which raises
        # NameError -- inside a class body the method is not a module-level function.
        # It must be reached through the instance: `self.`.
        l = self.lowestCommonAncestor(root.left, p, q)
        r = self.lowestCommonAncestor(root.right, p, q)

        # p and q were found on opposite sides, so this node is the split point = the LCA.
        if l and r:
            return root
        # Otherwise pass up whichever side found something (or None if neither did).
        return l or r
