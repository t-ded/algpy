from collections import namedtuple
from typing import Literal, Protocol, TypeVar

T = TypeVar('T')


class Comparable(Protocol):
    def __lt__(self: T, other: T) -> bool: ...

    def __le__(self: T, other: T) -> bool: ...

    def __eq__(self, other: T) -> bool: ...


class PrintableComparable(Comparable, Protocol):
    def __repr__(self) -> str: ...


COMPLEXITIES = Literal['both', 'time', 'space']
METRICS_TO_PLOT = Literal['both', 'time', 'n_ops']
TEST_SEED = 42
VERBOSITY_LEVELS = Literal[0, 1, 2]

ProblemInstance = TypeVar('ProblemInstance')
ResultInstance = TypeVar('ResultInstance')
InputSize = TypeVar('InputSize', bound=PrintableComparable)
GraphSize = namedtuple('GraphSize', 'nodes edges', defaults=[0, 0])
LoadBalancingTaskSize = namedtuple('LoadBalancingTaskSize', 'num_tasks num_servers')

G = TypeVar('G')
Node = TypeVar('Node')
EdgeData = TypeVar('EdgeData')
SingleEdgeData = TypeVar('SingleEdgeData')
MultiEdgeData = set[SingleEdgeData]
FlowEdgeData = namedtuple('FlowEdgeData', 'lower_bound flow upper_bound', defaults=[0, None, float('inf')])
Edge = tuple[Node, Node, EdgeData]

