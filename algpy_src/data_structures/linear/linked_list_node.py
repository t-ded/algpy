from __future__ import annotations

from typing import TypeVar, Optional, Generic

T = TypeVar('T')


class LinkedListNode(Generic[T]):

    def __init__(self, value: T):
        self._value: T = value
        self._successor: Optional[LinkedListNode] = None
        self._predecessor: Optional[LinkedListNode] = None

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__} (value={self._value!r}, '
            f'successor={self._successor._value if self._successor else None}, '
            f'predecessor={self._predecessor._value if self._predecessor else None})'
        )

    def __str__(self) -> str:
        return str(self._value)

    @property
    def value(self) -> T:
        return self._value

    @property
    def predecessor(self) -> Optional[LinkedListNode]:
        return self._predecessor

    @property
    def successor(self) -> Optional[LinkedListNode]:
        return self._successor

    def add_successor(self, value: T) -> None:
        self._successor = LinkedListNode(value)

    def change_successor(self, new_successor: Optional[LinkedListNode]) -> None:
        self._successor = new_successor

    def remove_successor(self) -> None:
        del self._successor
        self._successor = None

    def add_predecessor(self, value: T) -> None:
        self._predecessor = LinkedListNode(value)

    def change_predecessor(self, new_predecessor: Optional[LinkedListNode]) -> None:
        self._predecessor = new_predecessor

    def remove_predecessor(self) -> None:
        del self._predecessor
        self._predecessor = None
