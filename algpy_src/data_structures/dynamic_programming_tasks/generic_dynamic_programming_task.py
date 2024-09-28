from abc import abstractmethod
from typing import TypeVar, Generic, cast, Iterable, Callable, Optional

StateType = TypeVar('StateType')


class GenericDynamicProgrammingTask(Generic[StateType]):

    _EMPTY_STATE = object()

    def __init__(self) -> None:
        self._state: StateType = cast(StateType, self._EMPTY_STATE)

    @property
    def state(self) -> StateType:
        return self._state

    def set_state(self, state: StateType) -> None:
        self._state = state

    @abstractmethod
    def value_computation(self) -> tuple[Iterable[StateType], Callable]:
        raise NotImplementedError

    @abstractmethod
    def get_state_transitions(self) -> Optional[list[StateType]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_optimization(self) -> bool:
        raise NotImplementedError
