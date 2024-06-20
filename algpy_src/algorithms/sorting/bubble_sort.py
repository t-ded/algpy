import random
from typing import Iterable, Optional, TypeVar
from algpy_src.base.constants import Comparable

from algpy_src.algorithms.algorithm import Algorithm


class BubbleSort(Algorithm):

    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return 'Bubble sort'

    @property
    def time_complexity(self) -> str:
        return 'n^2'

    @property
    def space_complexity(self) -> str:
        return '1'

    def generate_increasing_input_size_sequence(self) -> Iterable[tuple[int, ...]]:
        return [10 ** i for i in range(0, 7)]

    def generate_random_input(self, input_size: tuple[int, ...]) -> Iterable[Comparable]:
        return [random.randint(1, 1_000) for _ in range(input_size[0])]

    def run_algorithm(self, input_instance: Iterable[Comparable], *args, **kwargs) -> tuple[Optional[Iterable[Comparable]], int]:
        pass
