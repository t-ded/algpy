import pytest

from algpy_src.data_structures.graphs.trees.heaps.fibonacci_heap import FibonacciHeap


@pytest.fixture
def fib_heap() -> FibonacciHeap:
    return FibonacciHeap()


def test_fibonacci_heap_base(fib_heap: FibonacciHeap) -> None:
    assert fib_heap.name == 'Fibonacci Heap'
