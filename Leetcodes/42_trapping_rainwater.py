"""
Given n non-negative integers representing an elevation map where the width of each bar is 1, 
compute how much water it is able to trap after raining.
https://leetcode.com/problems/trapping-rain-water/

Example:
Input: [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
"""

class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        l, r, water, min_height = 0, len(height) - 1, 0, 0
        while l < r:
            min_height = min(height[l], height[r])
            while l < r and height[l] <= min_height:
                water += min_height - height[l] 
                l += 1
            while l < r and height[r] <= min_height:
                water += min_height - height[r]
                r -= 1
        return water