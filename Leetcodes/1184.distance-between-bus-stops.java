/*
 * @lc app=leetcode id=1184 lang=java
 *
 * [1184] Distance Between Bus Stops
 */

// @lc code=start
class Solution {
    public int distanceBetweenBusStops(int[] distance, int start, int destination) {
        int loopLen = 0;
        int clockwise = 0;
        int i = start;

        do {
            // Circle problem should be solved by %
            loopLen += distance[i % distance.length];
            if (((++i) % distance.length) == destination) {
                clockwise = loopLen;
            }
        } while (i % distance.length != start);

        return Math.min(clockwise, loopLen - clockwise);
    }
}
// @lc code=end

