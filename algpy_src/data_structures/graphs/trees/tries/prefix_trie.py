import string
from typing import Optional, Self, Generic, Iterable, Sequence, cast
from typing import TypeVar

from algpy_src.data_structures.container import Container
from algpy_src.data_structures.graphs.trees.tries.trie_node import TrieNode

T = TypeVar('T', bound=Sequence)


class PrefixTrie(Container, Generic[T]):

    def __init__(self, alphabet: Optional[Iterable[T]] = None) -> None:
        super().__init__()
        self._alphabet: dict[T, int] = {}
        if alphabet is None:
            for i, letter in enumerate(string.ascii_lowercase + string.ascii_uppercase):
                self._alphabet[cast(T, letter)] = i
        else:
            for i, word in enumerate(alphabet):
                self._alphabet[word] = i
        self._root = TrieNode('', len(self._alphabet))

    def print_trie(self) -> None:
        self._print_trie_recursive(self._root, [], 0)

    def _print_trie_recursive(self, node: TrieNode, prefix: list[T], length: int) -> None:

        if node.is_terminal:
            print('Terminal word:', prefix)

        for i in range(len(self._alphabet)):
            child = node.children[i]
            if child is not None:
                self._print_trie_recursive(child, prefix + [child.key], length + 1)

    @classmethod
    def from_words(cls, words: Iterable[T], alphabet: Optional[Sequence[T]]) -> Self:
        trie = cls(alphabet=alphabet)
        for word in words:
            trie.insert(word)
        return trie

    @property
    def name(self) -> str:
        return 'Trie'

    @property
    def space_complexity(self) -> str:
        return 'n'

    @property
    def best_case_insert_time_complexity(self) -> str:
        return 'k'

    @property
    def best_case_insert_description(self) -> str:
        return 'one-character present words'

    @property
    def average_case_insert_time_complexity(self) -> str:
        return 'k'

    @property
    def worst_case_insert_time_complexity(self) -> str:
        return 'k'

    @property
    def worst_case_insert_description(self) -> str:
        return 'high-length non-present words'

    @property
    def best_case_delete_time_complexity(self) -> str:
        return 'k'

    @property
    def best_case_delete_description(self) -> str:
        return 'one-character present words'

    @property
    def average_case_delete_time_complexity(self) -> str:
        return 'k'

    @property
    def worst_case_delete_time_complexity(self) -> str:
        return 'k'

    @property
    def worst_case_delete_description(self) -> str:
        return 'high-length non-present words'

    @property
    def best_case_search_time_complexity(self) -> str:
        return 'k'

    @property
    def best_case_search_description(self) -> str:
        return 'one-character present words'

    @property
    def average_case_search_time_complexity(self) -> str:
        return 'k'

    @property
    def worst_case_search_time_complexity(self) -> str:
        return 'high-length non-present words'

    @property
    def worst_case_search_description(self) -> str:
        return 'k'

    def _traverse_to_word(self, word: T, insert_along: bool) -> Optional[TrieNode]:
        current = self._root
        for char in word:
            char_pos = self._alphabet[char]
            if current.children[char_pos] is None:
                if insert_along:
                    current.children[char_pos] = TrieNode(char, len(self._alphabet), parent=current)
                else:
                    return None
            child = current.children[char_pos]
            if child is not None:
                current = child
        return current

    def insert(self, word: T) -> bool:
        word_node = self._traverse_to_word(word, True)
        if word_node is None:
            raise ValueError('Could not insert the given word')
        if word_node.is_terminal:
            return False
        word_node.set_terminal(True)
        return True

    def search(self, word: T) -> Optional[TrieNode[T]]:
        word_node = self._traverse_to_word(word, False)
        if word_node is None or word_node.is_terminal is False:
            return None
        return word_node

    def delete(self, word: T) -> bool:
        word_node = self._traverse_to_word(word, False)
        if word_node is None or word_node.is_terminal is False:
            return False
        word_node.set_terminal(False)

        if all(word_node.children) is False and word_node.parent is not None:
            node_position = self._alphabet[word_node.key]
            word_node.parent.children[node_position] = None

        return True