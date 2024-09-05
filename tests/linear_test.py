from pytest import mark, fixture
from datastructures import *


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

class TestStack:
    @fixture
    def empty_stack(self):
        return Stack()

    @fixture
    def filled_stack(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        return stack

    def test_push(self, empty_stack):
        empty_stack.push(10)
        assert len(empty_stack) == 1
        assert empty_stack.peek() == 10

    def test_pop(self, filled_stack):
        assert filled_stack.pop() == 3
        assert len(filled_stack) == 2
        assert filled_stack.pop() == 2
        assert len(filled_stack) == 1

    def test_peek(self, filled_stack):
        assert filled_stack.peek() == 3
        filled_stack.pop()
        assert filled_stack.peek() == 2

    def test_len(self, filled_stack):
        assert len(filled_stack) == 3
        filled_stack.pop()
        assert len(filled_stack) == 2

    def test_is_empty(self, empty_stack):
        assert bool(empty_stack) is False
        empty_stack.push(5)
        assert bool(empty_stack) is True

class TestQueue:
    @fixture
    def empty_queue(self):
        return Queue()

    @fixture
    def filled_queue(self):
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        return queue

    def test_enqueue(self, empty_queue):
        empty_queue.enqueue(10)
        assert len(empty_queue) == 1
        assert empty_queue.peek_front() == 10

    def test_dequeue(self, filled_queue):
        assert filled_queue.dequeue() == 1
        assert len(filled_queue) == 2
        assert filled_queue.dequeue() == 2

    def test_peek_front(self, filled_queue):
        assert filled_queue.peek_front() == 1
        filled_queue.dequeue()
        assert filled_queue.peek_front() == 2

    def test_peek_back(self, filled_queue):
        assert filled_queue.peek_back() == 3

    def test_len(self, filled_queue):
        assert len(filled_queue) == 3
        filled_queue.dequeue()
        assert len(filled_queue) == 2

    def test_is_empty(self, empty_queue):
        assert bool(empty_queue) is False
        empty_queue.enqueue(5)
        assert bool(empty_queue) is True

class TestDeque:
    @fixture
    def empty_deque(self):
        return Deque()

    @fixture
    def filled_deque(self):
        deque = Deque()
        deque.push_back(1)
        deque.push_back(2)
        deque.push_back(3)
        return deque

    def test_push_front(self, empty_deque):
        empty_deque.push_front(10)
        assert len(empty_deque) == 1
        assert empty_deque.peek_front() == 10

    def test_push_back(self, empty_deque):
        empty_deque.push_back(20)
        assert len(empty_deque) == 1
        assert empty_deque.peek_back() == 20

    def test_pop_front(self, filled_deque):
        assert filled_deque.pop_front() == 1
        assert len(filled_deque) == 2
        assert filled_deque.pop_front() == 2

    def test_pop_back(self, filled_deque):
        assert filled_deque.pop_back() == 3
        assert len(filled_deque) == 2
        assert filled_deque.pop_back() == 2

    def test_peek_front(self, filled_deque):
        assert filled_deque.peek_front() == 1
        filled_deque.pop_front()
        assert filled_deque.peek_front() == 2

    def test_peek_back(self, filled_deque):
        assert filled_deque.peek_back() == 3

    def test_len(self, filled_deque):
        assert len(filled_deque) == 3
        filled_deque.pop_front()
        assert len(filled_deque) == 2

    def test_is_empty(self, empty_deque):
        assert bool(empty_deque) is False
        empty_deque.push_front(5)
        assert bool(empty_deque) is True
