"""
Given a string s, find the longest palindromic substring in s. 
You may assume that the maximum length of s is 1000.

Example:
Input: "babad"
Output: "bab"
Note: "aba" is also a valid answer.

Example 2:
Input: "cbbd"
Output: "bb"
"""

class Solution(object):
    def longest_Palindrome(self, sentence):
        # s1,s2最长公共序列
        def longest_Common_String(s1, s2):
            m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
            longest, x_longest = 0, 0
            for x in range(1, 1 + len(s1)):
                for y in range(1, 1 + len(s2)):
                    if s1[x - 1] == s2[y - 1]:
                        m[x][y] = m[x - 1][y - 1] + 1
                        if m[x][y] > longest:
                            longest = m[x][y]
                            x_longest = x
                    else:
                        m[x][y] = 0
            return s1[x_longest - longest: x_longest]

        # 逆序sentence求最长公共序列，再判断是否存在回文
        temp = longest_Common_String(sentence, sentence[::-1])
        # print(temp)
        length = len(temp)
        if length % 2 == 1:
            for i in range((length) - 1 // 2):
                if temp[i] == temp[length - 1 - i]:
                    continue
                else:
                    temp = "There's no palindrome in this sentence."
                    break
        else:
            for i in range(length // 2):
                if temp[i] == temp[length - 1 - i]:
                    continue
                else:
                    temp = "There's no palindrome in this sentence."
                    break
        print(temp)

def main():
    string = input("Input: ")
    lpd = Solution()
    lpd.longest_Palindrome(string)

if __name__ == '__main__':
    main()