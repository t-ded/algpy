import logging
from typing import Optional, TypeVar, Literal

from algpy_src.data_structures.data_structure import DataStructure
from algpy_src.data_structures.linear.linked_list_node import LinkedListNode

T = TypeVar('T')


class LinkedList(DataStructure):

    def __init__(self, linked_list_type: Literal['singly', 'doubly'] = 'singly') -> None:
        super().__init__()
        self.head: Optional[LinkedListNode] = None
        self.linked_list_type = linked_list_type
        if self.linked_list_type == 'doubly':
            self.tail: Optional[LinkedListNode] = None
        self.length: int = 0

    @property
    def name(self) -> str:
        return self.linked_list_type.capitalize() + ' Linked List'

    @property
    def best_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_insert_description(self) -> str:
        if self.linked_list_type == 'singly':
            return 'index 0'
        return 'index 0 or index -1'

    @property
    def average_case_insert_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_insert_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_insert_description(self) -> str:
        if self.linked_list_type == 'singly':
            return 'index equals length'
        return 'index equals half of length'

    @property
    def best_case_delete_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_delete_description(self) -> str:
        if self.linked_list_type == 'singly':
            return 'item in head'
        return 'item in head or index -1'

    @property
    def average_case_delete_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_delete_time_complexity(self) -> str:
        return 'n'

    @property
    def worst_case_delete_description(self) -> str:
        if self.linked_list_type == 'singly':
            return 'item at tail'
        return 'item at tail if index not provided, otherwise item in the middle'

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

    # TODO: add index % self.length and index = self.length + index for cases when index < 0
    def traverse(self, index: int, reset_n_ops: bool = False) -> Optional[LinkedListNode]:
        """
        Convenience method to traversing from head up to given index.
        If linked list is of type double, traverse from tail for cases when index is higher than half of length.

        Parameters
        ----------
        index : int
            Index to end at with head having index 0.
        reset_n_ops : bool (default False)
            Whether to reset self.n_ops to 0 at the beginning of the method run (False for convenience usage).

        Returns
        -------
        current : LinkedListNode | None
            None if linked list is empty or index is out of range, node at index otherwise.
        """
        if reset_n_ops is True:
            self.n_ops = 0
        current: Optional[LinkedListNode] = None
        if index > self.length:
            logging.warning('Index out of range.')
        else:
            if self.linked_list_type == 'singly' or index <= self.length / 2:
                current = self.head
                if current is not None:
                    for i in range(index):
                        if current.successor is not None:
                            current = current.successor
                            self.increment_n_ops()
            elif self.linked_list_type == 'doubly':
                current = self.tail
                if current is not None:
                    for i in range(self.length - index):
                        if current.predecessor is not None:
                            current = current.predecessor
                            self.increment_n_ops()
        return current

    def prepend(self, data: T) -> None:
        """
        Insert node with value 'data' at index 0 assuming length is more than 0.

        Parameters
        ----------
        data : Any
            Value for the node to hold.
        """
        new_node = LinkedListNode(data)
        new_node.change_successor(self.head)
        if self.linked_list_type == 'doubly':
            if self.head is not None:
                self.head.change_predecessor(new_node)
                self.increment_n_ops()
        self.head = new_node
        self.increment_n_ops(2)

    def append(self, data: T) -> None:
        """
        Insert node with value 'data' at index -1 assuming length is more than 0.

        Parameters
        ----------
        data : Any
            Value for the node to hold.
        """
        new_node = LinkedListNode(data)
        tail = self.traverse(self.length)
        if tail is not None:
            tail.change_successor(new_node)
            self.increment_n_ops()
        if self.linked_list_type == 'doubly':
            new_node.change_predecessor(tail)
            self.tail = new_node
            self.increment_n_ops(2)

    def setup_first_node(self, data: T) -> None:
        """
        Setup first node with value 'data' as head and also as tail in case of doubly linked list

        Parameters
        ----------
        data : Any
            Value for the node to hold.
        """
        new_node = LinkedListNode(data)
        self.head = new_node
        self.increment_n_ops()
        if self.linked_list_type == 'doubly':
            self.tail = new_node
            self.increment_n_ops()

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
                self.setup_first_node(data)
            else:
                if index == 0:
                    self.prepend(data)
                elif index == self.length:
                    self.append(data)
                else:
                    preceding = self.traverse(index - 1)
                    if preceding is not None:
                        following = preceding.successor
                        new_node = LinkedListNode(data)
                        new_node.change_successor(following)
                        preceding.change_successor(new_node)
                        if self.linked_list_type == 'doubly':
                            new_node.change_predecessor(preceding)
                            if following is not None:
                                following.change_predecessor(new_node)
                                self.increment_n_ops()
                            self.increment_n_ops()
                        self.increment_n_ops(2)
            self.length += 1

    # TODO: Factor in doubly linked listed type
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
                    preceding.change_successor(preceding.successor.successor)
                    self.increment_n_ops()
                    self.length -= 1

        else:
            current = self.head
            if current is not None:
                if current.value == data:
                    self.head = current.successor
                    self.increment_n_ops()
                    self.length -= 1
                    return
                while current.successor is not None:
                    self.increment_n_ops()
                    if current.successor.value == data:
                        current.change_successor(current.successor.successor)
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
        Print the time complexity information breakdown of given Linked List per insertion, deletion and search.
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
