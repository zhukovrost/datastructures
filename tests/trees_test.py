from pytest import fixture, raises
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


class TestRedBlackTree:
    @fixture
    def red_black_tree(self):
        tree = RedBlackTree()
        values = [10, 20, 30, 15, 25]
        for value in values:
            tree.insert(value)
        return tree

    def test_insert(self, red_black_tree):
        # Insert new element and check
        assert red_black_tree.insert(5) == True
        assert red_black_tree.find(5) == 5
        assert red_black_tree.size == 6

    def test_find(self, red_black_tree):
        # Test finding existing elements
        assert red_black_tree.find(10) == 10
        assert red_black_tree.find(25) == 25

        # Test finding non-existing element
        assert red_black_tree.find(40) is None

    def test_delete(self, red_black_tree):
        # Test deletion of a node
        assert red_black_tree.delete(15) == 15
        assert red_black_tree.find(15) is None
        assert red_black_tree.size == 4

    def test_delete_root(self, red_black_tree):
        # Test deletion of the root node
        assert red_black_tree.delete(20) == 20
        assert red_black_tree.find(20) is None
        assert red_black_tree.size == 4

    def test_delete_nonexistent(self, red_black_tree):
        # Test deletion of a non-existing node
        with raises(AssertionError):
            red_black_tree.delete(40)

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


class TestTwoThreeTree:
    @fixture
    def two_three_tree(self):
        tree = TwoThreeTree()
        return tree

    def test_insert_and_search(self, two_three_tree):
        tree = two_three_tree

        # Insert elements and test search
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        tree.insert(40)
        tree.insert(50)

        assert tree.search(10) is True
        assert tree.search(20) is True
        assert tree.search(30) is True
        assert tree.search(40) is True
        assert tree.search(50) is True

        # Test for non-existent elements
        assert tree.search(5) is False
        assert tree.search(60) is False

    def test_split_and_structure(self, two_three_tree):
        tree = two_three_tree

        # Insert more than 3 elements to trigger a split
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)

        assert tree.root.keys == [20]  # Root should split with middle key promoted
        assert tree.root.children[0].keys == [10]  # Left child
        assert tree.root.children[1].keys == [30]  # Right child

        tree.insert(40)
        tree.insert(50)

        # Test new structure after more insertions
        assert tree.root.keys == [20, 40]
        assert tree.root.children[0].keys == [10]
        assert tree.root.children[1].keys == [30]
        assert tree.root.children[2].keys == [50]

    def test_complex_insertions(self, two_three_tree):
        tree = two_three_tree

        # Insert many elements to test deeper structure
        for i in range(10, 100, 10):
            tree.insert(i)

        assert tree.search(70) is True
        assert tree.search(35) is False  # 35 is not in the tree
