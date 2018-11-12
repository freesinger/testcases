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
    # 拼接之后排列，复杂度超出O(log (m+n))
    def findMedianOfArrays_A(self, str1, str2):
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

    """
    首先转成求A和B数组中第k小的数的问题, 然后用k/2在A和B中分别找。
    """
    def findMedainOfArrays_B(self, str1, str2):
        def findKth(A, B, k):
            if len(A) == 0:
                return B[k - 1]
            if len(B) == 0:
                return A[k - 1]
            if k == 1:
                return min(A[0], B[0])
            # 应该使用floor division
            a = A[k // 2 - 1] if len(A) >= k // 2 else None
            b = B[k // 2 - 1] if len(B) >= k // 2 else None

            if b is None or (a is not None and a < b):
                return findKth(A[k // 2:], B, k - k // 2)
            return findKth(A, B[k // 2:], k - k // 2)
        
        str1 = str1.split(',')
        str2 = str2.split(',')
        str1 = list(map(int, str1))
        str2 = list(map(int, str2))
        n = len(str1) + len(str2)
        
        if n % 2 == 1:
            return findKth(str1, str2, n // 2 + 1)
        else:
            smaller = findKth(str1, str2, n // 2)
            bigger = findKth(str1, str2, n // 2 + 1)
            return (smaller + bigger) / 2.0

if __name__ == '__main__':
    # str_in_1 = input('Input 1st array: ').split(',')
    str_in_1 = input('Input 1st array: ')
    str_in_2 = input('Input 2nd Array: ')
    find = Solution()
    print(find.findMedianOfArrays_A(str_in_1, str_in_2))
    # print(find.findMedainOfArrays_B(str_in_1, str_in_2))