"""
Example 1:

Given input matrix = 
[
  [1,2,3],
  [4,5,6],
  [7,8,9]
],

rotate the input matrix in-place such that it becomes:
[
  [7,4,1],
  [8,5,2],
  [9,6,3]
]
"""

'''
Using another 2D to sort results
'''
class Solution_A(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        results = list()
        if matrix:
            row_len = len(matrix)
            num_elems = len(matrix[0])
            for column in range(num_elems):
                temp = list()
                for row in range(row_len):
                    temp.append(matrix[row_len - row - 1][column])
                results.append(temp)
        else: results = None
        return results


'''
You have to rotate the image in-place, which means you have to modify the input 2D matrix directly.
DO NOT allocate another 2D matrix and do the rotation.
'''
class Solution_A(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        matrix[:] = map(list, zip(*matrix[::-1]))
