from functools import cached_property
from typing import Optional, Generic, TypeVar


T = TypeVar('T')
O = TypeVar('O')


class GenericBacktrackingTask(Generic[T, O]):

    def __init__(self) -> None:
        self._state: Optional[T] = None

    @property
    def state(self) -> Optional[T]:
        return self._state

    @cached_property
    def get_options(self) -> list[O]:
        raise NotImplementedError

    def is_option_allowed(self, option: O) -> bool:
        raise NotImplementedError

    def apply_option(self, option: O) -> None:
        raise NotImplementedError

    def is_solved(self) -> bool:
        raise NotImplementedError
