/*
 * @lc app=leetcode id=1186 lang=java
 *
 * [1186] Maximum Subarray Sum with One Deletion
 */

// @lc code=start
class Solution {
    public int maximumSum(int[] arr) {
        int n = arr.length;
        int[] f = new int[n];
        int[] g = new int[n];
        int ans = arr[0];

        f[0] = arr[0];
        g[0] = Integer.MIN_VALUE;
        
        for (int i = 1; i < n; i++) {
            f[i] = Math.max(f[i - 1] + arr[i], arr[i]);
            g[i] = Math.max(g[i - 1] + arr[i], f[i - 1]);
            ans = Math.max(ans, Math.max(f[i], g[i]));
        }

        return ans;
    }
}
// @lc code=end

