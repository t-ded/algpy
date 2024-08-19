from abc import abstractmethod
from typing import Optional, Generic, Any

from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.complexity_object import ComplexityObject
from algpy_src.base.constants import VERBOSITY_LEVELS, ProblemInstance, InputSize, ResultInstance


class Algorithm(ComplexityObject, Generic[ProblemInstance, InputSize, ResultInstance]):
    """
    Base class for all algorithms.
    Inheriting class should specify type hints for ProblemInstance and InputSize
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name='Generic Algorithm Class',
            algorithm_family=AlgorithmFamily.BASE_CLASS,
            is_deterministic=True,
            best_case_time_complexity='N/A',
            best_case_description='N/A',
            average_case_time_complexity='N/A',
            worst_case_time_complexity='N/A',
            worst_case_description='N/A',
            space_complexity='N/A',
        )

    @property
    def name(self) -> str:
        return self.algorithm_properties.name

    @property
    def algorithm_family(self) -> AlgorithmFamily:
        return self.algorithm_properties.algorithm_family

    @property
    def is_deterministic(self) -> bool:
        return self.algorithm_properties.is_deterministic

    @property
    def best_case_time_complexity(self) -> str:
        return self.algorithm_properties.best_case_time_complexity

    @property
    def best_case_description(self) -> str:
        return self.algorithm_properties.best_case_description

    @property
    def average_case_time_complexity(self) -> str:
        return self.algorithm_properties.average_case_time_complexity

    @property
    def worst_case_time_complexity(self) -> str:
        return self.algorithm_properties.worst_case_time_complexity

    @property
    def worst_case_description(self) -> str:
        return self.algorithm_properties.worst_case_description

    @property
    def space_complexity(self) -> str:
        return self.algorithm_properties.space_complexity

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
    def run_algorithm(self, input_instance: ProblemInstance, verbosity_level: VERBOSITY_LEVELS = 0, *args: Any, **kwargs: Any) -> tuple[bool, Optional[ResultInstance]]:
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
        result : tuple[bool, Optional[ResultInstance]]
            Returns boolean value representing whether the algorithm terminated successfully and some form of input processed by the algorithm if relevant.
        """
        raise NotImplementedError()
