from pytest import mark
from datastructures.sorts import *
from datastructures.my_functions import is_sorted


test_lists = [
    [3, 5, 8, 9, 1],
    [1, 1, 1, 1, 1],
    [],
    [1],
    [9, 8, 7, 6, 5, 4, 3, 2, 1]
]


@mark.parametrize('arr', test_lists)
def test_heap_sort(arr):
    assert is_sorted(heap_sort(arr))


@mark.parametrize('arr', test_lists)
def test_bubble_sort(arr):
    assert is_sorted(bubble_sort(arr))
