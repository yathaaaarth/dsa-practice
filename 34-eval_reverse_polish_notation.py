# Question Link -> https://leetcode.com/problems/evaluate-reverse-polish-notation

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        st = []

        for c in tokens:
            if c == "+":
                # Addition is commutative, so pop order does not matter.
                st.append(st.pop() + st.pop())
            elif c == "-":
                # Subtraction is NOT commutative. The stack pops in reverse order, so the
                # first pop is the RIGHT operand and the second pop is the LEFT operand.
                second, first = st.pop(), st.pop()
                # FIX: was `st.append(first, second)` -> TypeError, list.append takes one
                # argument. The intent was to push the difference.
                st.append(first - second)
            elif c == "*":
                # Multiplication is commutative, so pop order does not matter.
                st.append(st.pop() * st.pop())
            elif c == "/":
                second, first = st.pop(), st.pop()
                # int(first / second) truncates TOWARD ZERO, which is what LeetCode asks for.
                # Do NOT use `first // second`: floor division rounds toward -infinity,
                # so -7 // 2 == -4 but int(-7 / 2) == -3.
                st.append(int(first / second))
            else:
                st.append(int(c))

        return st[0]
