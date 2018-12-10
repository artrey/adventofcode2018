import typing


class DListNode:
    """
    A node in a doubly-linked list.
    """
    def __init__(self,
                 data: typing.Any=None,
                 prev_node: typing.Optional['DListNode']=None,
                 next_node: typing.Optional['DListNode']=None):
        self.data = data
        self.prev = prev_node
        self.next = next_node

    def __repr__(self):
        return repr(self.data)


class RoundedLinkedList:
    def __init__(self) -> None:
        self.head: typing.Optional[DListNode] = None
        self.count = 0

    def __repr__(self) -> str:
        """
        Return a string representation of the list.
        Takes O(n) time.
        """
        nodes = []
        curr = self.head
        while curr:
            nodes.append(repr(curr))
            curr = curr.next
        return '[' + ', '.join(nodes) + ']'

    def set_head(self, node: DListNode) -> None:
        self.head = node

    def set_single_head(self, node: DListNode) -> None:
        self.head = node
        self.head.next = self.head
        self.head.prev = self.head
        self.count = 1

    def insert_after(self, node: DListNode, after: DListNode) -> DListNode:
        node.prev = after
        node.next = after.next
        after.next.prev = node
        after.next = node
        self.count += 1
        return node

    def insert(self, data: typing.Any, after: DListNode) -> DListNode:
        """
        Insert a new element after the `after` node.
        Takes O(1) time.
        """
        node = DListNode(data=data)
        if self.count > 0:
            self.insert_after(node, after)
        else:
            self.set_single_head(node)
        return node

    def prepend(self, data: typing.Any) -> DListNode:
        """
        Insert a new element before the head.
        Takes O(1) time.
        """
        return self.insert(data, self.head.prev)

    def append(self, data: typing.Any) -> DListNode:
        """
        Insert a new element after the head.
        Takes O(1) time.
        """
        return self.insert(data, self.head)

    def find(self, data: typing.Any) -> typing.Optional[DListNode]:
        """
        Search for the first element with `data` matching.
        Return the element or `None` if not found.
        Takes O(n) time.
        """
        if self.count == 0:
            return None

        curr = self.head
        idx = 0
        while idx < self.count and curr.data != data:
            curr = curr.next
            idx += 1

        if idx < self.count:
            return curr

        return None

    def remove_node(self, node: DListNode) -> DListNode:
        """
        Unlink an element from the list and return it.
        Takes O(1) time.
        """
        if self.count == 1 and self.head == node:
            self.count = 0
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        node.prev = None
        node.next = None
        return node

    def remove(self, data: typing.Any) -> typing.Optional[DListNode]:
        """
        Remove the first occurrence of `data` in the list.
        Takes O(n) time.
        """
        elem = self.find(data)
        if elem is not None:
            return self.remove_node(elem)
        return None
