from functools import cached_property
from typing import Optional, Generic, TypeVar


StateType = TypeVar('StateType')
CandidateType = TypeVar('CandidateType')
OptionType = TypeVar('OptionType')


class GenericBacktrackingTask(Generic[StateType, CandidateType, OptionType]):

    def __init__(self) -> None:
        self._state: Optional[StateType] = None

    @property
    def state(self) -> Optional[StateType]:
        return self._state

    @cached_property
    def get_candidates(self) -> list[CandidateType]:
        raise NotImplementedError

    @cached_property
    def get_options(self) -> list[OptionType]:
        raise NotImplementedError

    @property
    def default_option(self) -> OptionType:
        raise NotImplementedError

    def is_option_allowed(self, candidate: CandidateType, option: OptionType) -> bool:
        raise NotImplementedError

    def apply_option(self, candidate: CandidateType, option: OptionType) -> None:
        raise NotImplementedError

    def is_solved(self) -> bool:
        raise NotImplementedError
