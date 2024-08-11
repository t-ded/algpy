import pytest

from algpy_src.base.constants import TEST_SEED
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.trees.heaps.fibonacci_heap import FibonacciHeap

TEST_PRIORITY = 10


@pytest.fixture
def fib_heap() -> FibonacciHeap:
    return FibonacciHeap()


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
