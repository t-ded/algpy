import pytest

from algpy_src.base.constants import TEST_SEED
from algpy_src.data_structures.graphs.trees.heaps.heap_node import HeapNode

TEST_PRIO = 1


@pytest.fixture
def heap_node() -> HeapNode:
    return HeapNode(TEST_SEED, TEST_PRIO)


def test_basic_node_properties(heap_node: HeapNode) -> None:
    node = heap_node

    assert node.key == TEST_SEED
    assert node.priority == TEST_PRIO
    assert node.degree == 0

    assert node.successor is not None and node.successor.key == TEST_SEED
    assert node.predecessor is not None and node.predecessor.key == TEST_SEED
    assert node.predecessor == node == node.successor
    assert node.parent is None
    assert node.child is None

    assert (repr(node) == f'HeapNode ((value={TEST_SEED}, priority={TEST_PRIO}), successor=(value={TEST_SEED}, ' +
            f'priority={TEST_PRIO}), predecessor=(value={TEST_SEED}, priority={TEST_PRIO}), parent=None, child=None)')
    assert str(node) == f'(value={TEST_SEED}, priority={TEST_PRIO})'

    higher_priority_node = HeapNode(TEST_SEED, 2)
    lower_priority_node = HeapNode(TEST_SEED, 0)

    assert higher_priority_node > node > lower_priority_node


def test_adding_parent(heap_node: HeapNode) -> None:

    to_be_child = heap_node
    assert to_be_child.parent is None

    to_be_child.add_parent(TEST_SEED + 1, TEST_PRIO + 1)
    assert to_be_child.parent is not None and to_be_child.parent.key == TEST_SEED + 1

    to_be_new_parent = HeapNode(TEST_SEED + 2, TEST_PRIO + 2)
    to_be_child.change_parent(to_be_new_parent)
    assert to_be_child.parent == to_be_new_parent

    to_be_child.remove_parent()
    assert to_be_child.parent is None


def test_adding_child(heap_node: HeapNode) -> None:
    node = heap_node

    node.create_and_add_child(TEST_SEED + 1, TEST_PRIO + 1)
    assert node.child is not None and node.child.key == TEST_SEED + 1

    node.add_child(HeapNode(TEST_SEED + 2, TEST_PRIO + 2))
    assert node.child is not None and node.child.key == TEST_SEED + 1
    assert node.child.successor is not None and node.child.successor.key == TEST_SEED + 2
    assert node.child.successor == node.child.predecessor

    node.create_and_add_child(TEST_SEED + 3, TEST_PRIO + 3)
    assert node.child is not None and node.child.key == TEST_SEED + 1
    assert node.child.predecessor is not None and node.child.predecessor.key == TEST_SEED + 3
    assert node.child.predecessor.successor is not None and node.child.predecessor.successor == node.child
    assert node.degree == 3


def test_children_removal(heap_node: HeapNode) -> None:
    node = heap_node

    node.create_and_add_child(TEST_SEED + 1, TEST_PRIO + 1)
    node.remove_children_root()
    assert node.child is None
    assert node.degree == 0

    node.create_and_add_child(TEST_SEED + 1, TEST_PRIO + 1)
    node.create_and_add_child(TEST_SEED + 2, TEST_PRIO + 2)
    node.create_and_add_child(TEST_SEED + 3, TEST_PRIO + 3)

    node.remove_children_root()
    assert node.child is not None and node.child.key == TEST_SEED + 2
    assert node.child.predecessor is not None and node.child.predecessor.key == TEST_SEED + 3
    assert node.child.successor is not None and node.child.successor.key == TEST_SEED + 3
    assert node.degree == 2

    node.remove_children()
    assert node.degree == 0


def test_changing_children_root(heap_node: HeapNode) -> None:
    node = heap_node

    to_be_root = HeapNode(TEST_SEED + 1, TEST_PRIO + 1)
    node.change_children_root(to_be_root)
    assert node.child == to_be_root
    assert node.child.parent == node
    assert node.degree == 1

    to_be_new_root = HeapNode(TEST_SEED + 2, TEST_PRIO + 2)
    node.change_children_root(to_be_new_root)
    assert node.child == to_be_new_root
    assert node.child.parent == node
    assert node.child.predecessor == node.child.successor == to_be_new_root
    assert node.degree == 1

    node.create_and_add_child(TEST_SEED + 3, TEST_PRIO + 3)
    assert node.degree == 2
    to_be_last_new_root = HeapNode(TEST_SEED + 4, TEST_PRIO + 4)
    node.change_children_root(to_be_last_new_root)
    assert node.child == to_be_last_new_root
    assert node.child.parent == node
    assert node.child.predecessor.key == node.child.successor.key == TEST_SEED + 3
    assert node.degree == 2
