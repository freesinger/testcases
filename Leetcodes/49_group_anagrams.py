from collections import defaultdict

class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        idx_dict = defaultdict(list)
        temp = [''.join(j) for j in [sorted(i) for i in strs]]
        for idx, string in enumerate(temp):
            idx_dict[string].append(idx)
        return [list(strs[i] for i in j) for j in idx_dict.values()]

if __name__ == '__main__':
    t = Solution()
    # i = input()
    # ['', '']
    print(t.groupAnagrams(["eat","tea","tan","ate","nat","bat"]))