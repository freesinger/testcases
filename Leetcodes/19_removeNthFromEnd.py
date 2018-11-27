"""
Given a linked list, remove the n-th node from the end of list and return its head.

Example:
Given linked list: 1->2->3->4->5, and n = 2.
After removing the second node from the end, the linked list becomes 1->2->3->5.
"""
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

from LinkList import *

def removeNthFromEnd(List, n):
    """
    :type head: ListNode
    :type n: int
    :rtype: ListNode
    """
    current = List.head
    if current == None:
        return head
    else:
        for i in range(n):
            current = current.next
        return current

def main():
    ListLen = int(input("List length: "))
    Listval = [int(input()) for i in range(ListLen)]
    elemNum = int(input("Number: "))
    lst = List()
    for e in Listval:
        lst.insert(e)
    size = lst.size()
    pos = size - elemNum
    lst.remove(removeNthFromEnd(lst, pos).getData())
    lst.printValue()

if __name__ == '__main__':
    main()
    

