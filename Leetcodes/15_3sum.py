"""
Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? 
Find all unique triplets in the array which gives the sum of zero.

Note: The solution set must not contain duplicate triplets.

Example:
Given array nums = [-1, 0, 1, 2, -1, -4],
A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]
"""

class Solution(object):
    def sum_calculate(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        length = len(nums)
        result = []
        # sort() to cut duplicate
        nums.sort()
        for i in range(length):
            for j in range(i + 1, length):
                for k in range(j + 1, length):
                    if nums[i] + nums[j] + nums[k] == 0:
                        tmp_res = [nums[i], nums[j], nums[k]]
                        if tmp_res not in result:
                            result.append(tmp_res)
        return result

if __name__ == '__main__':
    sumCalculate = Solution()
    array = list(map(int, input("Input: ").split(',')))
    print("Output: ", sumCalculate.sum_calculate(array))