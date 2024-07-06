from dataclasses import dataclass
from typing import Iterable, Generic

from algpy_src.base.constants import InputSize, ProblemInstance


@dataclass
class AlgorithmRuntimeBreakdown(Generic[ProblemInstance, InputSize]):
    algorithm_name: str
    input_sizes: Iterable[InputSize]
    input_sequences: dict[InputSize, ProblemInstance]

    worst_case_input_size: InputSize
    worst_case_instance: ProblemInstance
    worst_case_avg_secs: float
    worst_case_std_secs: float
    worst_case_avg_ops: float
    worst_case_std_ops: float

    avg_secs_per_instance: float
    std_secs_per_instance: float
    avg_ops_per_instance: float
    std_ops_per_instance: float
