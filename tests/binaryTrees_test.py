from datastructures.binaryTrees import *
from pytest import mark, fixture


class TestHeap:
    @mark.parametrize('index,value', [(0, -1), (1, 0), (2, 0), (3, 1), (6, 2)])
    def test_get_parent_index(self, index, value):
        assert get_parent_index(index) == value
