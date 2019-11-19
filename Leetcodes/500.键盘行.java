import java.util.ArrayList;

/*
 * @lc app=leetcode.cn id=500 lang=java
 *
 * [500] 键盘行
 */

// @lc code=start
class Solution {
    public String[] findWords(String[] words) {
        String firstLine = "qwertyuiop";
        String secondLine = "asdfghjkl";
        String thirdLine = "zxcvbnm";
        ArrayList<String> res = new ArrayList<>();

        for (String word : words) {
            int f = 0, s = 0, t = 0;
            for (int j = 0; j < word.length(); j++) {
                char ch = Character.toLowerCase(word.charAt(j));
                // if (firstLine.indexOf(ch))
                if (firstLine.contains(""+ch)) f = 1;
                if (secondLine.contains(""+ch)) s = 1;
                if (thirdLine.contains(""+ch)) t = 1;
            }
            if ((f + s + t) == 1) res.add(word);
        }
        return res.toArray(new String[res.size()]);
    }
}
// @lc code=end

