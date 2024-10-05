from typing import Any

import pytest

from algpy_src.base.constants import TEST_SEED
from algpy_src.data_structures.hash_based.hash_table import HashTable


class WorstCaseHashableObject:
    def __hash__(self) -> int:
        return TEST_SEED


@pytest.fixture
def ht() -> HashTable[Any, Any]:
    return HashTable()


@pytest.mark.parametrize(
    'pairs_to_insert',
    [
        pytest.param([('dog', 'woof'), ('cat', 'meow'), ('cow', 'boo')], id='Str-str pairs'),
        pytest.param([(i, i * 2) for i in range(50)], id='Int-int pairs'),
    ]
)
def test_hash_table_operations(ht: HashTable, pairs_to_insert: list[tuple[Any, Any]]) -> None:
    print(ht._hash_table)
    for key, value in pairs_to_insert:
        ht.insert(key, value)
        assert ht.search(key) == value

    for key, value in pairs_to_insert:
        ht.delete(key)
        assert ht.search(key) is None


def test_handles_worst_case_collisions(ht: HashTable) -> None:
    for i in range(40):
        obj = WorstCaseHashableObject()
        ht.insert(obj, i)
        assert ht.search(obj) == i


def test_rehashing_works(ht: HashTable) -> None:
    for i in range(10_000):
        ht.insert(i, i * 2)
        assert ht.search(i) == i * 2


def test_cannot_hash_unhashable(ht: HashTable) -> None:
    with pytest.raises(TypeError):
        ht.insert([], 10)  # type: ignore # (we test invalid input type error)