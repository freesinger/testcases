"""
class Single Linked Node definition
"""
class SingleListNode(object):
    def __init__(self, data):
        self.val = data
        self.next = None

    def getData(self):
        return self.val
    
    def getNext(self):
        return self.next
    
    def setData(self, newdata):
        self.val = newdata

    def setNext(self, newnext):
        # :type newnext: SingleListNode
        self.next = newnext
    
    def printValue(self):
        while self != None:
            print(self.val)
            self = self.next

"""
class Single Linked List definition
"""
class SingleLinkedList(object):
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    # insert at the beginning
    def prepend(self, item):
        temp = SingleListNode(item)
        # head is actually just a 'pointer'
        temp.setNext(self.head)
        self.head = temp
        
    # insert at the end
    def append(self, item):
        if self.head == None:
            self.head = SingleListNode(item)
        else:
            current = self.head
            while current.next != None:
                current = current.getNext()
            current.setNext(SingleListNode(item))

    def insert(self, position, item):
        temp = SingleListNode(item)
        if self.head == None:
            self.head = temp
        elif position > self.size() or position < 0:
            return print('position out of range')
        elif position == 0:
            self.prepend(item)
        else:
            current = self.head
            count = 1
            while count < position:
                current = current.next
                count += 1
            temp.setNext(current.getNext())
            current.setNext(temp)

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.getNext()
        return count

    def find(self, item):
        current = self.head
        found = False
        position = 1
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
                position += 1
        if found == True:
            return position
        else:
            return None
    
    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            elif current.getNext() == None and current.getData() != item:
                return print(item, "not exist!")
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

    def print(self):
        if self.head == None:
            return None
        current = self.head
        while current != None:
            print(current.getData())
            current = current.getNext()

"""
class Double Linked Node definition
"""
class DoubleListNode(object):
    def __init__(self, item):
        self.val = item
        self.prev = None
        self.next = None
    
    def getData(self):
        return self.val

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.val = newdata

    def setNext(self, newnext):
        self.next = newnext
        newnext.prev = self

    def getValue(self):
        while self != None:
            print(self.val)
            self = self.next

"""
class Double Linked List definition
"""
class DoubleLinkedList(object):
    def __init__(self):
        self.head = None
    
    def isEmpty(self):
        return self.head == None
    
    def prepend(self, item):
        temp = DoubleListNode(item)
        if self.head is not None:
            temp.setNext(self.head)
            # find the last Node
            current = self.head
            while current.next is not self.head:
                current = current.next
            # set the last Node's pointers
            current.next = temp
            temp.prev = current
            self.head = temp
        else:
            temp.prev = temp
            temp.next = temp
            self.head = temp
        
    def append(self, item):
        temp = DoubleListNode(item)
        if self.head == None:
            temp.prev = temp
            temp.next = temp
            self.head = temp
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = temp
            temp.prev = current
            temp.next = self.head
            self.head.prev = temp
    
    def insert(self, position, item):
        temp = DoubleListNode(item)
        if self.head == None:
            temp.next = temp
            temp.prev = temp
            self.head = temp
        elif position > self.size() or position < 0:
            return print("position out range")
        elif position == 0:
            self.prepend(item)
        else:
            current = self.head
            count = 1
            while count < position:
                current = current.next
                count += 1
            temp.next = current.next
            current.next.prev = temp
            temp.prev = current
            current.next = temp

    def size(self):
        current = self.head
        count = 1
        while current.next != self.head:
            current = current.next
            count += 1
        return count

    def find(self, item):
        current = self.head
        found = False
        position = 1
        while current.next != self.head and not found:
            if current.val == item:
                found = True
            else:
                current = current.next
                position += 1
        if found == True:
            return position
        else:
            return None

    def remove(self, item):
        current = self.head
        found = False
        while not found:
            if current.val == item:
                found = True
            else:
                current = current.next
                # check if the last value == item
                if current.next == self.head and current.val != item:
                    # break here raise Error
                    return print("Not that item!")
                   
        if current == self.head:
            if current.next == current:
                self.head = None
            else:
                current.next.prev = current.prev
                current.prev.next = current.next
                # set head or print in infinity loop
                self.head = current.next
        else:
            current.prev.next = current.next
            current.next.prev = current.prev
    
    def print(self):
        if self.head == None:
            return print(None)
        current = self.head
        while current.next != self.head:
            print(current.val)
            current = current.next
        print(current.val)        

"""
# Single linked list test
lst = SingleLinkedList()
print(lst.isEmpty())
lst.append(3)
lst.prepend(2)
lst.prepend(1)
lst.insert(3, 4)
lst.insert(0, 0)
lst.print()
# 0 1 2 3 4
lst.remove(5)
# 5 not exsit!
lst.remove(4)
print(lst.find(1))
# 2
lst.print()
# 0 1 2 3
print(lst.size())
# 4
"""

#-------------------------#
"""
# Double linked list test

# Case A:
dlst = DoubleLinkedList()
dlst.append(1)
dlst.prepend(2)
dlst.printValue()
# 1 2
dlst.remove(1)
dlst.remove(1)
# Not that item!
dlst.remove(3)
# Not that item!
dlst.printValue()
# 2


# Case B:
dlst = DoubleLinkedList()
print(dlst.isEmpty())
# True
dlst.append(3)
dlst.append(4)
dlst.append(5)
dlst.prepend(2)
dlst.prepend(1)
dlst.printValue()
# Output: 1 2 3 4 5
dlst.remove(3)
dlst.printValue()
# Output: 1 2 4 5
print(dlst.find(1))
# 1
print(dlst.find(3))
# None

# Case C:
dlst = DoubleLinkedList()
dlst.insert(1, 4)
dlst.append(5)
dlst.prepend(3)
dlst.print()
# 3 4 5
dlst.insert(0, 2)
dlst.print()
# 2 3 4 5
dlst.remove(2)
dlst.remove(5)
dlst.print()
# 3 4 
print(dlst.size())
# 2
"""