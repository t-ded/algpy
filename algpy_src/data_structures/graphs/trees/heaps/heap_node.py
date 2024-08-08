from __future__ import annotations

from typing import TypeVar, Generic

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

        self._parent = None
        self._child = None

    def __le__(self, other: HeapNode) -> bool:
        return self._priority <= other._priority

    def __lt__(self, other: HeapNode) -> bool:
        return self._priority < other._priority

    @property
    def key(self) -> _K:
        return self.value

    @property
    def priority(self) -> _V:
        return self._priority
