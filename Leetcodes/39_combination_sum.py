'''
Given a set of candidate numbers (candidates) (without duplicates) and a target number (target), 
find all unique combinations in candidates where the candidate numbers sums to target.
The same repeated number may be chosen from candidates unlimited number of times.

Note:
All numbers (including target) will be positive integers.
The solution set must not contain duplicate combinations.

Example 1:
Input: candidates = [2,3,6,7], target = 7,
A solution set is:
[
  [7],
  [2,2,3]
]

Example 2:
Input: candidates = [2,3,5], target = 8,
A solution set is:
[
  [2,2,2,2],
  [2,3,3],
  [3,5]
]
'''

class Solution(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        result = list()
        def recursive(number, tmpres, index):
            if number == 0:
                result.append(tmpres)
                return
            if number < 0:
                return
            if index >= len(candidates):
                return
            # skip current number
            recursive(number, tmpres, index+1)
            # stick to  current number
            recursive(number-candidates[index], tmpres+[candidates[index]], index)
        recursive(target, list(), 0)
        return result
    
if __name__ == '__main__':
    combsum = Solution()
    candidates = list(int(x) for x in input("Enter candidates: ").strip().split(','))
    sumnumber = int(input("Number: "))
    print(combsum.combinationSum(candidates, sumnumber))