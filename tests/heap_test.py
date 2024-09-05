from pytest import mark, fixture
from datastructures import *


def is_heap(arr: MinHeap):
    if not isinstance(arr, MinHeap):
        raise TypeError

    flag = True
    for i in range(len(arr)):
        if arr.has_left_child(i):
            if arr[i] > arr.left_child(i):
                flag = False
                break
        if arr.has_right_child(i):
            if arr[i] > arr.right_child(i):
                flag = False
                break

    return flag


class TestHeap:
    @fixture
    def empty_heap(self):
        return MinHeap()

    @fixture
    def filled_heap(self):
        return MinHeap([1, 2, 3, 4, 5, 6, 7, 8, 9])

    @mark.parametrize('index,value', [(0, -1), (1, 0), (2, 0), (3, 1), (6, 2)])
    def test_get_parent_index(self, index, value, empty_heap):
        assert empty_heap.get_parent_index(index) == value

    @mark.parametrize('arr', [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 2, 3, 4, 5, 6, 7, 8, 1],
        [2, 4, 3, 100000, 34, 3, 8]
    ])
    def test_build_heap(self, arr):
        heap = MinHeap(arr)
        assert is_heap(heap)

    @mark.parametrize('index', [None, 0, 8, 4, 1000])
    def test_poll(self, index, filled_heap):
        start_len = len(filled_heap)

        if index is not None and start_len <= index:
            try:
                filled_heap.poll(index)
            except IndexError:
                assert True
            else:
                assert False
            return

        if index is None:
            item = filled_heap[0]
        else:
            item = filled_heap[index]

        item_count = filled_heap.count(item)

        result = filled_heap.poll(index)
        assert result == item
        assert len(filled_heap) == start_len - 1
        assert item_count - 1 == filled_heap.count(item)
        assert is_heap(filled_heap)

    @mark.parametrize('val', [-1, 5, 1000])
    def test_add(self, val, filled_heap):
        val_count = filled_heap.count(val)
        filled_heap.add(val)
        assert val_count + 1 == filled_heap.count(val)
        assert is_heap(filled_heap)


class TestPriorityQueue:
    @fixture
    def empty_queue(self):
        return PriorityQueue()

    @fixture
    def filled_queue(self):
        q = PriorityQueue()
        q.enqueue('a', 1)
        q.enqueue('b', 2)
        q.enqueue('c', 3)
        return q

    @mark.parametrize('item,priority', [('task1', 5), ('task2', 0), ('task3', -1)])
    def test_enqueue(self, item, priority, filled_queue):
        start_len = len(filled_queue)
        filled_queue.enqueue(item, priority)
        assert len(filled_queue) == start_len + 1
        assert is_heap(filled_queue)

    def test_dequeue(self, filled_queue):
        assert filled_queue.dequeue() == 'a'
        assert filled_queue.dequeue() == 'b'
        assert len(filled_queue) == 1

    def test_empty_dequeue(self, empty_queue):
        try:
            empty_queue.dequeue()
        except IndexError:
            assert True
        else:
            assert False
