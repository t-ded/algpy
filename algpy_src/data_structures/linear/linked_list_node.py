from __future__ import annotations

from typing import TypeVar, Optional

T = TypeVar('T')


class LinkedListNode:

    def __init__(self, value: T):
        self.value: T = value
        self.successor: Optional[LinkedListNode] = None
        self.predecessor: Optional[LinkedListNode] = None

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def add_successor(self, value: T) -> None:
        self.successor = LinkedListNode(value)

    def change_successor(self, new_successor: Optional[LinkedListNode]) -> None:
        self.successor = new_successor

    def add_predecessor(self, value: T) -> None:
        self.predecessor = LinkedListNode(value)

    def change_predecessor(self, new_predecessor: Optional[LinkedListNode]) -> None:
        self.predecessor = new_predecessor
        