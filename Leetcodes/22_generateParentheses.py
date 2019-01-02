'''
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
For example, given n = 3, a solution set is:

[
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
]
'''

class Solution(object):
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        self.res = list()
        self.singleStr('', 0, 0, n)
        return self.res

    def singleStr(self, s, left, right, n):
        if left == n and right == n:
            self.res.append(s)
        if left < n:
            self.singleStr(s + '(', left + 1, right, n)
        if left > right:
            self.singleStr(s + ')', left, right + 1, n)

if __name__ == '__main__':
    generateParent = Solution()
    num = int(input('Number: '))
    print(generateParent.generateParenthesis(num))
