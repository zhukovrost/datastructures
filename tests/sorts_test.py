from pytest import fixture
from datastructures.sorts import *
from datastructures.my_functions import is_sorted


@fixture
def lists():
    return [
        [3, 5, 8, 9, 1],
        [1, 1, 1, 1, 1],
        [],
        [1],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [100, 1, -1000, 421, 4, 34, 99, -123, 43, 50, 23]
    ]


def canvas(func, lists):
    for arr in lists:
        arr = arr.copy()
        default = is_sorted(arr)
        assert is_sorted(func(arr))
        assert default == is_sorted(arr)
        assert is_sorted(func(arr, reverse=True)[::-1])
        func(arr, inplace=True)
        assert is_sorted(arr)

def test_heap_sort(lists):
    canvas(heap_sort, lists)


def test_bubble_sort(lists):
    canvas(bubble_sort, lists)


def test_quicksort(lists):
    canvas(quicksort, lists)

def test_merge_sort(lists):
    canvas(merge_sort, lists)