import inspect
import logging
import time
from typing import Optional, Iterable, cast, Any

import numpy as np

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.algorithm_runtime_breakdown import AlgorithmRuntimeBreakdown, AlgorithmRuntimeSingle
from algpy_src.base.constants import ProblemInstance, InputSize, METRICS_TO_PLOT
from algpy_src.base.utils import print_delimiter, print_gap, underscore_formatter
from algpy_src.tools.algorithm_input_generation.generate_increasing_input_size_sequence import generate_increasing_input_size_sequence
from algpy_src.tools.algorithm_input_generation.random_input_generators import get_generator
from algpy_src.tools.complexity_info_display.complexity_info_displaying import print_time_complexity_info

_has_matplotlib = True
try:
    import matplotlib.pyplot as plt  # type: ignore
    import matplotlib.ticker as ticker  # type: ignore
except ImportError:
    _has_matplotlib = False


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

    def get_runtime_analysis_single_instance(self, problem_instance: ProblemInstance, input_size: InputSize, override_n_repetitions: Optional[int] = None,
                                             **run_algorithm_kwargs) -> AlgorithmRuntimeSingle:
        """
        Run statistical runtime analysis of this analytic's algorithm on a single problem instance.

        Parameters
        ----------
        problem_instance : ProblemInstance
            Problem instance to run the algorithm on.
        input_size : InputSize
            Size of the given problem instance.
        override_n_repetitions : Optional[int] (default None)
            If given, override the number self.n_repetitions for this runtime.
        **run_algorithm_kwargs : dict[Any, Any]
            Additional keyword arguments to pass to the algorithm's run_algorithm() function call.

        Returns
        -------
        runtime_breakdown : AlgorithmRuntimeSingle
            Breakdown of algorithm's runtime on a single instance
        """
        runtimes: list[float] = []
        ops_counts: list[int] = []

        n_repetitions = override_n_repetitions if override_n_repetitions is not None else self.n_repetitions
        for _ in range(n_repetitions):
            start = time.time()
            self.algorithm.run_algorithm(problem_instance, 0, **run_algorithm_kwargs)
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
            Additional keyword arguments passed to the run_algorithm() function call.

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

        run_algorithm_args = list(inspect.signature(self.algorithm.run_algorithm).parameters)
        run_algorithm_kwargs = {k: kwargs.pop(k) for k in dict(kwargs) if k in run_algorithm_args}

        worst_case_input_size = max(input_sequence.keys())
        worst_case_arguments = self.algorithm.get_worst_case_arguments(worst_case_input_size)
        worst_case_instance = worst_case_arguments.pop('input_instance')
        n_reps = 1 if self.algorithm.is_deterministic else None
        self.runtime_analysis.worst_case_breakdown = self.get_runtime_analysis_single_instance(
            worst_case_instance, worst_case_input_size, n_reps, **worst_case_arguments
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

    def print_runtime_analysis(self) -> None:
        """
        Function to print runtime analysis assigned to this analytic obtained earlier.
        """
        if self.runtime_analysis is None:
            logging.warning(f'No runtime analysis performed yet, run {self.__class__.__name__}.get_runtime_analysis(...) first.')
            return

        print_delimiter('-', 10)
        print(f'Analysing runtime of the {self.algorithm.name} algorithm:')
        print_time_complexity_info(self.algorithm)

        if self.runtime_analysis.worst_case_breakdown is not None:
            print_delimiter('-', 10)
            print('Algorithm analysis on its worst case instance:')
            if self.algorithm.is_deterministic:
                time_info = f'{self.runtime_analysis.worst_case_breakdown.avg_secs:_.2f}'
                n_ops_info = f'{int(self.runtime_analysis.worst_case_breakdown.avg_ops):_}'
                reps_info = '1 repetition'
            else:
                time_info = f'{self.runtime_analysis.worst_case_breakdown.avg_secs:_.2f} ' + u'\u00B1' + f' {self.runtime_analysis.worst_case_breakdown.std_secs:_.2f}'
                n_ops_info = f'{self.runtime_analysis.worst_case_breakdown.avg_ops:_.2f} ' + u'\u00B1' + f' {self.runtime_analysis.worst_case_breakdown.std_ops:_.2f}'
                reps_info = f'{self.n_repetitions} repetitions'
            print(
                f'  Run on worst case instance with problem size {self.runtime_analysis.worst_case_breakdown.input_size:_}',
                f'took {time_info} seconds and {n_ops_info} operations ({reps_info}).'
            )

        if self.runtime_analysis.per_case_breakdowns is not None:
            print_delimiter('-', 10)
            print(f'Algorithm analysis on {"given" if self.runtime_analysis.used_random is False else "random"} instances:')
            for input_size, breakdown in self.runtime_analysis.per_case_breakdowns.items():
                print(
                    f'  Run on instance with problem size {input_size:_}',
                    f'took {breakdown.avg_secs:_.2f}', u'\u00B1', f'{breakdown.std_secs:_.2f} seconds',
                    f'and {breakdown.avg_ops:_.2f}', u'\u00B1', f'{breakdown.std_ops:_.2f} operations',
                    f'({self.n_repetitions} repetitions).'
                )

        print_delimiter('-', 10)
        print_gap()

    def plot_runtime_analysis(self, save_path: Optional[str] = None, metric_to_plot: METRICS_TO_PLOT = 'both') -> None:
        """
        Function to plot runtime analysis assigned to this analytic obtained earlier and optionally save it.

        Parameters
        ----------
        save_path : Optional[str] (default None)
            If given, try saving the plot to the given path.
        metric_to_plot : METRICS_TO_PLOT (default 'both')
            One of 'both', 'time', 'n_ops' signifying which metric we want to plot.
        """
        if not _has_matplotlib:
            logging.warning('Optional module matplotlib is not installed. Install it to enable plotting functionality.')
            return

        if self.runtime_analysis is None:
            logging.warning(f'No runtime analysis performed yet, run {self.__class__.__name__}.get_runtime_analysis(...) first.')
            return

        if self.runtime_analysis.per_case_breakdowns is None:
            logging.warning(f'No per case breakdown analysis performed yet, run {self.__class__.__name__}.get_runtime_analysis(...) with either input sequence or max_input_size parameter first.')
            return

        input_sizes = sorted(self.runtime_analysis.per_case_breakdowns.keys())
        avg_secs = [self.runtime_analysis.per_case_breakdowns[size].avg_secs for size in input_sizes]
        std_secs = [self.runtime_analysis.per_case_breakdowns[size].std_secs for size in input_sizes]
        avg_ops = [self.runtime_analysis.per_case_breakdowns[size].avg_ops for size in input_sizes]
        std_ops = [self.runtime_analysis.per_case_breakdowns[size].std_ops for size in input_sizes]

        fig, ax1 = plt.subplots()
        ax1.set_title(f'Runtime Analysis of the {self.algorithm.name} algorithm', y=1.07, fontsize=14)
        fig.suptitle(f'Worst case time complexity O({self.algorithm.worst_case_time_complexity})', y=0.845, fontsize=12)

        ops_axis = None
        if metric_to_plot != 'n_ops':
            self._plot_values(input_sizes, avg_secs, std_secs, ax1, color='tab:blue', xlabel='Input Size', ylabel='Time (seconds)')
            if metric_to_plot == 'both':
                ops_axis = ax1.twinx()
        else:
            ops_axis = ax1
        if ops_axis is not None:
            self._plot_values(input_sizes, avg_ops, std_ops, ops_axis, color='tab:red', xlabel='Input Size', ylabel='# Operations')

        fig.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    @staticmethod
    def _plot_values(
            x_values_to_plot: list[int | float], y_values_to_plot: list[int | float], stds_to_plot: list[int | float], ax: Any,
            label_fontsize: int = 10, color: str = 'tab:black', xlabel: str = '', ylabel: str = '', fmt: str = 'X'
    ) -> None:

        ax.set_xlabel(xlabel, fontsize=label_fontsize)
        ax.set_ylabel(ylabel, color=color, fontsize=label_fontsize)
        ax.errorbar(x_values_to_plot, y_values_to_plot, yerr=stds_to_plot, fmt=fmt, color=color, ecolor='lightgray', elinewidth=1.5, capsize=2.5)
        ax.tick_params(axis='y', labelcolor=color)

        if x_values_to_plot[-1] >= 1_000:
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(underscore_formatter))
        if y_values_to_plot[-1] >= 1_000:
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(underscore_formatter))
