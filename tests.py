import unittest

from random import randint, seed
from Project1.List import List, fix_playlist

seed(331)  # change this or comment for more testing


class TestProject1(unittest.TestCase):

    def test_accessors(self):
        """front, back"""

        lst = List()  # empty
        assert lst.front() is lst.node
        assert lst.back() is lst.node

        lst = List(1)  # 1 node of None
        assert lst.front().val is None
        assert lst.back().val is None

        lst = List(2, 1)  # 2 nodes of 1
        assert lst.front().val == 1
        assert lst.back().val == 1
        assert lst.front() is not lst.back()
        assert lst.front().prev is lst.node
        assert lst.back().next is lst.node

        lst = List(10, 6)  # 10 nodes of 6
        assert lst.front().val == 6
        assert lst.back().val == 6

        lst = List(container=[1, 2, 3, 4, 5])  # different values
        assert lst.front().val == 1
        assert lst.back().val == 5

    def test_swap(self):
        """swap"""

        lst1 = List(container=[])
        lst2 = List(container=[6])

        lst1.swap(lst2)

        assert lst1 == List(container=[6])
        assert lst2 == List(container=[])

        lst1.assign(container=[1, 2])
        lst2.assign(container=[3, 4])

        lst1.swap(lst2)

        assert lst1 == List(container=[3, 4])
        assert lst2 == List(container=[1, 2])

        lst1.assign(container=[i for i in range(20)])
        lst2.assign(container=[i for i in range(30, -1, -1)])

        lst1.swap(lst2)

        assert lst1 == List(container=[i for i in range(30, -1, -1)])
        assert lst2 == List(container=[i for i in range(20)])

    def test_capacity(self):
        """empty, size"""

        lst = List()  # empty
        assert lst.empty()
        assert lst.size() == 0

        lst.assign(1)  # 1 node
        assert not lst.empty()
        assert lst.size() == 1

        lst.clear()
        assert lst.empty()
        assert lst.size() == 0

        lst.assign(container=[9, 2, 6, None, 5, 3])  # 6 nodes
        assert not lst.empty()
        assert lst.size() == 6

        lst.assign(container=[1 for i in range(200)])
        assert lst.size() == 200

    def test_string(self):
        """__str__"""

        def gen_string():
            assert str(List(container=arr)) == " <-> ".join([str(x) for x in arr])

        for arr in [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]:
            gen_string()

    def test_insert(self):
        """insert"""

        lst = List()

        # empty
        lst.insert(lst.node.next, 2)
        assert lst == List(container=[2])

        # front
        lst.insert(lst.node.next, 0)
        assert lst == List(container=[0, 2])

        # middle
        lst.insert(lst.node.prev, 1)
        assert lst == List(container=[0, 1, 2])

        # back
        lst.insert(lst.node, 3)
        assert lst == List(container=[0, 1, 2, 3])

        # multiple - val
        lst.insert(lst.node.next, 5, 4)
        assert lst == List(container=[5, 5, 5, 5, 0, 1, 2, 3])

        # position: Negligible, val: Negligible, n: 0
        lst.assign(1)
        lst.insert(lst.node.next, 10, 0)
        assert List(container=[None]) == lst

    def test_erase(self):
        """erase"""

        lst = List(container=[0, 1, 2, 3])

        # back
        assert lst.erase(lst.node.prev) == lst.node
        assert lst == List(container=[0, 1, 2])

        # middle
        assert lst.erase(lst.node.next.next) == 2
        assert lst == List(container=[0, 2])

        # front
        assert lst.erase(lst.node.next) == 2
        assert lst == List(container=[2])

        # one node
        assert lst.erase(lst.node.next) == lst.node
        assert lst == List()

        # empty
        assert lst.erase(lst.node.next) is lst.node
        assert lst == List()

        lst.assign(container=[4, 5, 6, 7])

        # remove three nodes with two pointers
        assert lst.erase(lst.node.next, lst.node.prev) == 7
        assert lst == List(container=[7])

        lst.assign(container=[4, 5, 6, 7])

        # root node
        lst.erase(lst.node)
        assert List(container=[4, 5, 6, 7]) == lst

        # remove one with two pointers
        assert lst.erase(lst.node.next, lst.node) == lst.node
        assert lst == List()

    def test_push_pop(self):
        """push_front, push_back, pop_front, pop_back"""

        # hint: this class will be in one of your hidden test cases
        # remember Lists are type-agnostic
        class SpecialClass:
            def __init__(self, num=None):
                self.num = num if num else randint(0, 100)

            def __str__(self):
                return str(self.num)

            def __eq__(self, other):
                return self.num == other.num if other else False

        lst = List()
        lst.push_front(SpecialClass(2))

        assert lst.node.next == SpecialClass(2)
        assert lst.node.prev == SpecialClass(2)

        lst.push_back(SpecialClass(1))
        assert lst.node.next == SpecialClass(2)
        assert lst.node.prev == SpecialClass(1)

        lst.pop_front()
        lst.pop_back()

        assert lst.node.next is lst.node

        # empty list
        lst.pop_front()
        lst.pop_back()

        assert lst.node.next is lst.node

    def test_remove(self):
        """remove, remove_if"""

        # remove
        array = [([], [], 3), ([1], [], 1), ([5, 4], [5], 4), ([0, 0], [], 0), ([1, 1, 1, 2], [2], 1),
                 ([2, 5, 5, 5], [2], 5), ([1, 1, 1], [], 1), ([1, 2, 2, 3], [1, 3], 2), ([4, 5, 5, 5, 6], [4, 6], 5),
                 ([6, 5, 5, 6, 6], [5, 5], 6), ([1, 6, 2, 8], [1, 6, 2, 8], 7)]

        lst = List()
        for arr in array:
            lst.assign(container=arr[0])
            lst.remove(arr[2])
            assert lst == List(container=arr[1])

        # remove_if
        def is_even(x: int) -> bool:
            return not x % 2

        def is_palindrome(x: str) -> bool:
            for i in range(len(x)):
                if x[i] != x[-(i + 1)]:
                    return False
            return True

        lst = List(container=[1, 6, 3, 7, 8, 0, 3, 6, 2, 1, 0, 5])
        lst.remove_if(is_even)
        assert lst == List(container=[1, 3, 7, 3, 1, 5])

        lst = List(container=["a", "ab", "bab", "abba", "ababa", "abbab"])
        lst.remove_if(is_palindrome)
        assert lst == List(container=["ab", "abbab"])

    def test_reverse(self):
        """reverse"""

        lst = List()
        for arr in [[], [1], [9, 7], [6, 0, 1]]:
            lst.assign(container=arr)
            lst.reverse()
            arr.reverse()
            assert lst == List(container=arr)

    def test_unique(self):
        """unique"""
        array = [([], []), ([1], [1]), ([5, 4], [5, 4]), ([0, 0], [0]), ([1, 1, 1, 2], [1, 2]), ([2, 5, 5, 5], [2, 5]),
                 ([1, 1, 1], [1]), ([1, 2, 2, 3], [1, 2, 3]), ([4, 5, 5, 5, 6], [4, 5, 6]),
                 ([6, 5, 5, 6, 6], [6, 5, 6])]

        lst = List()
        for arr in array:
            lst.assign(container=arr[0])
            lst.unique()
            assert lst == List(container=arr[1])

    def test_application(self):
        """fix_playlist"""

        # empty - proper
        lst = List(container=[])
        assert fix_playlist(lst) is True
        assert lst == List(container=[])

        # empty - broken
        lst.node.next = None  # bug
        assert fix_playlist(lst) is True
        assert lst == List(container=[])

        # one item - proper
        lst.assign(container=[1])
        assert fix_playlist(lst) is True
        assert lst == List(container=[1])

        # one item - broken
        lst.assign(container=[1])
        lst.node.next.next = lst.node.prev = None  # bug
        assert fix_playlist(lst) is True
        assert lst == List(container=[1])

        # one item - improper
        lst.assign(container=[1])
        assert fix_playlist(lst) is True  # proper
        lst.node.prev.next = lst.node.next  # bug
        lst.node.prev = None  # bug
        assert fix_playlist(lst) is False

        # three items - improper
        lst.assign(container=[1, 2, 3])
        assert fix_playlist(lst) is True  # proper
        lst.node.prev.next = lst.node.next  # bug
        lst.node.prev = None  # bug
        assert fix_playlist(lst) is False


if __name__ == '__main__':
    unittest.main()
