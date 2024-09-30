from algpy_src.data_structures.graphs.trees.tries.trie_node import TrieNode


def test_trie_node() -> None:
    node = TrieNode('Hello', 256)
    assert node.is_terminal is False
    node.set_terminal(True)
    assert node.is_terminal is True