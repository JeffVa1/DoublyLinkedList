"""
Doubly Linked List
Author - Jeffrey Valentic
9/22/2020
"""

from __future__ import annotations  # allow self-reference
from typing import TypeVar, Generic, Callable  # function type
from Project1.Node import DoublyLinkedListNode as Node

T = TypeVar("T")

class List:
    """
    Adaptation of the C++ List implementation where its underlying
    structure is a cyclic Doubly Linked List
    """
    def __init__(self, num: int = None, val: Generic[T] = None, container: list = None) -> None:
        """
        Creates root node and sets its prev and next member variable to itself
        Assigns list with param values given
        :param num: count of val occurrences
        :param val: value to be stored in Node
        :param container: contains elements used in assign
        """
        self.node = Node(None)
        self.node.prev = self.node.next = self.node

        if num or container:
            self.assign(num, val, container)

    def __repr__(self) -> str:
        """
        :return: Represents the list as a string utilizing __str__
        """
        return self.__str__()

    def __eq__(self, other: List) -> bool:
        """
        :param other: compares equality with this List
        :return: True if equal otherwise False
        """
        def is_equal(node1: Node, node2: Node) -> bool:
            if node1 is self.node and node2 is other.node:
                return True
            if node1 is self.node or node2 is other.node or node1 != node2\
                    or node1.prev != node2.prev:
                return False
            return is_equal(node1.next, node2.next)
        return is_equal(self.node.next, other.node.next)

    def assign(self, num: int = None, val: Generic[T] = None, container: list = None):
        """
        Populates self with nodes using the given parameters
        :param num: represents the number of occurrences of val to assign to list
        :param val: value to have n occurrences
        :param container: used to generate nodes with its contents
        """
        self.clear()
        node = self.node

        if container:
            for item in container:
                node.next = Node(item, prev=node)
                node = node.next
        elif num:
            for _ in range(num):
                node.next = Node(val, prev=node)
                node = node.next

        node.next, self.node.prev = self.node, node

    def clear(self) -> None:
        """
        Resets list by reassigning root nodes' references to itself
        """
        self.node.prev = self.node.next = self.node

    # Implement below - Do not modify function signatures

    def empty(self) -> bool:
        """
        :return: if List contains any additional nodes other than the root node, False else True
        """
        if self.node.next is not self.node or self.node.prev is not self.node:
            return False
        return True

    def front(self) -> Node:
        """
        :return: first node in the list or root node if empty
        """
        return self.node.next

    def back(self) -> Node:
        """
        :return: last node in the list or root node if empty
        """
        if self.empty():
            return self.node
        return self.node.prev

    def swap(self, other: List) -> None:
        """
        :param other: List to swap contents
        """
        self.node, other.node = other.node, self.node

    def __str__(self) -> str:
        """
        RECURSIVE
        :return: string representation of linked list
        """
        def to_string(node):
            """string helper"""
            node_str = ''
            cur_node = node.next
            if cur_node is not self.node:
                if cur_node.next is not self.node:
                    node_str = str(cur_node) + " <-> " + to_string(cur_node)
                else:
                    node_str = str(cur_node)
            return node_str

        lst_string = to_string(self.node)
        return lst_string

    def size(self) -> int:
        """
        RECURSIVE
        :return: size of list or number of nodes not including the root node
        """
        def size_list(node) -> int:
            count = 0
            curNode = node.next
            if curNode is not self.node:
                count = 1 + size_list(curNode)
            return count
        return size_list(self.node)

    def insert(self, position: Node, val: Generic[T], num: int = 1) -> Node:
        """
        RECURSIVE
        Places node before given position with a value of val
        When num is given, insert num occurrences of node
        :param position: Node index to insert new node before
        :param val: value to insert
        :param num: number of insertions of val at position index
        :return: node that points to the first of the newly inserted nodes
        """
        prev_pos = position.prev
        new_node = Node(val, position, position.prev)
        if num > 0:
            position.prev = new_node
            prev_pos.next = new_node
            return self.insert(new_node, val, num-1)
        return new_node

    def erase(self, first: Node, last: Node = None) -> Node:
        """
        Erases node or nodes in list from first to, but not including last: [first, last)
        When last is not given, erase only first node
        :param first: position to start erasing (inclusive)
        :param last: position to end erasing (exclusive)
        :return: node that followed the last node erased
        """
        #first is root
        if first is self.node:
            return self.node
        #last is None
        if last is None:
            before = first.prev
            after = first.next
            before.next = after
            after.prev = before
            return after
        else:
            before = first.prev
            before.next = last
            last.prev = before
            return last

    def push_front(self, val: Generic[T]) -> None:
        """
        Inserts new Node with value of val in the front of the list
        :param val: value of new Node
        """
        self.insert(self.node.next, val)

    def push_back(self, val: Generic[T]) -> None:
        """
        Inserts new Node with value of val in the back of the list
        :param val: value of new Node
        """
        self.insert(self.node, val)

    def pop_front(self) -> None:
        """
        Erases Node in the front of the list
        """
        self.erase(self.node.next)

    def pop_back(self) -> None:
        """
        Erases Node in the back of the list
        """
        self.erase(self.node.prev)

    def remove(self, val: Generic[T]) -> None:
        """
        RECURSIVE
        Removes all nodes containing a value of val
        :param val: value to remove
        """
        def remove_node(node: Node) -> Node:
            """remove helper"""
            prev_node = node.prev
            next_node = node.next
            if node.val == val:
                prev_node.next = next_node
                next_node.prev = prev_node
            if next_node != None:
                remove_node(next_node)
            else:
                return next_node
        remove_node(self.node)

    def remove_if(self, pred: Callable[[T], bool]) -> None:
        """
        RECURSIVE
        Removes all Nodes with pred returning True
        :param pred: predicate function that returns a boolean
        """
        def remove_node_if(node: Node) -> Node:
            """remove_if helper"""
            prev_node = node.prev
            next_node = node.next
            if node != None and pred(node.val):
                prev_node.next = next_node
                next_node.prev = prev_node
            if next_node != None:
                remove_node_if(next_node)
            else:
                return self.node

        remove_node_if(self.node)

    def reverse(self) -> None:
        """
        RECURSIVE
        Reverses linked list in place
        """
        def reverse_list(node: Node) -> None:
            """reverse helper"""
            if not self.empty():
                temp = node.next
                node.next = node.prev
                node.prev = temp
            if node.prev != None:
                reverse_list(node.prev)
        reverse_list(self.node)

    def unique(self) -> None:
        """
        RECURSIVE
        Removes all but one element from every consecutive group of equal elements in the container
        """
        def unique_list(node: Node) -> Node:
            """unique helper"""
            if self.size() <= 1 or node.next is None or node is self.back():
                return node
            if node.val == node.next.val:
                temp = node.next.next
                node.next = temp
                temp.prev = node
                return unique_list(node)
            else:
                return unique_list(node.next)
        unique_list(self.node)

# Application Problem
def fix_playlist(lst: List) -> bool:
    """
    Checks if the given lst is proper, broken, or improper
    It is broken when there is no cycle
    It is improper when lst forms a cycle with a node other than the root node
    Fixes lst if broken in place
    :param lst: List to check and fix cycle
    :return: True if proper or fixed broken cycle else False
    """
    def fix_playlist_helper(slow: Node, fast: Node) -> bool:
        """fix_playlist helper"""
        start = lst.node
        if start.next is start:
            return True
        if slow.next is None and slow.next is not start:
            slow.next = start
            return True
        elif fast.next is None and fast.next is not start or fast.next.next is None and fast.next.next is not start:
            if fast.next is None and fast.next is not start:
                fast.next = start
                start.prev = fast.next
                return True
            elif fast.next.next is None and fast.next.next is not start:
                fast.next.next = start
                start.prev = fast.next
                return True
        if fast is start or fast.next is start:
            return True
        else:
            if fast == slow:
                return False
            fast = fast.next.next
            slow = slow.next
            return fix_playlist_helper(slow, fast)
    return fix_playlist_helper(lst.node, lst.node.next)
