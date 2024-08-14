import pytest

from algpy_src.base.constants import TEST_SEED
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.trees.heaps.fibonacci_heap import FibonacciHeap
from algpy_src.data_structures.graphs.trees.heaps.heap_node import HeapNode

TEST_PRIORITY = 10


@pytest.fixture
def fib_heap() -> FibonacciHeap:
    return FibonacciHeap()


@pytest.fixture
def complex_fib_heap() -> FibonacciHeap:
    fh: FibonacciHeap[int, int] = FibonacciHeap()

    # Left branch
    node_35: HeapNode[int, int] = HeapNode(35, 35)
    node_46: HeapNode[int, int] = HeapNode(46, 46)
    node_26: HeapNode[int, int] = HeapNode(26, 26)
    node_26.add_child(node_35)
    node_24: HeapNode[int, int] = HeapNode(24, 24)
    node_24.add_child(node_26)
    node_24.add_child(node_46)

    node_30: HeapNode[int, int] = HeapNode(30, 30)
    node_17: HeapNode[int, int] = HeapNode(17, 17)
    node_17.add_child(node_30)

    node_23: HeapNode[int, int] = HeapNode(23, 23)

    root_7: HeapNode[int, int] = HeapNode(7, 7)
    root_7.add_child(node_24)
    root_7.add_child(node_17)
    root_7.add_child(node_23)

    # Middle branch
    node_52: HeapNode[int, int] = HeapNode(52, 52)
    node_21: HeapNode[int, int] = HeapNode(21, 21)
    node_21.add_child(node_52)

    node_39: HeapNode[int, int] = HeapNode(39, 39)

    root_18: HeapNode[int, int] = HeapNode(18, 18)
    root_18.add_child(node_21)
    root_18.add_child(node_39)

    # Right branch
    node_41: HeapNode[int, int] = HeapNode(41, 41)
    root_38: HeapNode[int, int] = HeapNode(38, 38)
    root_38.add_child(node_41)

    # Fib heap
    fh.insert_node(root_7)
    fh.insert_node(root_18)
    fh.insert_node(root_38)

    return fh


def test_fibonacci_heap_base(fib_heap: FibonacciHeap) -> None:
    assert fib_heap.name == 'Fibonacci Heap'
    assert fib_heap.space_complexity == 'n'

    assert fib_heap.best_case_insert_time_complexity == '1'
    assert fib_heap.best_case_insert_description == 'same for all insert operations'
    assert fib_heap.average_case_insert_time_complexity == '1'
    assert fib_heap.worst_case_insert_time_complexity == '1'
    assert fib_heap.worst_case_insert_description == 'same for all insert operations'

    assert fib_heap.best_case_search_time_complexity == '1'
    assert fib_heap.best_case_search_description == 'search min'
    assert fib_heap.average_case_search_time_complexity == 'log(n)'
    assert fib_heap.worst_case_search_time_complexity == 'n'
    assert fib_heap.worst_case_search_description == 'search for item not present in degenerate heap'

    assert fib_heap.best_case_delete_time_complexity == 'log(n)'
    assert fib_heap.best_case_delete_description == 'delete min'
    assert fib_heap.average_case_delete_time_complexity == 'log(n)'
    assert fib_heap.worst_case_delete_time_complexity == 'n'
    assert fib_heap.worst_case_delete_description == 'delete min after n single item insertions'


def test_insertion(fib_heap: FibonacciHeap) -> None:

    for i in range(5):
        inserted_node = fib_heap.insert(TEST_SEED - i, TEST_PRIORITY - i)
        assert inserted_node.predecessor is not None
        assert inserted_node.successor is not None
        assert inserted_node.parent is None

    min_node = fib_heap.get_min_node()
    assert not isinstance(min_node, NoNode) and min_node.key == TEST_SEED - 4
    assert min_node.predecessor is not None and not isinstance(min_node.predecessor, NoNode) and min_node.predecessor > min_node
    assert min_node.successor is not None and not isinstance(min_node.successor, NoNode) and min_node.successor > min_node
    assert len(fib_heap) == 5


def test_min_node_extraction_one_node(fib_heap: FibonacciHeap) -> None:

    assert fib_heap.extract_min_node() == NoNode()
    for i in range(5):
        inserted_node = fib_heap.insert(TEST_SEED - i, TEST_PRIORITY - 1)
        assert inserted_node == fib_heap.extract_min_node()
        assert len(fib_heap) == 0


def test_min_node_extraction_nodes_in_root_list(fib_heap: FibonacciHeap) -> None:

    for i in range(5):
        fib_heap.insert(TEST_SEED - i, TEST_PRIORITY - i)

    min_node = fib_heap.extract_min_node()
    assert not isinstance(min_node, NoNode) and min_node.key == TEST_SEED - 4

    new_min_node = fib_heap.get_min_node()
    assert not isinstance(new_min_node, NoNode) and new_min_node.key == TEST_SEED - 3
    assert len(fib_heap) == 4
