from collections import namedtuple
from typing import Literal, Protocol, TypeVar

T = TypeVar('T')


class Comparable(Protocol):
    def __lt__(self: T, other: T) -> bool: ...

    def __eq__(self, other: T) -> bool: ...


class PrintableComparable(Comparable, Protocol):
    def __repr__(self) -> str: ...


COMPLEXITIES = Literal['both', 'time', 'space']
METRICS_TO_PLOT = Literal['both', 'time', 'n_ops']
TEST_SEED = 42
VERBOSITY_LEVELS = Literal[0, 1, 2]

ProblemInstance = TypeVar('ProblemInstance')
InputSize = TypeVar('InputSize', bound=PrintableComparable)
GraphSize = namedtuple('GraphSize', 'nodes edges', defaults=[0, 0])

G = TypeVar('G')
Node = TypeVar('Node')
EdgeData = TypeVar('EdgeData')
SingleEdgeData = TypeVar('SingleEdgeData')
MultiEdgeData = set[SingleEdgeData]
Edge = tuple[Node, Node, EdgeData]
