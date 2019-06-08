class Queue:
    def __init__(self):
        self.size = 0
        self.queue = []

    def dequeue(self):
        if self.size:
            self.size -= 1
            return self.queue.pop(0)

    def enqueue(self, element):
        self.queue.append(element)
        self.size += 1
