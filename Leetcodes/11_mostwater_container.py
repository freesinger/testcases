"""
Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). 
n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). 
Find two lines, which together with x-axis forms a container, such that the container contains the most water.

Note: You may not slant the container and n is at least 2.

The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. 
In this case, the max area of water (blue section) the container can contain is 49.

Example:
Input: [1,8,6,2,5,4,8,3,7]
Output: 49
"""

class Solution(object):
    def most_water_Container(self, height):
        """
        height: list[int]
        left, right: int
        """
        left, right, max_water = 0, len(height) - 1, 0
        while left < right:
            cur_water = (right - left) * min(height[left], height[right])
            max_water = max(cur_water, max_water)
            if height[left] < height[right]:
                left += 1
            elif height[left] > height[right]:
                right -= 1
            else:
                left += 1
                right -= 1
        return max_water

def main():
    # barrel = [int(i) for i in input("Input: ").split(',')]
    barrel = list(map(int, input("Input: ").split(',')))
    maxArea = Solution()
    print("Output: ", maxArea.most_water_Container(barrel))

if __name__ == '__main__':
    main()