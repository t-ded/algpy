import logging
from typing import Optional, TypeVar, Literal, Iterator, cast

from algpy_src.base.constants import VERBOSITY_LEVELS
from algpy_src.data_structures.container import Container
from algpy_src.data_structures.linear.linked_list_node import LinkedListNode

T = TypeVar('T')


class LinkedList(Container):

    def __init__(self, linked_list_type: Literal['singly', 'doubly'] = 'singly') -> None:
        super().__init__()
        self._head: Optional[LinkedListNode] = None
        self.linked_list_type = linked_list_type
        if self.linked_list_type == 'doubly':
            self._tail: Optional[LinkedListNode] = None
        self._length: int = 0

    def __repr__(self) -> str:
        str_repr = ''
        if self._head is not None:
            str_repr += f'{self._head.value} (head)'
            current = self._head.successor
            while current is not None:
                str_repr += f' -> {current.value}'
                current = current.successor
        return str_repr

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[LinkedListNode]:
        node = self._head
        while node is not None:
            yield node
            node = node.successor

    @property
    def name(self) -> str:
        return self.linked_list_type.capitalize() + ' Linked List'

    @property
    def head(self) -> Optional[LinkedListNode]:
        return self._head

    @property
    def tail(self) -> Optional[LinkedListNode]:
        return self._tail

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

    def traverse(self, index: int, reset_n_ops: bool = False, verbosity_level: VERBOSITY_LEVELS = 0) -> Optional[LinkedListNode]:
        """
        Convenience method to traversing from head up to given index.
        If linked list is of type double, traverse from tail for cases when index is higher than half of length.

        Parameters
        ----------
        index : int
            Index to end at with head having index 0.
        reset_n_ops : bool (default False)
            Whether to reset self.n_ops to 0 at the beginning of the method run (False for convenience usage).
        verbosity_level : int (default 0)
            Select the amount of information to print throughout the traversal.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to printing the linked list and 2 meaning additionally print every element of traversal.

        Returns
        -------
        current : LinkedListNode | None
            None if linked list is empty or index is out of range, node at index otherwise.
        """
        if reset_n_ops is True:
            self.reset_n_ops()
        if verbosity_level > 0:
            print(self)
        current: Optional[LinkedListNode] = None
        if index > self._length:
            logging.warning('Index out of range.')
        else:
            if index < 0:
                index %= self._length
            if self.linked_list_type == 'singly' or index <= self._length / 2:
                current = self._head
                if current is not None:
                    for i in range(index):
                        if verbosity_level == 2:
                            print(current)
                        if current is not None and current.successor is not None:
                            current = current.successor
                            self.increment_n_ops()
            elif self.linked_list_type == 'doubly':
                current = self._tail
                if current is not None:
                    for i in range(self._length - index - 1):
                        if verbosity_level == 2:
                            print(current)
                        if current is not None and current.predecessor is not None:
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
        new_node: LinkedListNode = LinkedListNode(data)
        new_node.change_successor(self._head)
        if self.linked_list_type == 'doubly':
            if self._head is not None:
                self._head.change_predecessor(new_node)
                self.increment_n_ops()
        self._head = new_node
        self.increment_n_ops(2)
        self._length += 1

    def append(self, data: T) -> None:
        """
        Insert node with value 'data' at index -1 assuming length is more than 0.

        Parameters
        ----------
        data : Any
            Value for the node to hold.
        """
        if self._length == 0:
            self.insert_to_empty(data)
        else:
            new_node: LinkedListNode = LinkedListNode(data)
            tail = cast(LinkedListNode, self.traverse(self._length))
            tail.change_successor(new_node)
            self.increment_n_ops()
            if self.linked_list_type == 'doubly':
                new_node.change_predecessor(tail)
                self._tail = new_node
                self.increment_n_ops(2)
            self._length += 1

    def insert_to_empty(self, data: T) -> None:
        """
        Setup first node with value 'data' as head and also as tail in case of doubly linked list

        Parameters
        ----------
        data : Any
            Value for the node to hold.
        """
        new_node: LinkedListNode = LinkedListNode(data)
        self._head = new_node
        self.increment_n_ops()
        if self.linked_list_type == 'doubly':
            self._tail = new_node
            self.increment_n_ops()
        self._length += 1

    def insert(self, data: T, index: int, verbosity_level: VERBOSITY_LEVELS = 0) -> None:
        """
        Insert node with value 'data' at given index.

        Parameters
        ----------
        data : Any
            Value for the node to hold.
        index : int
            At what position to insert the node. Must be lower than or equal to self._length.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout the insertion.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to printing the linked list before and after insertion
            and 2 meaning additionally print every element of traversal.
        """
        self.reset_n_ops()
        if verbosity_level > 0:
            print(self)
        if index > self._length or (index < 0 and abs(index + 1) > self._length):
            logging.warning('Index out of range.')
        else:
            if self._head is None:
                self.insert_to_empty(data)
            else:
                if index < 0:
                    index += self._length + 1
                if index == 0:
                    self.prepend(data)
                elif index == self._length:
                    self.append(data)
                else:
                    preceding = self.traverse(index - 1, verbosity_level=2 if verbosity_level == 2 else 0)
                    if preceding is not None:
                        following = preceding.successor
                        if following is not None:
                            new_node: LinkedListNode = LinkedListNode(data)
                            new_node.change_successor(following)
                            preceding.change_successor(new_node)
                            if self.linked_list_type == 'doubly':
                                new_node.change_predecessor(preceding)
                                if following is not None:
                                    following.change_predecessor(new_node)
                                    self.increment_n_ops()
                                self.increment_n_ops()
                            self.increment_n_ops(2)
                            self._length += 1
        if verbosity_level > 0:
            print(self)

    def delete_head(self) -> None:
        """
        Delete the first node in the linked list (head).
        """
        if self._head is not None:
            if self._head.successor is not None:
                new_head = self._head.successor
                new_head.remove_predecessor()
                del self._head
                self._head = new_head
                self.increment_n_ops(4)
            else:
                self._head = None
                self.increment_n_ops()
            self._length -= 1

    def delete_last(self, preceding: LinkedListNode) -> None:
        """
        Delete the last node in the linked list (tail) given its predecessor.

        Parameters
        ----------
        preceding : LinkedListNode
            The node preceding to the node to be deleted (which is last in the linked list).
        """
        if preceding.successor is not None:
            if preceding.successor.successor is None:
                preceding.remove_successor()
                preceding.remove_successor()
                if self.linked_list_type == 'doubly':
                    self._tail = preceding
                    self.increment_n_ops()
                self.increment_n_ops(2)
                self._length -= 1

    def delete_middle(self, preceding: LinkedListNode) -> None:
        """
        Delete the node following input node assuming that such node is not the last in the linked list.

        Parameters
        ----------
        preceding : LinkedListNode
            The node preceding to the node to be deleted (which is not last in the linked list).
        """
        if preceding.successor is not None:
            if preceding.successor.successor is not None:
                following = preceding.successor.successor
                preceding.remove_successor()
                preceding.change_successor(following)
                if self.linked_list_type == 'doubly':
                    following.change_predecessor(preceding)
                    self.increment_n_ops()
                self.increment_n_ops(3)
                self._length -= 1

    def delete(self, data: T, index: Optional[int] = None, verbosity_level: VERBOSITY_LEVELS = 0) -> None:
        """
        Delete node with value 'data'.
        If index is passed, the element at given index has to hold value equal to 'data'. Otherwise, first entry with given value is deleted.

        Parameters
        ----------
        data : Any
            Value which the node to be deleted is holding.
        index : Optional[int] (default None)
            Index of the node to be deleted. Has to be lower than or equal to self._length.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout the deletion.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to printing the linked list before and after deletion
            and 2 meaning additionally print every element of traversal.
        """

        self.reset_n_ops()
        if verbosity_level > 0:
            print(self)
        if self._head is None:
            return
        if index is not None:
            if index >= self._length or (index < 0 and abs(index) > self._length):
                logging.warning('Index out of range.')
            else:
                if index < 0:
                    index += self._length
                if index == 0:
                    if self._head.value == data:
                        self.delete_head()
                    if self._length == 0:
                        self._tail = None
                else:
                    preceding = self.traverse(index - 1, verbosity_level=2 if verbosity_level == 2 else 0)
                    if preceding is not None and preceding.successor is not None and preceding.successor.value == data:
                        if preceding.successor.successor is None:
                            self.delete_last(preceding)
                        else:
                            self.delete_middle(preceding)

        else:
            current = self._head
            if current is not None:
                if current.value == data:
                    self.delete_head()
                    if verbosity_level > 0:
                        print(self)
                    if self._length == 0:
                        self._tail = None
                    return
                while current.successor is not None:
                    self.increment_n_ops()
                    if current.successor.value == data:
                        if current.successor.successor is None:
                            self.delete_last(current)
                        else:
                            self.delete_middle(current)
                        break

        if verbosity_level > 0:
            print(self)

    def search(self, data: T) -> Optional[int]:
        """
        Search for node with given value 'data'. Index of first occurrence (from the front) of such node is returned or None of it is not found.

        Parameters
        ----------
        data : Any
            Value to be held by the node.

        Returns
        -------
        location : Optional[int]
            Index of first occurrence of such node or None if it is not found.
        """
        self.reset_n_ops()
        location = None
        current = self._head
        if current is not None:
            for i in range(self._length):
                self.increment_n_ops()
                if current is not None and current.value == data:
                    return i
                if current is not None and current.successor is None:
                    break
                if current is not None:
                    current = current.successor

        return location
