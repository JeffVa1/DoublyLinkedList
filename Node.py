
from __future__ import annotations  # allow self-reference
from typing import TypeVar, Generic  # function type

T = TypeVar("T")


class SinglyLinkedListNode:
    """Singly Linked List Node Class"""

    def __init__(self, val: Generic[T], nxt: SinglyLinkedListNode = None):
        """
        :param val: value of node
        :param nxt: pointer to next node
        """
        self.val = val
        self.next = nxt

    def __str__(self):
        """:return: string representation of node"""
        return str(self.val)

    def __repr__(self):
        """:return: string representation of node"""
        return self.__str__()

    def __eq__(self, other: [SinglyLinkedListNode, Generic[T]]):
        """
        == operation
        :param other: item to compare
        :return: True if self is equal to other else False
        """
        if type(other) == SinglyLinkedListNode:
            return False if not other else self.val == other.val
        return self.val == other


class DoublyLinkedListNode(SinglyLinkedListNode):
    """Doubly Linked List Node Class"""

    def __init__(self, val: Generic[T], nxt: DoublyLinkedListNode = None, prev: DoublyLinkedListNode = None):
        """
        Instantiates parent class and prev member variable
        :param val: int or string value of node
        :param nxt: pointer to next node
        :param prev: pointer to previous node
        """
        SinglyLinkedListNode.__init__(self, val, nxt)
        self.prev = prev

    def __eq__(self, other: [DoublyLinkedListNode, Generic[T]]):
        """
        == operation
        :param other: item to compare
        :return: True if self is equal to other else False
        """
        if type(other) == DoublyLinkedListNode:
            return False if not other else self.val == other.val
        return self.val == other
