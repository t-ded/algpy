from __future__ import annotations

from typing import TypeVar, Generic, Optional

from algpy_src.base.constants import Comparable
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.trees.tree_node import TreeNode
from algpy_src.data_structures.linear.linked_list_node import LinkedListNode

_K = TypeVar('_K')
_V = TypeVar('_V', bound=Comparable)


class HeapNode(LinkedListNode, TreeNode[_K], Generic[_K, _V]):

    def __init__(self, key: _K, priority: _V) -> None:
        """
        Constructor of the HeapNode class.

        Parameters
        ----------
        key : _K
            Key to represent the node.
        priority : _V
            Numeric priority with respect to which the heap property is maintained.
        """
        LinkedListNode.__init__(self, key)
        TreeNode.__init__(self, key)

        self._priority: _V = priority
        self._degree: int = 0
        self._mark: bool = False

        self._parent: Optional[HeapNode] = None
        self._child: Optional[HeapNode] = None

        self._successor: HeapNode = self
        self._predecessor: HeapNode = self

    def __le__(self, other: HeapNode | NoNode) -> bool:
        if isinstance(other, NoNode):
            return True
        if not isinstance(other, HeapNode):
            raise NotImplementedError('Cannot compare HeapNode object with non-HeapNode object')
        return self._priority <= other._priority

    def __lt__(self, other: HeapNode | NoNode) -> bool:
        if isinstance(other, NoNode):
            return True
        if not isinstance(other, HeapNode):
            raise NotImplementedError('Cannot compare HeapNode object with non-HeapNode object')
        return self._priority < other._priority

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__} ({str(self)}, '
            f'successor={str(self._successor) if self._successor else None}, '
            f'predecessor={str(self._predecessor) if self._predecessor else None}, '
            f'parent={str(self._parent) if self._parent else None}, '
            f'child={str(self._child) if self._child else None})'
        )

    def __str__(self) -> str:
        return f'(value={self._value!r}, priority={self._priority})'

    @property
    def key(self) -> _K:
        return self._value

    @property
    def priority(self) -> _V:
        return self._priority

    @property
    def degree(self) -> int:
        return self._degree

    @property
    def mark(self) -> bool:
        return self._mark

    @property
    def parent(self) -> Optional[HeapNode]:
        return self._parent

    @property
    def child(self) -> Optional[HeapNode]:
        return self._child

    def change_priority(self, new_priority: _V) -> None:
        self._priority = new_priority

    def change_degree(self, new_degree: int) -> None:
        self._degree = new_degree

    def increment_degree(self) -> None:
        self._degree += 1

    def decrement_degree(self) -> None:
        self._degree -= 1

    def set_mark(self, mark: bool) -> None:
        self._mark = mark

    def create_and_add_child(self, key: _K, priority: _V) -> None:
        self.add_child(HeapNode(key, priority))

    def add_child(self, child: HeapNode) -> None:
        if self._child is None:
            self._child = child
            self._child.change_parent(self)
        else:
            current = self._child
            while current.successor != self._child:
                if current.successor is None:
                    raise IndexError('Fibonacci heap sibling layer is expected to be circular.')
                current = current.successor
            child.change_parent(self)
            child.change_successor(current.successor)
            child.change_predecessor(current)
            current.change_successor(child)
            self._child.change_predecessor(child)

        self.increment_degree()

    def change_children_root(self, new_child_root: HeapNode) -> None:
        new_child_root.change_parent(self)
        if self._degree == 0 or self._child is None:
            self._child = new_child_root
            self.change_degree(1)
        elif self._degree == 1 and self._child is not None:
            self._child = new_child_root
        elif self._degree > 1 and self._child is not None:
            new_child_root.change_successor(self._child.successor)
            if self._child.successor is not None:
                self._child.successor.change_predecessor(new_child_root)
            new_child_root.change_predecessor(self._child.predecessor)
            if self._child.predecessor is not None:
                self._child.predecessor.change_successor(new_child_root)
            self._child = new_child_root

    def remove_children_root(self) -> None:
        if self._child is not None and self._child != self._child.successor:
            if self._child.predecessor is None or self._child.successor is None:
                raise IndexError("Heap node's children root does not have predecessor or successor")
            self._child.predecessor.change_successor(self._child.successor)
            self._child.successor.change_predecessor(self._child.predecessor)
            self._child = self._child.successor
        else:
            self._child = None
        self.decrement_degree()

    def remove_child(self, child: HeapNode) -> None:
        child.remove_parent()
        if self._degree == 0 or self._child is None:
            return
        elif self._degree == 1 and self._child is not None:
            if self._child == child:
                self._child = None
                self.change_degree(0)
        else:
            current = self._child
            if current == child:
                self._child = current.successor
                if current.successor is not None:
                    current.successor.change_predecessor(current.predecessor)
                if current.predecessor is not None:
                    current.predecessor.change_successor(current.successor)
                self.decrement_degree()
            else:
                while current.successor != self._child:
                    if current.successor is None:
                        raise IndexError('Fibonacci heap sibling layer is expected to be circular.')
                    if current.successor == child:
                        current.change_successor(current.successor.successor)
                        if current.successor.successor is not None:
                            current.successor.successor.change_predecessor(current)
                        self.decrement_degree()
                    current = current.successor

    def remove_children(self) -> None:
        self._child = None
        self.change_degree(0)

    def add_parent(self, key: _K, priority: _V) -> None:
        self._parent = HeapNode(key, priority)
