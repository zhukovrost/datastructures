from pytest import mark, fixture
from datastructures import \
    Trie


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

