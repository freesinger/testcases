import java.time.Month;
import java.time.Year;

/*
 * @lc app=leetcode id=1185 lang=java
 *
 * [1185] Day of the Week
 */

// @lc code=start
class Solution {
    public String dayOfTheWeek(int day, int month, int year) {
        String[] week = new String[] {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
        int d = Year.of(year).atMonth(Month.of(month)).atDay(day).getDayOfWeek().getValue() - 1;
        return week[d - 1];
    }
}
// @lc code=end

