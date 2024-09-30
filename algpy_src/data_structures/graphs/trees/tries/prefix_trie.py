import string
from typing import Optional, Self, Generic, Iterable
from typing import TypeVar

from algpy_src.data_structures.container import Container
from algpy_src.data_structures.graphs.trees.tries.trie_node import TrieNode

T = TypeVar('T')


class PrefixTrie(Container, Generic[T]):

    def __init__(self, alphabet: Optional[Iterable[T]] = None) -> None:
        super().__init__()
        self._alphabet = alphabet if alphabet is not None else list(iter(string.ascii_lowercase)) + list(iter(string.ascii_uppercase))
        self._root = TrieNode('')

    @classmethod
    def from_words(cls, words: Iterable[T], alphabet: Optional[Iterable[T]]) -> Self:
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

    def insert(self, word: T) -> None:
        raise NotImplementedError

    def search(self, word: T) -> Optional[TrieNode[T]]:
        raise NotImplementedError

    def delete(self, word: T) -> bool:
        raise NotImplementedError