from typing import Literal, Protocol, TypeVar

COMPLEXITIES = Literal['both', 'time', 'space']
TEST_SEED = 42
VERBOSITY_LEVELS = Literal[0, 1, 2]

T = TypeVar('T')


class Comparable(Protocol):
    def __lt__(self: T, other: T) -> bool: ...
    def __eq__(self, other: T) -> bool: ...


class PrintableComparable(Comparable, Protocol):
    def __repr__(self) -> str: ...
