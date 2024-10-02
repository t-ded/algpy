import string

import pytest

from algpy_src.data_structures.graphs.trees.tries.prefix_trie import PrefixTrie


@pytest.fixture
def prefix_trie() -> PrefixTrie[str]:
    return PrefixTrie(list(string.ascii_lowercase))


def test_prefix_trie_insert(prefix_trie: PrefixTrie[str]) -> None:
    prefix_trie.insert('cat')
    prefix_trie.insert('catapult')
    prefix_trie.insert('cattle')
    prefix_trie.insert('hours')

    assert prefix_trie.insert('horse') is True
    assert prefix_trie.insert('horse') is False


def test_prefix_trie_search(prefix_trie: PrefixTrie[str]) -> None:
    prefix_trie.insert('catapult')
    assert prefix_trie.search('cat') is None
    prefix_trie.insert('cat')
    assert prefix_trie.search('cat') is not None


def test_prefix_trie_delete(prefix_trie: PrefixTrie[str]) -> None:
    prefix_trie.insert('cattle')
    assert prefix_trie.delete('cat') is False
    assert prefix_trie.delete('cattle') is True
