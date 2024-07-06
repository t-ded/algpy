from typing import Optional, Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.algorithm_runtime_breakdown import AlgorithmRuntimeBreakdown
from algpy_src.base.constants import ProblemInstance, InputSize


class AlgorithmRuntimeAnalytic:
    """
    Base class for running analysis of algorithms and comparing distinct algorithms among each other.
    """

    def __init__(self):
        pass

    def analyse_runtime(
            self, algorithm: Algorithm, input_sequence: Optional[dict[InputSize, ProblemInstance]],
            seed: Optional[int] = None, n: int = 10, generation_input_kwargs: Optional[dict[Any, Any]] = None,
            *run_algorithm_args, **run_algorithm_kwargs
    ) -> AlgorithmRuntimeBreakdown:
        """
        Runs algorithm on predefined or randomly generated instances of given sizes to assess its runtime complexity.

        Parameters
        ----------
        algorithm : Algorithm
        input_sequence : dict[InputSize, ProblemInstance]
        seed : Optional[int] (default None)
        n : int (default 10)
        generation_input_kwargs : dict[Any, Any] (default None)
        run_algorithm_args : Any
        run_algorithm_kwargs : Any

        Returns
        -------
        runtime_breakdown : AlgorithmRuntimeBreakdown
        """
        raise NotImplementedError()
