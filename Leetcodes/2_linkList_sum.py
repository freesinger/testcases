"""
You are given two non-empty linked lists representing two non-negative integers. 
The digits are stored in reverse order and each of their nodes contain a single digit. 
Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example:

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.

"""

# Solution A: (转换成数字运算)
class Solution(object):
    def addTwoNumbers(self, L1, L2):
        # 检查元素
        """
        :type L1: ListNode
        :type L2: ListNode
        :rtype: ListNode
        """
        if not L1:
            return L2
        if not L2:
            return L1

        val1, val2 = [L1.val], [L2.val]
        while L1.next:
            val1.append(L1.next.val)
            L1 = L1.next
        while L2.next:
            val2.append(L2.next.val)
            L2 = L2.next
        
        num1 = ''.join([str(i) for i in val1[::-1]])
        num2 = ''.join([str(i) for i in val2[::-1]])

        # 倒序存储结果
        tmp = str(int(num1) + int(num2))[::-1]
        # res保存链表
        res = ListNode(int(tmp[0]))
        # 保存运行结果
        run_res = res
        for i in range(1, len(tmp)):
            run_res.next = ListNode(int(tmp[i]))
            run_res = run_res.next
        return res

class Solution(object):
    def addTwoNumbers(self, L1, L2):
        # check List
        if not L1:
            return L2
        if not L2:
            return L1
        
        if L1.val + L2.val < 10:
            L3 = ListNode(L1.val + L2.val)
            L3.next  = self.addTwoNumbers(L1.next, L2.next)
        else:
            L3 = ListNode(L1.val + L2.val - 10)
            tmp = ListNode(1)
            tmp.next = None
            L3.next = self.addTwoNumbers(L1.next, self.addTwoNumbers(L2.next, tmp))

        return L3