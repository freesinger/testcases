"""
There are two sorted arrays nums1 and nums2 of size m and n respectively.
Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
You may assume nums1 and nums2 cannot be both empty.

Example 1:
nums1 = [1, 3]
nums2 = [2]
The median is 2.0

Example 2:
nums1 = [1, 2]
nums2 = [3, 4]
The median is (2 + 3)/2 = 2.5
"""

class Solution(object):
    def findMedianOfArrays(self, str1, str2):
        str1 = str1.split(',')
        # str1 = [n for n in str1.split(',')]
        str2 = [i for i in str2.split(',')]
        # str1,append(str2) 
        # [1,2,3] <----> [1,2,[3]]
        str1.extend(str2)
        # str1 = [int(i) for i in str1]
        str1 = list(map(int, str1))
        temp, num = sorted(str1), len(str1)
        return (float)((temp[0] + temp[num - 1]) / 2)

if __name__ == '__main__':
    # str_in_1 = input('Input 1st array: ').split(',')
    str_in_1 = input('Input 1st array: ')
    str_in_2 = input('Input 2nd Array: ')
    find = Solution()
    print(find.findMedianOfArrays(str_in_1, str_in_2))