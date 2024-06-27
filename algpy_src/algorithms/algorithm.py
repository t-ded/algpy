import time
from abc import abstractmethod
from typing import Optional, Iterable, TypeVar, Generic, Any

import numpy as np

from algpy_src.base.complexity_object import ComplexityObject
from algpy_src.base.constants import COMPLEXITIES, PrintableComparable
from algpy_src.base.utils import print_delimiter, print_gap

ProblemInstance = TypeVar('ProblemInstance')
InputSize = TypeVar('InputSize', bound=PrintableComparable)


class Algorithm(ComplexityObject, Generic[ProblemInstance, InputSize]):
    """
    Base class for all algorithms.
    Inheriting class should specify type hints for ProblemInstance and InputSize
    """

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Generic Algorithm Class'

    @property
    @abstractmethod
    def best_case_time_complexity(self) -> str:
        return 'N/A'

    @property
    @abstractmethod
    def best_case_description(self) -> str:
        return 'N/A'

    @property
    @abstractmethod
    def average_case_time_complexity(self) -> str:
        return 'N/A'

    @property
    @abstractmethod
    def worst_case_time_complexity(self) -> str:
        return 'N/A'

    @property
    @abstractmethod
    def worst_case_description(self) -> str:
        return 'N/A'

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        return 'N/A'

    def print_complexity_info(self, which: COMPLEXITIES = 'both') -> None:
        """
        Print the complexity information for the algorithm.

        Parameters:
        ----------
        which : str (default 'both')
            Select the type of complexity measure you want to print (one of 'both', 'time' or 'space').
        """
        print_delimiter()
        if which == 'time' or which == 'both':
            self.print_time_complexity_info()
            print_delimiter(n=5)
        if which == 'space' or which == 'both':
            self.print_space_complexity_info()
        print_delimiter()

    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information of the algorithm.
        """
        print(f'Time complexity breakdown of the {self.name} algorithm:')
        print(f'\tBest case time complexity is O({self.best_case_time_complexity}) with best case being {self.best_case_description}.')
        print(f'\tAverage case time complexity is O({self.average_case_time_complexity}).')
        print(f'\tWorst case time complexity is O({self.worst_case_time_complexity}) with worst case being {self.worst_case_description}.')

    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the algorithm.
        """
        print(f'Space complexity of the {self.name} algorithm is O({self.space_complexity}).')

    @abstractmethod
    def generate_increasing_input_size_sequence(self, *args: Any, **kwargs: Any) -> Iterable[InputSize]:
        """
        Parameters
        ----------
        *args : Any
            Additional arguments passed to the input sizes generating function.
        **kwargs : Any
            Additional keyword arguments passed to the input sizes generating function.

        Returns
        -------
        input_size_sequence : Iterable[InputSize]
            Sequence of viable input size parameters for generate_random_input(input_size) in order of increasing complexity.
        """
        raise NotImplementedError()

    @abstractmethod
    def generate_random_input(self, input_size: InputSize, seed: Optional[int] = None, *args: Any, **kwargs: Any) -> ProblemInstance:
        """
        Way to generate single random input instance of given size.
        Output of this function has to be accepted by run_algorithm().

        Parameters
        ----------
        input_size : InputSize
            Desired input size (form depends on specific algorithm).
        seed : Optional[int] (default None)
            Seed for generating random instance.
        *args : Any
            Additional arguments passed to the generating function.
        **kwargs : Any
            Additional keyword arguments passed to the generating function.

        Returns
        -------
        instance : ProblemInstance
            A problem instance supported in run_algorithm(input_instance=instance).
        """
        raise NotImplementedError()

    @abstractmethod
    def generate_worst_case(self, input_size: InputSize, *args: Any, **kwargs: Any) -> ProblemInstance:
        """
        Way to generate single input instance of given size corresponding to algorithm's worst case scenario.
        Output of this function has to be accepted by run_algorithm().

        Parameters
        ----------
        input_size : InputSize
            Desired input size (form depends on specific algorithm).
        *args : Any
            Additional arguments passed to the generating function.
        **kwargs : Any
            Additional keyword arguments passed to the generating function.

        Returns
        -------
        instance : ProblemInstance
            A problem instance supported in run_algorithm(input_instance=instance).
        """
        raise NotImplementedError()

    @abstractmethod
    def run_algorithm(self, input_instance: ProblemInstance, *args: Any, **kwargs: Any) -> tuple[Optional[ProblemInstance], int]:
        """
        The main run function of each algorithm. The algorithms should be able to internally count number of ops.

        Parameters
        ----------
        input_instance : ProblemInstance
            Instance on which to run the algorithm.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        output_instance : Optional[ProblemInstance]
            Returns input processed by the algorithm if relevant.
        number_of_operations : int
            Outputs the total number of operations made by the algorithm.
        """
        raise NotImplementedError()

    def analyse_runtime_single(self, problem_instance: ProblemInstance, n: int = 10, *args: Any, **kwargs: Any) -> tuple[float, float, float, float]:
        """
        Perform runtime and number of operations analysis with a single problem instance.

        Parameters
        ----------
        problem_instance : ProblemInstance
            Instance on which to run the algorithm. Has to be accepted by the run_algorithm(input_instance=problem_instance) call.
        n : int (default 10)
            Number of repetitions to obtain the statistical results.
        *args : Any
            Additional arguments passed to the run_algorithm() function call.
        **kwargs
            Additional keyword arguments passed to the run_algorithm() function call.

        Returns
        -------
        avg_secs : float
            Average runtime of the algorithm for a single problem instance.
        std_secs : float
            Standard deviation of runtime of the algorithm for a single problem instance.
        avg_ops : float
            Average number of operations of the algorithm for a single problem instance.
        std_ops : float
            Standard deviation of number of operations of the algorithm for a single problem instance.
        """
        runtimes: list[float] = []
        ops_counts: list[int] = []

        for _ in range(n):
            start = time.time()
            run_output = self.run_algorithm(problem_instance, args, kwargs)
            runtimes.append(time.time() - start)
            ops_counts.append(run_output[1])

        avg_secs = float(np.mean(runtimes))
        std_secs = float(np.std(runtimes))
        avg_ops = float(np.mean(ops_counts))
        std_ops = float(np.std(ops_counts))

        return avg_secs, std_secs, avg_ops, std_ops

    def analyse_runtime(self, input_sequence: Optional[dict[InputSize, ProblemInstance]],
                        seed: Optional[int] = None, n: int = 10, *args: Any, **kwargs: Any) -> None:
        """
        Runs algorithm on randomly generated instances of given sizes.

        Parameters
        ----------
        input_sequence : Optional[dict[InputSize, ProblemInstance]]
            Optional dictionary of input size : problem instance pairs to analyse the algorithm runtime on.
            If not given, random inputs are generated.
        seed : Optional[int] (default None)
            Seed for generating random instances in case input_sequence not provided.
        n : int (default 10)
            Number of repetitions per input size for the statistical analysis of algorithm's runtime.
        *args : Any
            Additional arguments passed to the run_algorithm() function call.
        **kwargs
            Additional keyword arguments passed to the run_algorithm() function call.
        """
        using_random = False
        if input_sequence is None:
            using_random = True
            input_sizes: Iterable[InputSize] = self.generate_increasing_input_size_sequence()
            input_sequence = {input_size: self.generate_random_input(input_size, seed, args, kwargs) for input_size in input_sizes}

        print_delimiter('-', 10)
        print(f'Analysing runtime of the {self.name} algorithm:')
        self.print_time_complexity_info()

        print_delimiter('-', 10)
        print('Algorithm analysis on its worst case instance:')
        worst_case_input_size = max(input_sequence.keys())
        worst_case_instance = self.generate_worst_case(worst_case_input_size, args, kwargs)
        avg_secs, std_secs, avg_ops, std_ops = self.analyse_runtime_single(worst_case_instance, n, args, kwargs)
        print(f'\tRun on worst case instance with problem size {worst_case_input_size} took {avg_secs:_.2f}', u'\u00B1', f'{std_secs:_2f} seconds',
              f'and {avg_ops:_.2f}', u'\u00B1', f'{std_ops:_2f} operations ({n=} repetitions)')

        print_delimiter('-', 10)
        print(f'Algorithm analysis on {"given" if using_random is False else "random"} instances:')
        for input_size, problem_instance in input_sequence.items():

            avg_secs, std_secs, avg_ops, std_ops = self.analyse_runtime_single(problem_instance, n, args, kwargs)
            print(f'\tRun on instance with problem size {input_size} took {avg_secs:_.2f}', u'\u00B1', f'{std_secs:_2f} seconds',
                  f'and {avg_ops:_.2f}', u'\u00B1', f'{std_ops:_2f} operations ({n=} repetitions)')

        print_delimiter('-', 10)
        print_gap(3)
