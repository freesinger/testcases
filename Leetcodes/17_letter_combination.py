"""
Given a string containing digits from 2-9 inclusive
Return all possible letter combinations that the number could represent

https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Example:
Input: "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
"""

class Solution(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtyrp: List[str]
        """
        # map key: value
        lookup = {
            '2': ['a', 'b', 'c'],
            '3': ['d', 'e', 'f'],
            '4': ['g', 'h', 'i'],
            '5': ['j', 'k', 'l'],
            '6': ['m', 'n', 'o'],
            '7': ['p', 'q', 'r', 's'],
            '8': ['t', 'u', 'v'],
            '9': ['w', 'x', 'y', 'z']
        }
        res = []
        # recursive find all number 
        def recurseFind(string, digits):
            if len(digits) == 0:
                res.append(string)
            else:
                cur_digit = digits[0]
                """
                if cur_digit not in lookup:
                    return res
                """
                for elem in lookup[cur_digit]:
                    recurseFind(string + elem, digits[1:])

        if not digits or len(digits) == 0:
            return res
        recurseFind('', digits)
        return res
        
def main():
    digits = input("Input: ")
    letterComb = Solution()
    print("Output: ", letterComb.letterCombinations(digits))

if __name__ == '__main__':
    main()