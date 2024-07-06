from typing import TypeVar, Any

from algpy_src.data_structures.data_structure import DataStructure

T = TypeVar('T')


class Queue(DataStructure):

    def __init__(self):
        super().__init__()
        self.queue = []

    @property
    def space_complexity(self) -> str:
        return 'n'

    @property
    def name(self) -> str:
        return 'Queue'

    @property
    def size(self) -> int:
        return len(self.queue)

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def peek(self) -> Any:
        """
        Returns the first element of the queue without removing it.

        Returns
        -------
        head : Any
            Element from the beginning of the queue.
        """
        return self.queue[0]

    def enqueue(self, value: T) -> None:
        """
        Add element to the end of the queue.

        Parameters
        ----------
        value : Any
            Element to add to the queue
        """
        self.reset_n_ops()
        self.queue.append(value)
        self.increment_n_ops()

    def dequeue(self) -> Any:
        """
        Remove element from the beginning of the queue.

        Returns
        -------
        head : Any
            Element from the beginning of the queue.
        """
        self.reset_n_ops()
        self.increment_n_ops()
        return self.queue.pop(0)

    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information breakdown of the Queue data structure.
        """
        print('All basic queue operations are done in constant time')
