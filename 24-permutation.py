# Question Link => https://leetcode.com/problems/permutations/description/

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def backtrack(remaining, path):
            # FIX: was missing `return`, so it kept looping over an empty list (harmless
            # but pointless). Base case: nothing left to place -> `path` is a full permutation.
            if not remaining:
                result.append(path)
                return

            for i in range(len(remaining)):
                # FIX: was `remaining[:] + remaining[i+1:]`, which is a FULL copy plus a tail
                # copy -- element i was never removed, so the recursion never shrank and the
                # "permutations" contained duplicates. Correct slice drops index i:
                #   remaining[:i]  -> everything before i
                #   remaining[i+1:] -> everything after i
                # FIX: was `path + remaining[i]`, i.e. list + int -> TypeError.
                # `[remaining[i]]` wraps the int in a list so `+` concatenates two lists.
                backtrack(remaining[:i] + remaining[i + 1:], path + [remaining[i]])

        result = []
        backtrack(nums, [])
        return result
