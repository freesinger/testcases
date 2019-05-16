class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        if not nums:
            return False
        if len(nums) == 1:
            return True
        reach = 0
        for idx, max_reach in enumerate(nums):
            if idx > reach:
                return False
            reach = max(reach, idx+max_reach)
        return True