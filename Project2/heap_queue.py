class HeapQueue:
    
    def __init__(self, min_heap=True):
        self.heap = []
        self.min_heap = min_heap
    
    def size(self):
        return len(self.heap)
 
    def push(self, item):
        """ Add then percelate up then return """
        self.heap.append(item)
 
        pos = len(self.heap) - 1
        parent = (pos - 1) // 2
 
        if self.min_heap:
            while parent >= 0 and self.heap[pos] < self.heap[parent]:
                self.heap[parent], self.heap[pos] = self.heap[pos], self.heap[parent]
                pos, parent = parent, (parent - 1) // 2
        else:
            while parent >= 0 and self.heap[pos] > self.heap[parent]:
                self.heap[parent], self.heap[pos] = self.heap[pos], self.heap[parent]
                pos, parent = parent, (parent - 1) // 2
 
    def pop(self):
        """
        Pop, percelate down then return
        """
        if not self.heap:
            return None
        result = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        pos = 0
        l = 1
        r = 2
 
        if self.min_heap:
            while l < len(self.heap):
                min_c = l
                if r < len(self.heap) and self.heap[r] < self.heap[l]:
                    min_c = r
 
                if self.heap[pos] > self.heap[min_c]:
                    self.heap[pos], self.heap[min_c] = self.heap[min_c], self.heap[pos]
                    pos = min_c
                    l = pos * 2 + 1
                    r = pos * 2 + 2
                else:
                    break
        else:
            while l < len(self.heap):
                max_c = l
                if r < len(self.heap) and self.heap[r] > self.heap[l]:
                    max_c = r
 
                if self.heap[pos] < self.heap[max_c]:
                    self.heap[pos], self.heap[max_c] = self.heap[max_c], self.heap[pos]
                    pos = max_c
                    l = pos * 2 + 1
                    r = pos * 2 + 2
                else:
                    break
        return result