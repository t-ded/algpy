import inspect
import logging
import time
from typing import Optional, Iterable, cast

import numpy as np

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.algorithm_runtime_breakdown import AlgorithmRuntimeBreakdown, AlgorithmRuntimeSingle
from algpy_src.base.constants import ProblemInstance, InputSize
from algpy_src.base.utils import print_delimiter, print_gap
from algpy_src.tools.algorithm_input_generation.generate_increasing_input_size_sequence import generate_increasing_input_size_sequence
from algpy_src.tools.algorithm_input_generation.random_input_generators import get_generator
from algpy_src.tools.complexity_info_display.complexity_info_displaying import print_time_complexity_info


class AlgorithmRuntimeAnalytic:
    """
    Base class for running analysis of algorithms and comparing distinct algorithms among each other.
    """

    def __init__(self, algorithm: Algorithm, n_repetitions: int = 10, seed: Optional[int] = None) -> None:
        """
        Analytic class to perform runtime analysis and get runtime breakdowns.

        Parameters
        ----------
        algorithm : Algorithm
            Algorithm whose runtime to analyse.
        n_repetitions : int (default 10)
            Number of repetitions for analysis of each problem instance to get a statistical sample.
        seed : Optional[int] (default None)
            Seed for random input generation.
        """
        self.algorithm: Algorithm = algorithm
        self.n_repetitions = n_repetitions
        self.runtime_analysis: Optional[AlgorithmRuntimeBreakdown] = None
        self.random_input_generator = get_generator(self.algorithm)(seed)

    def get_runtime_analysis_single_instance(self, problem_instance: ProblemInstance, input_size: InputSize,
                                             **run_algorithm_kwargs) -> AlgorithmRuntimeSingle:
        """
        Run statistical runtime analysis of this analytic's algorithm on a single problem instance.

        Parameters
        ----------
        problem_instance : ProblemInstance
            Problem instance to run the algorithm on.
        input_size : InputSize
            Size of the given problem instance.
        run_algorithm_kwargs
            Additional keyword arguments to pass to the algorithm's run_algorithm() function call.

        Returns
        -------
        runtime_breakdown : AlgorithmRuntimeSingle
            Breakdown of algorithm's runtime on a single instance
        """
        runtimes: list[float] = []
        ops_counts: list[int] = []

        for _ in range(self.n_repetitions):
            start = time.time()
            self.algorithm.run_algorithm(problem_instance, 0, kwargs=run_algorithm_kwargs)
            runtimes.append(time.time() - start)
            ops_counts.append(self.algorithm.n_ops)

        return AlgorithmRuntimeSingle(
            algorithm=self.algorithm,
            input_size=input_size,
            input_sequence=problem_instance,

            avg_secs=float(np.mean(runtimes)),
            std_secs=float(np.std(runtimes)),
            avg_ops=float(np.mean(ops_counts)),
            std_ops=float(np.std(ops_counts)),
        )

    def get_runtime_analysis(self, input_sequence: Optional[dict[InputSize, ProblemInstance]] = None, max_input_size: Optional[InputSize] = None, **kwargs) -> None:
        """
        Runs algorithm assigned to this analytic on predefined or randomly generated instances of given sizes to assess its runtime complexity.
        The complexity breakdown is saved to this object's runtime_analysis attribute.

        Parameters
        ----------
        input_sequence : Optional[dict[InputSize, ProblemInstance]] (default None)
            Optional dictionary of input_size : problem instance pairs to analyse the algorithm's runtime on.
            If not given, random inputs are generated.
        max_input_size : Optional[InputSize] (default None)
            Maximal size of an item in the randomly generated input sequence if input_sequence is not given.
            Has to be given if input_sequence is not given.
        **kwargs : Any
            Additional keyword arguments passed to the run_algorithm() or generate_worst_case() function call.

        Returns
        -------
        runtime_breakdown : AlgorithmRuntimeBreakdown
            Dataclass storing aggregate info per each input problem instance.
        """
        if input_sequence is None and max_input_size is None:
            raise ValueError('One of input_sequence or max_input_size must be given.')

        self.runtime_analysis = AlgorithmRuntimeBreakdown(
            algorithm=self.algorithm,
            used_random=input_sequence is None,
        )

        if input_sequence is None:
            max_input_size = cast(InputSize, max_input_size)
            input_sizes: Iterable[InputSize] = generate_increasing_input_size_sequence(self.algorithm, max_input_size=max_input_size)
            input_sequence = {
                input_size: self.random_input_generator.generate_random_input(input_size)
                for input_size in input_sizes
            }
        cast(dict[InputSize, ProblemInstance], input_sequence)

        run_algorithm_args = list(inspect.signature(self.algorithm.run_algorithm).parameters)
        run_algorithm_kwargs = {k: kwargs.pop(k) for k in dict(kwargs) if k in run_algorithm_args}

        worst_case_generation_args = list(inspect.signature(self.algorithm.generate_worst_case).parameters)
        worst_case_generation_kwargs = {k: kwargs.pop(k) for k in dict(kwargs) if k in worst_case_generation_args}
        worst_case_input_size = max(input_sequence.keys())
        worst_case_instance = self.algorithm.generate_worst_case(worst_case_input_size, kwargs=worst_case_generation_kwargs)
        self.runtime_analysis.worst_case_breakdown = self.get_runtime_analysis_single_instance(
            worst_case_instance, worst_case_input_size, kwargs=run_algorithm_kwargs
        )

        for input_size, problem_instance in input_sequence.items():
            if self.runtime_analysis.input_sequences is None:
                self.runtime_analysis.input_sequences = {}
            if self.runtime_analysis.per_case_breakdowns is None:
                self.runtime_analysis.per_case_breakdowns = {}
            self.runtime_analysis.input_sequences[input_size] = problem_instance
            self.runtime_analysis.per_case_breakdowns[input_size] = self.get_runtime_analysis_single_instance(
                problem_instance, input_size, kwargs=run_algorithm_kwargs
            )

    def print_runtime_analysis(self):
        """
        Function to print runtime analysis assigned to this analytic obtained earlier.
        """
        if self.runtime_analysis is None:
            logging.warning(f'No runtime analysis performed yet, run {self.__class__.__name__}.get_runtime_analysis(...) first.')
            return

        print_delimiter('-', 10)
        print(f'Analysing runtime of the {self.algorithm.name} algorithm:')
        print_time_complexity_info(self.algorithm)

        print_delimiter('-', 10)
        print('Algorithm analysis on its worst case instance:')
        print(
            f'  Run on worst case instance with problem size {self.runtime_analysis.worst_case_breakdown.input_size}',
            f'took {self.runtime_analysis.worst_case_breakdown.avg_secs:_.2f}', u'\u00B1', f'{self.runtime_analysis.worst_case_breakdown.std_secs:_.2f} seconds',
            f'and {self.runtime_analysis.worst_case_breakdown.avg_ops:_.2f}' + (u' \u00B1 ' if not self.algorithm.is_deterministic else '') +
            (f'{self.runtime_analysis.worst_case_breakdown.std_ops:_.2f}' if not self.algorithm.is_deterministic else '') +
            f' operations ({self.n_repetitions} repetitions)'
        )

        print_delimiter('-', 10)
        print(f'Algorithm analysis on {"given" if self.runtime_analysis.used_random is False else "random"} instances:')
        for input_size, breakdown in self.runtime_analysis.per_case_breakdowns.items():
            print(
                f'  Run on instance with problem size {input_size}',
                f'took {breakdown.avg_secs:_.2f}', u'\u00B1', f'{breakdown.std_secs:_.2f} seconds',
                f'and {breakdown.avg_ops:_.2f}', u'\u00B1', f'{breakdown.std_ops:_.2f} operations',
                f'({self.n_repetitions} repetitions)'
            )

        print_delimiter('-', 10)
        print_gap()
