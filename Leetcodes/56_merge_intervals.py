class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        # if len(intervals) == 1:
            # return intervals
        # while (len(intervals) > 1):
        '''    
        l = len(intervals)
        for i in range(len(intervals)):
            if i == len(intervals)-1:
                return intervals
            raw = intervals[i]
            for j in range(i+1, len(intervals)):
                if self.isOverlap(intervals[i], intervals[j]):
                    t = sorted(intervals[i] + intervals[j])
                    intervals.remove(intervals[j])
                    intervals.remove(intervals[i])
                    intervals.insert(0, [t[0], t[-1]])
                    break
                else:
                    j += 1
            # Incase [[1,4],[1,4]] will cause index out of range
            if raw == intervals[i] and l == len(intervals):
                continue
            else:
                break
        # print(intervals)
        '''
        result = []
        for pair in sorted(intervals, key=lambda k:k[0]):
            if result and result[-1][-1] >= pair[0]:
                result[-1][-1] = max(result[-1][-1], pair[1])
            else:
                result.append(pair)
        return result
            
    def isOverlap(self, i, j):
        if min(i) > max(j) or min(j) > max(i):
            return False
        else:
            return True

s = Solution()
print(s.merge([[1,3],[2,6],[8,10],[15,18]]))
print(s.merge([[1,4], [4,6]]))
print(s.merge([[0,1]]))
print(s.merge([[1,4],[1,4]]))
print(s.merge([[1,4],[2,3]]))
print(s.merge([]))