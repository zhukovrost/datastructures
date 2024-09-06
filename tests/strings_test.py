from datastructures.strings import *

cases = [
    ("abdabsaaebabcfuad", "abc", 10),
    ("abdabsaaebavbcfuad", "abc", -1),
    ("as", "adfasdfsdaf", -1),
    ("abcabc", "abc", 0),
    ("abssdaf", "", -1)
]

def search_canvas(func):
    for text, substring, expected in cases:
        assert func(text, substring) == expected

def test_brute():
    search_canvas(brute_force_search)

def test_rabin_karp():
    search_canvas(rabin_karp)
