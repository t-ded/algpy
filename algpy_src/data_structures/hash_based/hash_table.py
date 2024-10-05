from typing import TypeVar, Generic, cast, Optional

from algpy_src.base.constants import Hashable
from algpy_src.data_structures.container import Container
from algpy_src.data_structures.linear.linked_list import LinkedList

_K = TypeVar('_K', bound=Hashable)
_V = TypeVar('_V')


class HashTable(Container, Generic[_K, _V]):

    _EMPTY_BUCKET = object()

    def __init__(self, expected_size: int = 64) -> None:
        super().__init__()
        self._max_size = expected_size
        self._filled = 0
        self._hash_table: list[LinkedList] = [cast(LinkedList, self._EMPTY_BUCKET)] * self._max_size

    @property
    def __len__(self) -> int:
        return self._filled

    @property
    def name(self) -> str:
        return 'HashMap'

    @property
    def space_complexity(self) -> str:
        return 'n'

    @property
    def best_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_insert_description(self) -> str:
        return 'no collisions'

    @property
    def average_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_insert_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_insert_description(self) -> str:
        return 'all collisions'

    @property
    def best_case_delete_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_delete_description(self) -> str:
        return 'no collisions'

    @property
    def average_case_delete_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_delete_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_delete_description(self) -> str:
        return 'all collisions'

    @property
    def best_case_search_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_search_description(self) -> str:
        return 'no collisions'

    @property
    def average_case_search_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_search_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_search_description(self) -> str:
        return 'all collisions'

    def _rehash_if_necessary(self) -> None:
        """
        Utility function to dynamically resize the underlying array.
        """
        if self._filled >= 0.75 * self._max_size:
            self._max_size *= 2
            new_hash_table: list[LinkedList] = [cast(LinkedList, self._EMPTY_BUCKET)] * self._max_size
            for bucket in self._hash_table:
                if bucket != self._EMPTY_BUCKET and (head := bucket.head) is not None:
                    new_key_hash = hash(head.value[0]) % self._max_size
                    new_hash_table[new_key_hash] = bucket
            self._hash_table = new_hash_table

    def insert(self, key: _K, value: _V) -> None:
        """
        Insert a key-value pair to the hash table.
        If a key is already present, its value is rewritten.

        Parameters
        ----------
        key : Hashable
            Any object implementing __hash__.
        value : _V
            Any object.
        """
        key_hash = hash(key) % self._max_size
        current_value = self._hash_table[key_hash]
        if current_value == self._EMPTY_BUCKET:
            new_bucket = LinkedList('doubly')
            new_bucket.append((key, value))
            self._hash_table[key_hash] = new_bucket
            self._filled += 1
        else:
            changed = False
            for node in current_value:
                if node.value[0] == key:
                    node.change_value((key, value))
                    changed = True
                    break
            if not changed:
                current_value.append((key, value))
        self._rehash_if_necessary()

    def delete(self, key: _K) -> None:
        """
        Remove a key from the hash table.
        If a key is not present, it is silently ignored.

        Parameters
        ----------
        key : Hashable
            Any object implementing __hash__.
        """
        key_hash = hash(key) % self._max_size
        current_value = self._hash_table[key_hash]
        if current_value != self._EMPTY_BUCKET:
            for i, node in enumerate(current_value):
                if node.value[0] == key:
                    current_value.delete(node.value, i)
            if len(current_value) == 0:
                self._hash_table[key_hash] = cast(LinkedList, self._EMPTY_BUCKET)
                self._filled -= 1

    def search(self, key: _K) -> Optional[_V]:
        """
        Return a value from the hash table associated with the given key if such key exists, otherwise None.

        Parameters
        ----------
        key : Hashable
            Any object implementing __hash__.

        Returns
        -------
        value : Optional[_V]
            None if key not present in the hash table, otherwise value associated with the given key.
        """
        key_hash = hash(key) % self._max_size
        current_value = self._hash_table[key_hash]
        if current_value != self._EMPTY_BUCKET:
            for node in current_value:
                if node.value[0] == key:
                    return node.value[1]
        return None

