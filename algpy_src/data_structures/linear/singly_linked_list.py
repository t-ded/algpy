from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, TypeVar

from algpy_src.data_structures.data_structure import DataStructure

T = TypeVar("T")


@dataclass
class LinkedListNode:

    def __init__(self, value: T):
        self.value: T = value
        self.successor: Optional[LinkedListNode] = None

    def add_successor(self, value: T) -> None:
        successor = LinkedListNode(value)
        self.successor = successor


class SinglyLinkedList(DataStructure):

    def __init__(self) -> None:
        super().__init__()
        self.head: Optional[LinkedListNode] = None
        self.length: int = 0

    @property
    def name(self) -> str:
        return 'Singly Linked List'

    @property
    def best_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_insert_description(self) -> str:
        return 'index 0'

    @property
    def average_case_insert_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_insert_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_insert_description(self) -> str:
        return 'index equals length'

    @property
    def best_case_delete_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_delete_description(self) -> str:
        return 'item in head'

    @property
    def average_case_delete_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_delete_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_delete_description(self) -> str:
        return 'item at tail'

    @property
    def best_case_search_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_search_description(self) -> str:
        return 'item in head'

    @property
    def average_case_search_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_search_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_search_description(self) -> str:
        return 'item not present'

    @property
    def space_complexity(self) -> str:
        return 'n'

    def traverse(self, index: int, reset_n_ops: bool = False) -> Optional[LinkedListNode]:
        """
        Convenience method to traversing from head up to given index.

        Parameters
        ----------
        index : int
            Index to end at with head having index 0.
        reset_n_ops : bool (default False)
            Whether to reset self.n_ops to 0 at the beginning of the method run (False for convenience usage).

        Returns
        -------
        current : Optional[LinkedListNode]
            None if linked list is empty or index is out of range, node at index otherwise.
        """
        if reset_n_ops is True:
            self.n_ops = 0
        current: Optional[LinkedListNode] = None
        if index > self.length:
            logging.warning('Index out of range.')
        else:
            current = self.head
            if current is not None:
                for i in range(index):
                    if current.successor is not None:
                        current = current.successor
                        self.increment_n_ops()
        return current

    def insert(self, data: T, index: int) -> None:
        """
        Insert node with value 'data' at given index.

        Parameters
        ----------
        data : Any
            Value for the node to hold.
        index : int
            At what position to insert the node. Must be lower than or equal to self.length.
        """
        self.n_ops = 0
        if index > self.length:
            logging.warning('Index out of range.')
        else:
            if self.head is None:
                self.head = LinkedListNode(data)
                self.length += 1
            else:
                preceding = self.traverse(index - 1)
                if preceding is not None:
                    preceding.add_successor(data)
                    self.length += 1

    def delete(self, data: T, index: Optional[int]) -> None:
        """
        Delete node with value 'data'.
        If index is passed, the element at given index has to hold value equal to 'data'. Otherwise, first entry with given value is deleted.

        Parameters
        ----------
        data : Any
            Value which the node to be deleted is holding.
        index : Optional[int]
            Index of the node to be deleted. Has to be lower than or equal to self.length.
        """

        self.n_ops = 0
        if self.head is None:
            return

        if index is not None:
            if index > self.length:
                logging.warning('Index out of range.')
            elif index == 0:
                if self.head.value == data:
                    self.head = self.head.successor
                    self.increment_n_ops()
                    self.length -= 1
            else:
                preceding = self.traverse(index - 1)
                if preceding is not None and preceding.successor is not None and preceding.successor.value == data:
                    preceding.successor = preceding.successor.successor
                    self.increment_n_ops()
                    self.length -= 1

        else:
            current = self.head
            if current is not None:
                while current.successor is not None:
                    self.increment_n_ops()
                    if current.successor.value == data:
                        current.successor = current.successor.successor
                        self.increment_n_ops()
                        self.length -= 1
                        break

    def search(self, data: T) -> Optional[int]:
        """
        Search for node with given value 'data'. Index of first occurrence of such node is returned or None of it is not found.

        Parameters
        ----------
        data : Any
            Value to be held by the node.

        Returns
        -------
        location : Optional[int]
            Index of first occurrence of such node or None if it is not found.
        """
        self.n_ops = 0
        location = None
        current = self.head
        if current is not None:
            for i in range(self.length):
                self.increment_n_ops()
                if current.value == data:
                    return i
                if current.successor is None:
                    break
                current = current.successor

        return location

    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information breakdown of Singly Linked List per insertion, deletion and search.
        """
        print(f'Time complexity breakdown of {self.name} data structure:')

        print(f'\tInsertion:')
        print(f'\t\tBest case time complexity is O({self.best_case_insert_time_complexity}) with best case being {self.best_case_insert_description}.')
        print(f'\t\tAverage case time complexity is O({self.average_case_insert_time_complexity}).')
        print(f'\t\tWorst case time complexity is O({self.worst_case_insert_time_complexity}) with worst case being {self.worst_case_insert_description}.')

        print(f'\tDeletion:')
        print(f'\t\tBest case time complexity is O({self.best_case_delete_time_complexity}) with best case being {self.best_case_delete_description}.')
        print(f'\t\tAverage case time complexity is O({self.average_case_delete_time_complexity}).')
        print(f'\t\tWorst case time complexity is O({self.worst_case_delete_time_complexity}) with worst case being {self.worst_case_delete_description}.')

        print(f'\tSearch:')
        print(f'\t\tBest case time complexity is O({self.best_case_search_time_complexity}) with best case being {self.best_case_search_description}.')
        print(f'\t\tAverage case time complexity is O({self.average_case_search_time_complexity}).')
        print(f'\t\tWorst case time complexity is O({self.worst_case_search_time_complexity}) with worst case being {self.worst_case_search_description}.')
