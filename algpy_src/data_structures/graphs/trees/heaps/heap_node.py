from __future__ import annotations

from typing import TypeVar, Generic, Optional

from algpy_src.base.constants import Comparable
from algpy_src.data_structures.linear.linked_list_node import LinkedListNode

_K = TypeVar('_K')
_V = TypeVar('_V', bound=Comparable)


class HeapNode(LinkedListNode, Generic[_K, _V]):

    def __init__(self, key: _K, priority: _V):
        """
        Constructor of the HeapNode class.

        Parameters
        ----------
        key : _K
            Key to represent the node.
        priority : _V
            Numeric priority with respect to which the heap property is maintained.
        """
        super().__init__(key)

        self._priority: _V = priority
        self._degree: int = 0
        self._mark: bool = False

        self._parent: Optional[HeapNode] = None
        self._child: Optional[HeapNode] = None

        self._successor: HeapNode = self
        self._predecessor: HeapNode = self

    def __le__(self, other: HeapNode) -> bool:
        if not isinstance(other, HeapNode):
            raise NotImplementedError('Cannot compare HeapNode object with non-HeapNode object')
        return self._priority <= other._priority

    def __lt__(self, other: HeapNode) -> bool:
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
    def parent(self) -> Optional[HeapNode]:
        return self._parent

    @property
    def child(self) -> Optional[HeapNode]:
        return self._child

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

        self._degree += 1

    def change_children_root(self, new_child_root: HeapNode) -> None:
        new_child_root.change_parent(self)
        if self._degree == 0 or self._child is None:
            self._child = new_child_root
            self._degree = 1
        elif self._degree == 1 and self._child is not None:
            del self._child
            self._child = new_child_root
        elif self._degree > 1 and self._child is not None:
            new_child_root.change_successor(self._child.successor)
            if self._child.successor is not None:
                self._child.successor.change_predecessor(new_child_root)
            new_child_root.change_predecessor(self._child.predecessor)
            if self._child.predecessor is not None:
                self._child.predecessor.change_successor(new_child_root)
            del self._child
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
        self._degree = max(0, self._degree - 1)

    def remove_children(self) -> None:
        self._child = None
        self._degree = 0

    def add_parent(self, key: _K, priority: _V) -> None:
        self._parent = HeapNode(key, priority)

    def change_parent(self, new_parent: Optional[HeapNode]) -> None:
        del self._parent
        self._parent = new_parent

    def remove_parent(self) -> None:
        del self._parent
        self._parent = None
