from abc import abstractmethod
from typing import Optional, Iterable, Generic, Any

from algpy_src.base.complexity_object import ComplexityObject
from algpy_src.base.constants import VERBOSITY_LEVELS, ProblemInstance, InputSize


class Algorithm(ComplexityObject, Generic[ProblemInstance, InputSize]):
    """
    Base class for all algorithms.
    Inheriting class should specify type hints for ProblemInstance and InputSize
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def name(self) -> str:
        return 'Generic Algorithm Class'

    @property
    def is_deterministic(self) -> bool:
        return True

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
    def run_algorithm(self, input_instance: ProblemInstance, verbosity_level: VERBOSITY_LEVELS = 0, *args: Any, **kwargs: Any) -> Optional[ProblemInstance]:
        """
        The main run function of each algorithm.
        The algorithms should be able to internally count number of ops and should reset self.n_ops to 0 on each use of this method.

        Parameters
        ----------
        input_instance : ProblemInstance
            Instance on which to run the algorithm.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 typically referring to no printing, 1 leading to print of given ProblemInstance before and after and 2 meaning every step.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        output_instance : Optional[ProblemInstance]
            Returns input processed by the algorithm if relevant.
        """
        raise NotImplementedError()
