"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.

Example 1:
Input: "()"
Output: true

Example 2:
Input: "()[]{}"
Output: true

Example 3:
Input: "(]"
Output: false

Example 4:
Input: "([)]"
Output: false

Example 5:
Input: "{[]}"
Output: true
"""

class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        pair = {'(' : ')', '[' : ']', '{' : '}'}
        # stack store only target elements
        stack = []
        for i in s:
            if i in pair.keys() or i in pair.values():
                stack.append(i)
            else:
                continue
        if len(stack) % 2 != 0:
            return False
        index = 0
        while (len(stack)):
            if index >= len(stack) - 1:
                return False
            if stack[index] not in pair.keys():
                return False
            elif stack[index + 1] in pair.keys():
                index += 1
            elif stack[index + 1] == pair[stack[index]]:
                # pop order
                stack.pop(index + 1)
                stack.pop(index)
                # (){}[]
                index = 0 if index - 1 < 0 else index - 1
            else:
                return False
        return stack == []

def main():
    string = input("Input:")
    s = Solution()
    print("Output:", s.isValid(string))

if __name__ == '__main__':
    main()