"""
The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this:
(you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows:

string convert(string s, int numRows);

Example 1:
Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"

Example 2:
Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:
P     I    N
A   L S  I G
Y A   H R
P     I
"""

class Solution(object):
    def string_Convert_A(self, original_string, numRow):
        # print(len(original_string))
        if numRow == 1 or numRow >= len(original_string):
            return original_string
        result = [''] * numRow

        currentRow = 0
        # direction: ↑ True ↓ False
        for char in original_string:
            result[currentRow] += char
            if currentRow == 0:
                currentRow += 1
                direction = True
            elif currentRow == numRow - 1:
                currentRow -= 1
                direction = False
            elif direction == True:
                currentRow += 1
            elif direction == False:
                currentRow -= 1
        # print(result)
        return ''.join(result)

    def string_Convert_B(self, original_string, numRow):
        # print(len(original_string))
        if numRow == 1 or numRow >= len(original_string):
            return original_string
        result = [''] * numRow

        currentRow = 0
        # Use 'step' to change direction
        for char in original_string:
            result[currentRow] += char
            if currentRow == 0:
                step = 1
            elif currentRow == numRow - 1:
                step = -1
            currentRow += step

        # print(result)
        return ''.join(result)

def main():
    string = input("Input: ")
    numRow = int(input("Row: "))
    strConvert = Solution()
    print(strConvert.string_Convert_A(string, numRow))
    print(strConvert.string_Convert_B(string, numRow))

if __name__ == '__main__':
    main()