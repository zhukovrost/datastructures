from pytest import mark, fixture
from datastructures import \
    Stack, Queue, SinglyLinkedList, DoublyLinkedList, StaticArray, Deque


class TestSinglyLinkedList:
    @fixture
    def empty_list(self):
        return SinglyLinkedList()

    @fixture
    def linked_list(self, empty_list):
        empty_list.build([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return empty_list

    def test_iterations(self, linked_list):
        assert list(linked_list) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_size(self, linked_list):
        assert len(linked_list) == 9

    def test_build(self, empty_list):
        empty_list.build([1, 2, 3])
        assert list(empty_list) == [1, 2, 3]

    @mark.parametrize('index,value', [(0, 1), (8, 9), (3, 4)])
    def test_get_at(self, linked_list, index, value):
        assert linked_list.get_at(index) == value

    @mark.parametrize('index,value', [(0, 100), (8, 100), (3, 1)])
    def test_set_at(self, linked_list, index, value):
        linked_list.set_at(index, value)
        assert linked_list.get_at(index) == value

    @mark.parametrize('index,value', [(0, 100), (8, 100), (9, 100), (3, 777)])
    def test_insert_at(self, linked_list, index, value):
        prev_val, i_val = None, None
        if index < len(linked_list):
            i_val = linked_list.get_at(index)
        if index > 0:
            prev_val = linked_list.get_at(index - 1)
        linked_list.insert_at(index, value)
        assert linked_list.get_at(index) == value
        if index < len(linked_list) - 1:
            assert linked_list.get_at(index + 1) == i_val
        if index > 0:
            assert linked_list.get_at(index - 1) == prev_val

    @mark.parametrize('index', [0, 8, 2])
    def test_delete_at(self, linked_list, index):
        val = linked_list.get_at(index)
        prev_val, next_val = None, None
        if index > 0:
            prev_val = linked_list.get_at(index - 1)
        if index < len(linked_list) - 1:
            next_val = linked_list.get_at(index + 1)
        assert val == linked_list.get_at(index)
        if index > 0:
            assert linked_list.get_at(index - 1) == prev_val
        if index < len(linked_list) - 2:
            assert linked_list.get_at(index + 1) == next_val

    @mark.parametrize('index,value', [(0, 1), (8, 9), (3, 4), (-1, 777)])
    def test_search(self, linked_list, index, value):
        assert linked_list.search(value) == index


class TestDoublyLinkedList(TestSinglyLinkedList):
    @fixture
    def empty_list(self):
        return DoublyLinkedList()

    @fixture
    def linked_list(self, empty_list):
        empty_list.build([1, 2, 3, 4, 5, 6, 7, 8, 9])
        return empty_list


class TestStaticArray:
    @fixture
    def empty_array(self):
        return StaticArray(6)

    @fixture
    def filled_array(self, empty_array):
        arr = empty_array
        arr.set_at(0, 1)
        arr.set_at(1, 2)
        arr.set_at(2, 3)
        arr.set_at(3, 4)
        arr.set_at(4, 5)
        arr.set_at(5, 6)
        return arr

    @mark.parametrize('index,value', [(0, 1), (5, 6), (3, 4)])
    def test_get_at(self, filled_array, index, value):
        assert filled_array.get_at(index) == value

    @mark.parametrize('index,value', [(0, 1), (5, 6), (3, 4)])
    def test_set_at(self, filled_array, index, value):
        filled_array.set_at(index, value)
        assert filled_array.get_at(index) == value

    def test_static(self, empty_array):
        empty_array.set_at(1, 100)
        assert list(empty_array) == [None, 100, None, None, None, None]

    @mark.parametrize('index,value', [(0, 1), (5, 6), (3, 4)])
    def test_search(self, filled_array, index, value):
        assert filled_array.search(value) == index
