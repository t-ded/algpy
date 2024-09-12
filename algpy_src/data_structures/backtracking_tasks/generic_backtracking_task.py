from abc import abstractmethod
from functools import cached_property
from typing import Generic, TypeVar, cast

StateType = TypeVar('StateType')
CandidateType = TypeVar('CandidateType')
OptionType = TypeVar('OptionType')


class GenericBacktrackingTask(Generic[StateType, CandidateType, OptionType]):

    _EMPTY_STATE = object()

    def __init__(self) -> None:
        self._state: StateType = cast(StateType, self._EMPTY_STATE)

    @property
    def state(self) -> StateType:
        return self._state

    @cached_property
    @abstractmethod
    def get_candidates(self) -> list[CandidateType]:
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def get_options(self) -> list[OptionType]:
        raise NotImplementedError

    @property
    @abstractmethod
    def default_option(self) -> OptionType:
        raise NotImplementedError

    @abstractmethod
    def reset_candidate_to_initial_state(self, candidate: CandidateType) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_option_allowed(self, candidate: CandidateType, option: OptionType) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply_option(self, candidate: CandidateType, option: OptionType) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_solved(self) -> bool:
        raise NotImplementedError
