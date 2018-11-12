"""
给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
"""

# Solutin A:

class Solution(object):
    def twoSum_A(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    print([i, j])

# Solution B: (better)

# class Solution(object):
    def twoSum_B(self, nums, target):
        look_up = {}
        for i, num in enumerate(nums):
            if target - num in look_up:
                print([look_up[target - num], i])
            look_up[num] = i

if __name__ == '__main__':
    elements = input('Enter the elem: ').split(',')
    elements = list(map(int, elements))
    tar = int(input('Target num: '))
    prog = Solution()
    prog.twoSum_A(elements, tar)
    prog.twoSum_B(elements, tar)
