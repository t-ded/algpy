import time
from abc import abstractmethod
from typing import Optional, Iterable, TypeVar, Generic, Any

import numpy as np

from algpy_src.base.complexity_object import ComplexityObject
from algpy_src.base.constants import COMPLEXITIES, PrintableComparable

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
    def time_complexity(self) -> str:
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
        if which == 'time' or which == 'both':
            self.print_time_complexity_info()
        if which == 'space' or which == 'both':
            self.print_space_complexity_info()

    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information of the algorithm.
        """
        print(f'Time complexity of the {self.name} algorithm is O({self.time_complexity})')

    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the algorithm.
        """
        print(f'Space complexity of the {self.name} algorithm is O({self.space_complexity})')

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

    def analyse_runtime(self, input_sequence: Optional[dict[InputSize, ProblemInstance]], seed: Optional[int] = None, n: int = 10, *args, **kwargs) -> None:
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
        *args
            Arguments passed to the run_algorithm() function call.
        **kwargs
            Keyword arguments passed to the run_algorithm() function call.

        Returns
        -------

        """
        if input_sequence is None:
            input_sizes: Iterable[InputSize] = self.generate_increasing_input_size_sequence()
            input_sequence = {input_size: self.generate_random_input(input_size, seed, args, kwargs) for input_size in input_sizes}

        print('-' * 10)
        self.print_time_complexity_info()
        print(f'Analysing runtime of the {self.name} algorithm:')
        for input_size, problem_instance in input_sequence.items():

            runtimes: list[float] = []
            ops_counts: list[int] = []

            for _ in range(n):
                start = time.time()
                run_output = self.run_algorithm(problem_instance, args, kwargs)
                runtimes.append(time.time() - start)
                ops_counts.append(run_output[1])

            avg_secs = np.mean(runtimes)
            std_secs = np.std(runtimes)
            avg_ops = np.mean(ops_counts)
            std_ops = np.std(ops_counts)
            print(f'\tRun on instance with problem size {input_size} took {avg_secs:_.2f}', u'\u00B1', f'{std_secs:_2f} seconds',
                  f'and {avg_ops:_.2f}', u'\u00B1', f'{std_ops:_2f} operations ({n=} repetitions)')
