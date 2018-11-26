class ListNode(object):
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
        # :type newnext: ListNode
        self.next = newnext
    
    def printValue(self):
        while self != None:
            print(self.val)
            self = self.next

class List(object):
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    # append in the head of list
    def add(self, item):
        temp = ListNode(item)
        # head is actually just a 'pointer'
        temp.setNext(self.head)
        self.head = temp
        
    # insertion at the beginning
    def insert(self, item):
        if (self.head == None):
            self.head = ListNode(item)
        else:
            current = self.head
            while (current.next != None):
                current = current.getNext()
            current.setNext(ListNode(item))

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
        position = 0
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
                position += 1
        if found == True:
            return position + 1
        else:
            return False
    
    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        
        if previous == self.head:
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