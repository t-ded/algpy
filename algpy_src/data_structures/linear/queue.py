from typing import TypeVar, Generic, Optional

from algpy_src.data_structures.container import Container

T = TypeVar('T')


class Queue(Container, Generic[T]):

    def __init__(self) -> None:
        super().__init__()
        self.queue: list[T] = []

    @property
    def name(self) -> str:
        return 'Queue'

    @property
    def best_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_insert_description(self) -> str:
        return 'none - always constant'

    @property
    def average_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_insert_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_insert_description(self) -> str:
        return 'none - always constant'

    @property
    def best_case_delete_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_delete_description(self) -> str:
        return 'none - always constant'

    @property
    def average_case_delete_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_delete_time_complexity(self) -> str:
        return '1'

    @property
    def worst_case_delete_description(self) -> str:
        return 'none - always constant'

    @property
    def best_case_search_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_search_description(self) -> str:
        return 'item in the first position'

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

    @property
    def size(self) -> int:
        return len(self.queue)

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def peek(self) -> Optional[T]:
        """
        Returns the first element of the queue without removing it.

        Returns
        -------
        head : Optional[Any]
            Element from the beginning of the queue or None if the queue is empty.
        """
        if self.is_empty:
            return None
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

    def dequeue(self) -> T:
        """
        Remove element from the beginning of the queue.

        Returns
        -------
        head : Any
            Element from the beginning of the queue.
        """
        self.reset_n_ops()
        self.increment_n_ops()
        if self.is_empty:
            raise IndexError('The queue is empty')
        return self.queue.pop(0)
