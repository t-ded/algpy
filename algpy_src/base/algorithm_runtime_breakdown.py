from dataclasses import dataclass
from typing import Generic, Optional

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.constants import InputSize, ProblemInstance


@dataclass
class AlgorithmRuntimeSingle(Generic[InputSize, ProblemInstance]):
    algorithm: Algorithm
    input_size: InputSize
    input_sequence: ProblemInstance

    avg_secs: float
    std_secs: float
    avg_ops: float
    std_ops: float


@dataclass
class AlgorithmRuntimeBreakdown(Generic[ProblemInstance, InputSize]):
    algorithm: Algorithm
    used_random: bool

    worst_case_breakdown: Optional[AlgorithmRuntimeSingle] = None

    input_sequences: Optional[dict[InputSize, ProblemInstance]] = None
    per_case_breakdowns: Optional[dict[InputSize, AlgorithmRuntimeSingle]] = None



