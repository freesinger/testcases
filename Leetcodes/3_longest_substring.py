"""
Given a string, find the length of the longest substring without repeating characters.

Example 1:

Input: "abcabcbb"
Output: 3 
Explanation: The answer is "abc", with the length of 3. 
Example 2:

Input: "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3. 
             
Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
"""
import string

"""
legnth: 最长子串长度
start: 最长子串的开头
n: 字符串长
"""
class SolutionA(object):
    def lengthOfLongestSubstring(self, s):
        length, start, n = 0, 0, len(s)
        maps = {}
        for i in range(n):
            # 类似”slide window“
            start = max(start, maps.get(s[i], -1) + 1)
            length = max(length, i - start + 1)
            maps[s[i]] = i
        return length

# 滑动窗口
class SolutionB(object):
    def lengthOfLongestSubstring(self, s):
        lookup = {}
        start, end, counter, length = 0, 0, 0, 0
        while end < len(s):
            lookup[s[end]] = lookup.get(s[end], 0) + 1
            if lookup[s[end]] == 1:
                counter += 1
            end += 1
            while start < end and counter < end - start:
                lookup[s[start]] -= 1
                if lookup[s[start]] == 0:
                    counter -= 1
                start += 1
            length = max(length, end - start)
        return length

if __name__ == '__main__':
    string = input('Enter a string: ')
    # string = input()
    solution = SolutionA()
    # res = solution.lengthOfLongestSubstring(string)
    print('Output: ', solution.lengthOfLongestSubstring(string))
