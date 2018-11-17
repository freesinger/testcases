"""
Given an input string (s) and a pattern (p), implement regular expression matching with support for '.' and '*'.

'.' Matches any single character.
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).

Note:

s could be empty and contains only lowercase letters a-z.
p could be empty and contains only lowercase letters a-z, and characters like . or *.

Example 1:
Input:
s = "aa"
p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

Example 2:
Input:
s = "aa"
p = "a*"
Output: true
Explanation: '*' means zero or more of the precedeng element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
Input:
s = "ab"
p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".

Example 4:
Input:
s = "aab"
p = "c*a*b"
Output: true
Explanation: c can be repeated 0 times, a can be repeated 1 time. Therefore it matches "aab".

Example 5:
Input:
s = "mississippi"
p = "mis*is*p*."
Output: false
"""

class Solution(object):
    def re_matching(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        def helper(s, i, p, j):
            if j == -1:
                return i == -1
            if i == -1:
                if p[j] != '*':
                    return False
                return helper(s, i, p, j - 2)
            if p[j] == '*':
                if p[j - 1] == '.' or p[j - 1] == s[i]:
                    if helper(s, i - 1, p, j):
                        return True
                return helper(s, i, p, j - 2)
            if p[j] == '.' or p[j] == s[i]:
                return helper(s, i - 1, p, j - 1)
            return False

        return helper(s, len(s) - 1, p, len(p) - 1)

if __name__ == '__main__':
    rematch = Solution()
    string = input("Input str: ")
    pattern = input("Pattern: ")
    print("Output: ", rematch.re_matching(string, pattern))