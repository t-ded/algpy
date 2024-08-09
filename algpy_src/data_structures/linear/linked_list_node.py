from __future__ import annotations

from typing import TypeVar, Optional, Generic, Type

T = TypeVar('T')
LLN = TypeVar('LLN', bound='LinkedListNode')


class LinkedListNode(Generic[T, LLN]):

    def __init__(self, value: T):
        self._value: T = value
        self._successor: Optional[LLN] = None
        self._predecessor: Optional[LLN] = None

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__} (value={self._value!r}, '
            f'successor={self._successor._value if self._successor else None}, '
            f'predecessor={self._predecessor._value if self._predecessor else None})'
        )

    def __str__(self) -> str:
        return str(self._value)

    @classmethod
    def new_node(cls: Type[LLN], value: T) -> LLN:
        return cls(value)

    @property
    def value(self) -> T:
        return self._value

    @property
    def predecessor(self) -> Optional[LLN]:
        return self._predecessor

    @property
    def successor(self) -> Optional[LLN]:
        return self._successor

    def add_successor(self, value: T) -> None:
        self._successor = self.new_node(value)

    def change_successor(self, new_successor: Optional[LLN]) -> None:
        del self._successor
        self._successor = new_successor

    def remove_successor(self) -> None:
        del self._successor
        self._successor = None

    def add_predecessor(self, value: T) -> None:
        self._predecessor = self.new_node(value)

    def change_predecessor(self, new_predecessor: Optional[LLN]) -> None:
        del self._predecessor
        self._predecessor = new_predecessor

    def remove_predecessor(self) -> None:
        del self._predecessor
        self._predecessor = None
