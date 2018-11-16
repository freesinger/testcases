"""
Given a 32-bit signed integer, reverse digits of an integer.

Example 1:
Input: 123
Output: 321

Example 2:
Input: -123
Output: -321

Example 3:
Input: 120
Output: 21

Note:
Assume we are dealing with an environment which could only store integers within the 32-bit signed
integer range: [−2**31,  2**31 − 1]. For the purpose of this problem, 
assume that your function returns 0 when the reversed integer overflows.
"""

class Solution(object):
    # Mathematic Solution
    def reverse_integer_A(self, source_int):
        if source_int < 0:
            return -self.reverse_integer(-source_int)
        res = 0
        while source_int:
            res = res * 10 + source_int % 10
            source_int //= 10
        return res if res <= 0x7fffffff else 0

    # String Solution
    def reverse_integer_B(self, source_int):
        res =  -int(str(source_int)[::-1][:-1]) if source_int < 0 else int(str(source_int)[::-1])
        return res if res <= 0x7fffffff else 0

def main():
    integer = int(input("Input a integer: "))
    reverse = Solution()
    print("Reversed integer:", reverse.reverse_integer_A(integer))
    print("Reversed integer:", reverse.reverse_integer_B(integer))

if __name__ == '__main__':
    main()