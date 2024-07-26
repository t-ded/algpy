from typing import TypeVar, Generic, Optional

from algpy_src.data_structures.container import Container

T = TypeVar('T')


class Stack(Container, Generic[T]):

    def __init__(self) -> None:
        super().__init__()
        self._stack: list[T] = []

    @property
    def name(self) -> str:
        return 'Stack'

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
        return 'item on top of the stack'

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
        return len(self._stack)

    @property
    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def peek(self) -> Optional[T]:
        """
        Returns the top element of the stack without removing it.

        Returns
        -------
        head : Optional[Any]
            Element from the beginning of the stack or None if the stack is empty.
        """
        if self.is_empty:
            return None
        return self._stack[-1]

    def push(self, value: T) -> None:
        """
        Add element to top of the stack.

        Parameters
        ----------
        value : Any
            Element to add to the stack
        """
        self.reset_n_ops()
        self._stack.append(value)
        self.increment_n_ops()

    def pop(self) -> T:
        """
        Remove element from the top of the stack.

        Returns
        -------
        top : Any
            Element from the top of the stack.
        """
        self.reset_n_ops()
        self.increment_n_ops()
        if self.is_empty:
            raise IndexError('The stack is empty')
        return self._stack.pop(-1)
