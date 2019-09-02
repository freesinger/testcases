class Solution(object):
    def uniquePaths(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """
        self.cnt = 0
        self.recursive(1, 1, m, n)
        return self.cnt

    def recursive(self, x, y, m, n):
        if (x == m) & (y == n):
            self.cnt += 1
        elif (x < m) & (y < n):
            self.recursive(x+1, y, m, n)
            self.recursive(x, y+1, m, n)
        elif x == m:
            self.recursive(x, y+1, m, n)
        elif y == n:
            self.recursive(x+1, y, m, n)


a = Solution()
print(a.uniquePaths(7,4))