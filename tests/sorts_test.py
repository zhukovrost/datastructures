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
        [9, 8, 7, 6, 5, 4, 3, 2, 1]
    ]


def test_heap_sort(lists):
    for arr in lists:
        arr = arr.copy()
        default = is_sorted(arr)
        assert is_sorted(heap_sort(arr))
        assert default == is_sorted(arr)
        heap_sort(arr, inplace=True)
        assert is_sorted(arr)


def test_bubble_sort(lists):
    for arr in lists:
        arr = arr.copy()
        default = is_sorted(arr)
        assert is_sorted(bubble_sort(arr))
        assert default == is_sorted(arr)
        bubble_sort(arr, inplace=True)
        assert is_sorted(arr)
