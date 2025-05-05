class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class GameManager:
    def __init__(self):
        self.head = None
        self.values = set()
        self.length = 0

    def add_guess(self, value):
        if value.lower() in self.values:
            return False
        self.values.add(value.lower())
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self.length += 1
        return True

    def last_guess(self):
        cur = self.head
        if not cur:
            return None
        while cur.next:
            cur = cur.next
        return cur.value

    def score(self):
        return self.length

    def history(self):
        cur = self.head
        result = []
        while cur:
            result.append(cur.value)
            cur = cur.next
        return result