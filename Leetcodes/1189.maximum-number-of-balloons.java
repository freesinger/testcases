/*
 * @lc app=leetcode id=1189 lang=java
 *
 * [1189] Maximum Number of Balloons
 */

// @lc code=start
class Solution {
    public int maxNumberOfBalloons(String text) {
        String balloon = "balloonn";
        int res = Integer.MAX_VALUE;
        int[] cnt = new int[26 + 1];

        for (char ch : text.toCharArray()) {
            cnt[ch - 'a']++;
        }
        char[] t = balloon.toCharArray();
        for (char ch : t) {
            if (ch == 'l' | ch == 'o') {
                res = Math.min(res, cnt[ch - 'a'] / 2);
            } else {
                res = Math.min(res, cnt[ch - 'a']);
            }
        }
        
        return res;
    }
}
// @lc code=end

