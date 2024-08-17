from __future__ import annotations

import math
from typing import TypeVar, Generic, Iterator

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

    def __len__(self) -> int:
        return self._num_nodes

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

    @property
    def is_empty(self) -> bool:
        return self._num_nodes == 0

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
        return self.insert_node(heap_node)

    def insert_node(self, node: HeapNode) -> HeapNode:
        """
        Insert the given HeapNode object to the heap.

        Parameters
        ----------
        node : HeapNode
            The heap node to be inserted.

        Returns
        ----------
        heap_node : HeapNode
            The inserted heap node.
        """
        self._merge_with_root_list(node)
        self._num_nodes += 1

        if node < self._min_root:
            self._min_root = node
        return node

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
            if self._root_list_root.predecessor is None:
                raise ValueError('Fibonacci heap sibling layer is expected to be circular.')
            tail = self._root_list_root.predecessor
            node.change_successor(self._root_list_root)
            node.change_predecessor(tail)
            self._root_list_root.change_predecessor(node)
            tail.change_successor(node)
            if node.parent is not None:
                node.parent.remove_child(node)
                node.remove_parent()


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
        min_node: HeapNode | NoNode = self._min_root
        if not isinstance(min_node, NoNode):

            if min_node.child is not None:
                children = list(self._get_siblings(min_node.child))
                for child in children:
                    self._merge_with_root_list(child)
                    child.remove_parent()

            min_node.remove_children()
            self._remove_from_root_list(min_node)
            self._consolidate()

        return min_node

    def _get_siblings(self, node: HeapNode) -> Iterator[HeapNode]:
        """
        Convenience method to recursively iterate over successor of the given node, its successor and so on.

        Parameters
        ----------
        node : HeapNode
            Root node to start the iteration from (and end the iteration at, non-inclusively)

        Returns
        -------
        layer : Iterator[HeapNode]
            Generator of one layer of siblings starting with the given root node.
        """
        it_len = 0
        current: HeapNode = node
        while True:
            yield current
            it_len += 1
            if current.successor is None or it_len > self._num_nodes:
                raise ValueError('Fibonacci heap sibling layer is expected to be circular.')
            if current.successor == node:
                break
            current = current.successor

    def _remove_from_root_list(self, node: HeapNode) -> None:
        """
        Convenience method to remove the given node from the root list.

        Parameters
        ----------
        node : HeapNode
            The node in the root list to be removed.
        """
        root_list = list(self._get_siblings(node))

        if len(root_list) == 1:
            if node != self._root_list_root or node != self._min_root:
                raise AttributeError('Root list of Fibonacci heap contains one node but attempting to remove node that is not equal to main root or min root.')
            self._root_list_root = NoNode()
            self._min_root = NoNode()

        elif len(root_list) > 1:
            if node.predecessor is None or node.successor is None:
                raise ValueError('Fibonacci heap sibling layer is expected to be circular.')
            if node == self._root_list_root:
                self._root_list_root = node.successor
            if node == self._min_root:
                self._min_root = min(root for root in root_list if root != node)

            node.predecessor.change_successor(node.successor)
            node.successor.change_predecessor(node.predecessor)

        node.change_predecessor(node)
        node.change_successor(node)
        self._num_nodes -= 1

    def _consolidate(self) -> None:
        """
        Consolidate the heap following an extract min operation to reduce the number of unique roots
        in the root list and make node degrees as unique as possible.
        """
        if isinstance(self._root_list_root, NoNode):
            return

        degree_table: list[HeapNode | None] = [None] * (math.ceil(math.log(self._num_nodes, 2)) + 1)
        root_list_layer: list[HeapNode] = list(self._get_siblings(self._root_list_root))

        for i in range(len(root_list_layer)):
            root = root_list_layer[i]
            deg = root.degree
            while (node_with_deg := degree_table[deg]) is not None:
                if node_with_deg < root:
                    root, node_with_deg = node_with_deg, root
                self._heap_link(node_with_deg, root)
                degree_table[deg] = None
                deg += 1
            degree_table[deg] = root

        self._min_root = min(node for node in degree_table if node is not None)

    def _heap_link(self, to_be_child: HeapNode, to_be_parent: HeapNode) -> None:
        """
        Re-link two nodes from the root layer in a way that one of them is child of another.

        Parameters
        ----------
        to_be_child : HeapNode
            The new child of the other given node.
        to_be_parent : HeapNode
            The new parent of the other given node.
        """
        self._remove_from_root_list(to_be_child)
        self._num_nodes += 1
        to_be_child.set_mark(False)
        to_be_parent.add_child(to_be_child)

    def find(self, key: _K) -> HeapNode | NoNode:
        """
        Find node with the given key from the root list.

        Parameters
        ----------
        key : _K
            Searched-for key.

        Returns
        -------
        node : HeapNode | NoNode
            Returns node with the given key or NoNode() object in case such node is not present.
        """
        if isinstance(self._root_list_root, NoNode):
            return NoNode()

        for root in self._get_siblings(self._root_list_root):
            result = self._find_recursive(root, key)
            if not isinstance(result, NoNode):
                return result

        return NoNode()

    def _find_recursive(self, node: HeapNode, key: _K) -> HeapNode | NoNode:
        """
        Convenience method to recursively traverse node's children trying to find the given key.

        Parameters
        ----------
        node : HeapNode
            Root to start the traversal from.
        key : _K
            Key to look for.

        Returns
        -------
        found : HeapNode | NoNode
            NoNode() object if given key not found in the subtree formed by given node, otherwise the HeapNode() object holding that key.
        """
        if node.key == key:
            return node
        if node.child is not None:
            for child in self._get_siblings(node.child):
                result = self._find_recursive(child, key)
                if not isinstance(result, NoNode):
                    return result
        return NoNode()

    def decrease_priority(self, node: HeapNode, new_priority: int | float) -> None:
        """
        Change priority of the given node and consolidate the heap in a way that the heap property is maintained.

        Parameters
        ----------
        node : HeapNode
            Node whose priority is to be decreased.
        new_priority : int | float
            New priority for the given node.
        """
        if new_priority > node.priority:
            return
        node.change_priority(new_priority)

        parent = node.parent
        if parent is not None and node < parent:
            self._cut(node, parent)
            self._cascading_cut(parent)
        if node < self._min_root:
            self._min_root = node

    def _cut(self, node: HeapNode, parent: HeapNode) -> None:
        """
        Cut node from its parent and move it to the root list.

        Parameters
        ----------
        node : HeapNode
            Child node to cut.
        parent : HeapNode
            Parent node to cut from.
        """
        parent.remove_child(node)
        node.set_mark(False)
        self._merge_with_root_list(node)

    def _cascading_cut(self, node: HeapNode) -> None:
        """
        Cut given node's parents in cascade.

        Parameters
        ----------
        node : HeapNode
            Node whose parent to start the cascade from
        """
        parent = node.parent
        if parent is not None:
            if node.mark is False:
                node.set_mark(True)
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)
