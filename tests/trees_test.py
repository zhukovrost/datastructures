from pytest import fixture
from datastructures.trees.trees import *


# Тесты для SearchTree
class TestSearchTree:
    @fixture
    def search_tree(self):
        tree = SearchTree()
        tree.build([10, 5, 15, 3, 8, 12, 18])
        return tree

    def test_build(self, search_tree):
        assert len(search_tree) == 7

    def test_find_min(self, search_tree):
        assert search_tree.find_min() == 3

    def test_find_max(self, search_tree):
        assert search_tree.find_max() == 18

    def test_find_existing(self, search_tree):
        assert search_tree.find(8) == 8

    def test_find_non_existing(self, search_tree):
        assert search_tree.find(20) is None

    def test_insert(self, search_tree):
        assert search_tree.insert(6)
        assert search_tree.find(6) == 6
        assert len(search_tree) == 8

    def test_delete(self, search_tree):
        assert search_tree.delete(8) == 8
        assert search_tree.find(8) is None
        assert len(search_tree) == 6


# Тесты для SegmentTree
class TestSegmentTree:
    @fixture
    def segment_tree(self):
        tree = SegmentTree()
        tree.build([1, 2, 3, 4, 5, 6, 7])
        return tree

    def test_build(self, segment_tree):
        assert len(segment_tree) == 7

    def test_get_at(self, segment_tree):
        assert segment_tree.get_at(0) == 1
        assert segment_tree.get_at(6) == 7

    def test_insert_at(self, segment_tree):
        segment_tree.insert_at(3, 10)
        assert segment_tree.get_at(3) == 10
        assert len(segment_tree) == 8

    def test_delete_at(self, segment_tree):
        segment_tree.delete_at(3)
        assert len(segment_tree) == 6
        assert segment_tree.get_at(3) == 5


# Тесты для AVLTree
class TestAVLTree:
    @fixture
    def avl_tree(self):
        tree = AVLTree()
        tree.build([10, 5, 15, 3, 8, 12, 18])
        return tree

    def test_build(self, avl_tree):
        assert len(avl_tree) == 7

    def test_balance_after_insert(self, avl_tree):
        avl_tree.insert(20)
        assert avl_tree.find_max() == 20
        assert len(avl_tree) == 8

    def test_balance_after_delete(self, avl_tree):
        avl_tree.delete(8)
        assert avl_tree.find(8) is None
        assert len(avl_tree) == 6


class TestTrie:
    words = [
        "preclude",
        "predict",
        "prefix",
        "preface",
        "prehistoric",
        "disagree",
        "disapprove",
        "disrupt",
        "disappear",
        "disarray",
        "apple",
        "abricot"
    ]

    @fixture
    def empty_trie(self):
        return Trie()

    @fixture
    def filled_trie(self, empty_trie):
        empty_trie.insert(*self.words)
        return empty_trie

    def test_get_words(self, filled_trie):
        for word in filled_trie.get_words_with_prefix("dis"):
            assert word in ["disagree",
                            "disapprove",
                            "disrupt",
                            "disappear",
                            "disarray"]
        assert len(filled_trie.get_words_with_prefix("dis")) == 5
        assert len(filled_trie.get_words_with_prefix("pre")) == 5
        assert filled_trie.get_words_with_prefix("pre") != filled_trie.get_words_with_prefix("dis")

    def test_insert(self, empty_trie):
        empty_trie.insert(*self.words)
        for word in empty_trie:
            assert word in self.words

    def test_search(self, filled_trie):
        for word in filled_trie:
            assert word in self.words
        assert "pineapple" not in filled_trie
        assert "disappears" not in filled_trie
