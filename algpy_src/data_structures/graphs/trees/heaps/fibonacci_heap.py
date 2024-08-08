from __future__ import annotations

from typing import TypeVar, Generic, cast

from algpy_src.base.constants import Comparable
from algpy_src.data_structures.container import Container
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.trees.heaps.heap_node import HeapNode

_K = TypeVar('_K')
_V = TypeVar('_V', bound=Comparable)


class FibonacciHeap(Container, Generic[_K, _V]):
    """
    Fibonacci heap container data structure implementation.
    The heap property is maintained with respect to priority arguments.
    """

    def __init__(self) -> None:
        super().__init__()
        self._num_nodes: int = 0
        self._min_root: HeapNode | NoNode = NoNode()
        self._root_list_root: HeapNode | NoNode = NoNode()

    @property
    def name(self) -> str:
        return 'Fibonacci Heap'

    @property
    def space_complexity(self) -> str:
        return 'n'

    @property
    def best_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_insert_description(self) -> str:
        return 'same for all insert operations'

    @property
    def average_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_insert_description(self) -> str:
        return 'same for all insert operations'

    @property
    def best_case_delete_time_complexity(self) -> str:
        return 'log(n)'

    @property
    def best_case_delete_description(self) -> str:
        return 'delete min'

    @property
    def average_case_delete_time_complexity(self) -> str:
        return 'log(n)'

    @property
    def worst_case_delete_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_delete_description(self) -> str:
        return 'delete min after n single item insertions'

    @property
    def best_case_search_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_search_description(self) -> str:
        return 'search min'

    @property
    def average_case_search_time_complexity(self) -> str:
        return 'log(n)'

    @property
    def worst_case_search_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_search_description(self) -> str:
        return 'search for item not present in degenerate heap'

    def insert(self, key: _K, priority: _V) -> HeapNode:
        """
        Insert a given key associated with a comparable priority used to maintain the heap property of the keys.

        Parameters
        ----------
        key : _K
            Key to insert.
        priority : _V
            Value to associate the key with. Used to compare the keys and maintain the heap property.

        Returns
        ----------
        heap_node : HeapNode
            The inserted heap node.
        """
        heap_node = HeapNode(key, priority)
        heap_node.change_successor(heap_node)
        heap_node.change_predecessor(heap_node)
        self._merge_with_root_list(heap_node)
        self._num_nodes += 1

        if self._min_root == NoNode() or heap_node.priority < cast(HeapNode, self._min_root).priority:
            self._min_root = heap_node
        return heap_node

    def _merge_with_root_list(self, node: HeapNode) -> None:
        """
        Convenience function that merges the given node with the root list.

        Parameters
        ----------
        node : HeapNode
            Heap node to merge with the root list.
        """
        if isinstance(self._root_list_root, NoNode):
            self._root_list_root = node
        else:
            node.change_successor(self._root_list_root)
            node.change_predecessor(self._root_list_root)
            self._root_list_root.change_successor(node)
            self._root_list_root.change_predecessor(node)

    def _union(self, other: FibonacciHeap) -> FibonacciHeap:
        """
        Create a union of two Fibonacci heaps.

        Parameters
        ----------
        other : FibonacciHeap
            The second heap to make a union of this one with.

        Returns
        -------
        merged_heap : FibonacciHeap
            The new Fibonacci heap following the union operation.
        """
        new_heap: FibonacciHeap = FibonacciHeap()
        new_heap._root_list_root = self._root_list_root
        if isinstance(self._min_root, NoNode):
            new_heap._min_root = other._min_root
            return new_heap
        elif isinstance(other._min_root, NoNode):
            new_heap._min_root = self._min_root
            return new_heap
        else:
            new_heap._min_root = min(self._min_root, other._min_root)

        assert not isinstance(other._root_list_root, NoNode)
        assert not isinstance(new_heap._root_list_root, NoNode)
        other._root_list_root.change_predecessor(new_heap._root_list_root.predecessor)
        if new_heap._root_list_root.predecessor is not None:
            new_heap._root_list_root.predecessor.change_successor(other._root_list_root)
        new_heap._root_list_root.change_predecessor(other._root_list_root.predecessor)
        if new_heap._root_list_root.predecessor is not None:
            new_heap._root_list_root.predecessor.change_successor(new_heap._root_list_root)

        new_heap._num_nodes = self._num_nodes + other._num_nodes

        return new_heap

    def get_min_node(self) -> HeapNode | NoNode:
        """
        Peek node associated with the minimum priority.

        Returns
        -------
        min_priority_node : HeapNode | NoNode
            The heap node associated with the minimum priority or NoNode() object if the heap is empty.
        """
        return self._min_root

    def extract_min_node(self) -> HeapNode | NoNode:
        """
        Extract node associated with the minimum priority.

        Returns
        -------
        min_priority_node : HeapNode | NoNode
            The heap node associated with the minimum priority or NoNode() object if the heap is empty.
        """
        raise NotImplementedError
