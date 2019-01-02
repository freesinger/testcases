'''
Given a collection of distinct integers, return all possible permutations.

Example:
Input: [1,2,3]
Output:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]
'''

class Solution(object):
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if len(nums) == 0:
            return None
        if len(nums) == 1:
            return [nums]
        res = []
        for i in range(len(nums)):
            cur = nums[i]
            # nums.remove(cur)
            rest = nums[:i] + nums[i+1:]
            for j in self.permute(rest):
                res.append([cur] + j)
        return res

if __name__ == '__main__':
    permu = Solution()
    num = input('Input integers: ')
    numbers = list(int(i) for i in num.split(','))
    print(permu.permute(numbers))