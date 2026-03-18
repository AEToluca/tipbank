class _Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
class Deque:
    def __init__ (self):
        self.front_size = 0
        self.back_size = 0
        self.size = 0
        self.front_head = None
        self.back_head = None

    def insertFront(self, value: int):
        newNode = _Node (value) #Create new node
        newNode.next = self.front_head #Make old head next for new node
        self.front_head = newNode #Make old head new node
        self.front_size += 1 #Increment size
        self.size += 1
        self.balance()

        #Do same as add front but use back node
    def insertBack(self, value: int):
        newNode = _Node(value)
        newNode.next = self.back_head
        self.back_head = newNode
        self.back_size += 1
        self.size += 1
        self.balance()
    
    def removeFront(self) -> int:
        if self.isEmpty(): #Raise error if deque is empty
            raise IndexError("Deque is empty")
        
        if self.front_head is None:
            self.transferBackToFront()
        done = self.front_head.value
        self.front_head = self.front_head.next
        self.front_size -= 1
        self.size -= 1
        self.balance()
        return done
    
        #same as front but use back node
    def removeBack(self) -> int:
        if self.back_head is None:
            if self.front_head is None:
                raise IndexError("Deque is empty")
            self.transferFrontToBack()
        done = self.back_head.value
        self.back_head = self.back_head.next
        self.back_size -= 1
        self.size -= 1
        self.balance()
        return done

    def isEmpty(self) -> bool: #Check if deque is empty
        return self.front_head is None and self.back_head is None
    
    def getSize(self) -> int:
        return self.size
    
    def balance(self): #Balance the deque
        if self.front_size > 2 * self.back_size:
            self.transferFrontToBack()
        elif self.back_size > 2 * self.front_size:
            self.transferBackToFront()

    def transferBackToFront(self):
        if self.back_head is None:
            return
            
        #Create a variable to store the number of elements to transfer
        elementsToTransfer = self.back_size // 2
        if elementsToTransfer == 0:
            return
            
        #Find the last node to transfer
        current = self.back_head
        for _ in range(elementsToTransfer - 1):
            current = current.next
            
        #Transfer nodes
        newBackHead = current.next
        current.next = self.front_head
        self.front_head = self.back_head
        self.back_head = newBackHead
        
        #Update sizes
        self.front_size += elementsToTransfer
        self.back_size -= elementsToTransfer

    def transferFrontToBack(self):
        if self.front_head is None:
            return
            
        #Create a variable to store the number of elements to transfer
        elementsToTransfer = self.front_size // 2
        if elementsToTransfer == 0:
            return
            
        #Find the last node to transfer
        current = self.front_head
        for _ in range(elementsToTransfer - 1):
            current = current.next
            
        #Transfer nodes
        newFrontHead = current.next
        current.next = self.back_head
        self.back_head = self.front_head
        self.front_head = newFrontHead
        
        #Update sizes
        self.back_size += elementsToTransfer
        self.front_size -= elementsToTransfer
            
def main():
    dq = Deque()
    dq.insertFront(10)
    dq.insertBack(20)
    dq.insertFront(5)
    print(dq.removeFront()) # Output: 5
    print(dq.removeBack()) # Output: 20
    print(dq.isEmpty()) # Output: False
    print(dq.removeFront()) # Output: 10
    print(dq.isEmpty()) # Output: True

if __name__ == "__main__":
    main()
    
        


    

