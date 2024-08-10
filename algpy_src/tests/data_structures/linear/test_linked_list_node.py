import pytest

from algpy_src.base.constants import TEST_SEED
from algpy_src.data_structures.linear.linked_list_node import LinkedListNode


@pytest.fixture
def ll_node() -> LinkedListNode:
    return LinkedListNode(TEST_SEED)


def test_basic_node_operations(ll_node: LinkedListNode) -> None:
    node = ll_node
    assert node.value == TEST_SEED
    assert node.successor is None
    assert node.predecessor is None
    assert repr(node) == f'LinkedListNode ((value={TEST_SEED}), successor=None, predecessor=None)'

    node.add_successor(TEST_SEED + 1)
    assert repr(node) == f'LinkedListNode ((value={TEST_SEED}), successor=(value={TEST_SEED + 1}), predecessor=None)'
    assert node.successor is not None
    assert node.successor.value == TEST_SEED + 1
    node.add_predecessor(TEST_SEED - 1)
    assert repr(node) == f'LinkedListNode ((value={TEST_SEED}), successor=(value={TEST_SEED + 1}), predecessor=(value={TEST_SEED - 1}))'
    assert node.predecessor is not None
    assert node.predecessor.value == TEST_SEED - 1

    new_successor = LinkedListNode(TEST_SEED + 2)
    new_predecessor = LinkedListNode(TEST_SEED - 2)
    node.change_successor(new_successor)
    node.change_predecessor(new_predecessor)
    assert node.successor is not None
    assert node.successor.value == TEST_SEED + 2
    assert node.successor == new_successor
    assert node.predecessor is not None
    assert node.predecessor.value == TEST_SEED - 2
    assert node.predecessor == new_predecessor

    assert str(node) == f'(value={TEST_SEED})'
    assert repr(node) == f'LinkedListNode ((value={TEST_SEED}), successor=(value={TEST_SEED + 2}), predecessor=(value={TEST_SEED - 2}))'
