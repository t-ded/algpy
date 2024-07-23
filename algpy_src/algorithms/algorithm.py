from abc import abstractmethod
from typing import Optional, Generic, Any

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
    @abstractmethod
    def is_deterministic(self) -> bool:
        raise NotImplementedError()

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
    def get_worst_case_arguments(self, input_size: InputSize) -> dict[str, Any]:
        """
        Way to generate keyword arguments for this class' run_algorithm method corresponding to algorithm's worst case scenario.
        Output of this function has to be accepted by run_algorithm() and has to contain a pair 'input_instance': ProblemInstance with the value having given InputSize.

        Parameters
        ----------
        input_size : InputSize
            Desired input size (form depends on specific algorithm).

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with keyword arguments for the run_algorithm method.
        """
        raise NotImplementedError()

    @abstractmethod
    def run_algorithm(self, input_instance: ProblemInstance, verbosity_level: VERBOSITY_LEVELS = 0, *args: Any, **kwargs: Any) -> tuple[bool, Optional[ProblemInstance]]:
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
        result : tuple[bool, Optional[ProblemInstance]]
            Returns boolean value representing whether the algorithm terminated successfully and input processed by the algorithm if relevant.
        """
        raise NotImplementedError()
