import numpy as np
import time
from typing import Optional, Iterable
from abc import abstractmethod
from base.complexity_object import ComplexityObject
from base.constants import COMPLEXITIES


class Algorithm(ComplexityObject):
    """
    Base class for all algorithms.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    @property
    def name(self) -> str:
        return 'Generic Algorithm Class'

    def print_complexity_info(self, which: COMPLEXITIES = 'both') -> None:
        """
        Print the complexity information for the algorithm.

        Parameters:
        ----------
        which : str
            Select the type of complexity measure you want to print (one of 'both', 'time' or 'space').
        """
        if which == 'time' or which == 'both':
            self.print_time_complexity_info()
        if which == 'space' or which == 'both':
            self.print_space_complexity_info()

    @abstractmethod
    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information of the algorithm.
        """
        raise NotImplementedError()

    @abstractmethod
    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the algorithm.
        """
        raise NotImplementedError()

    @abstractmethod
    def generate_increasing_input_size_sequence(self) -> Iterable[int] | Iterable[Iterable[int]]:
        """

        Returns
        -------
        input_size_sequence : Iterable[int] or Iterable[Iterable[Iterable[int]]]
            Sequence of viable input size parameters for generate_random_input(input_size) in increasing order
        """
        raise NotImplementedError()

    @abstractmethod
    def generate_random_input(self, input_size: int | Iterable[int]) -> object:
        """
        Way to generate random input instance of given size.
        Output of this function has to be accepted by run_algorithm().

        Parameters
        ----------
        input_size : int or Iterable[int]
            Desired input size.

        Returns
        -------
        instance : object
            A problem instance supported in run_algorithm(input_instance=instance).
        """
        raise NotImplementedError()

    @abstractmethod
    def run_algorithm(self, input_instance: object, *args, **kwargs) -> tuple[Optional[object], int]:
        """
        The main run function of each algorithm. The algorithms should be able to internally count number of ops.

        Parameters
        ----------
        input_instance : object
            Instance on which to run the algorithm.
        *args
            Additional arguments passed to the algorithm.
        **kwargs
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        output_instance : Optional[object]
            Returns input processed by the algorithm if relevant.
        number_of_operations : int
            Outputs the total number of operations made by the algorithm.
        """
        raise NotImplementedError()

    def analyse_runtime(self, n: int = 10, *args, **kwargs) -> None:
        """
        Runs algorithm on randomly generated instances of given sizes

        Parameters
        ----------
        n : int
            Number of repetitions per input size for the statistical analysis of algorithm's runtime
        *args
            Arguments passed to the run_algorithm() function call.
        **kwargs
            Keyword arguments passed to the run_algorithm() function call.

        Returns
        -------

        """
        input_sizes = self.generate_increasing_input_size_sequence()
        print('-' * 10)
        self.print_time_complexity_info()
        print(f'Analysing runtime of the {self.name} algorithm:')
        for input_size in input_sizes:

            runtimes: list[float] = []
            ops_counts: list[int] = []

            for _ in range(n):
                input_instance = self.generate_random_input(input_size)
                start = time.time()
                run_output = self.run_algorithm(input_instance, args, kwargs)
                runtimes.append(time.time() - start)
                ops_counts.append(run_output[1])

            avg_secs = np.mean(runtimes)
            std_secs = np.std(runtimes)
            avg_ops = np.mean(ops_counts)
            std_ops = np.std(ops_counts)
            print(f'\tRun with input size {input_size} took {avg_secs:_.2f}', u'\u00B1', f'{std_secs:_2f} seconds',
                  f'and {avg_ops:_.2f}', u'\u00B1', f'{std_ops:_2f} operations ({n=} samples)')
