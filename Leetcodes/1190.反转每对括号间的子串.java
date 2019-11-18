import java.util.Stack;

/*
 * @lc app=leetcode.cn id=1190 lang=java
 *
 * [1190] 反转每对括号间的子串
 */

// @lc code=start
class Solution {
    public String reverseParentheses(String s) {
        Stack<String> stack = new Stack<>();
        stack.push("");
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                stack.push("");
            } else if (s.charAt(i) == ')') {
                StringBuilder stringBuilder = new StringBuilder(stack.pop());
                // String reverseTop = reverseString(stack.pop());
                stack.push(stack.pop() + stringBuilder.reverse());  
            } else {
                String top = stack.pop();
                stack.push(top + s.charAt(i));
            }
        }
        return stack.pop();
    }

    // private String reverseString(String s) {
    //     String res = "";
    //     for (int i = s.length() - 1; i >= 0; i--) {
    //         res += s.charAt(i);
    //     }
    //     return res;
    // }
}
// @lc code=end

