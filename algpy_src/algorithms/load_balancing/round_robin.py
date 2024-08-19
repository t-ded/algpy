import itertools
from typing import Iterable, Any, Optional

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import LoadBalancingTaskSize, VERBOSITY_LEVELS
from algpy_src.base.utils import print_problem_instance
from algpy_src.data_structures.system_design.load_task import LoadTask
from algpy_src.data_structures.system_design.server import Server


class RoundRobinAlgorithm(Algorithm[tuple[Iterable[LoadTask], list[Server]], LoadBalancingTaskSize, tuple[Iterable[LoadTask], list[Server]]]):
    """
    (Optionally weighted) Round Robin algorithm for load assignment to servers.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name='Round Robin',
            algorithm_family=AlgorithmFamily.LOAD_BALANCING,
            is_deterministic=True,
            best_case_time_complexity='n',
            best_case_description='irrelevant - with this variant, all inputs require exactly one pass through the entire task list',
            average_case_time_complexity='n',
            worst_case_time_complexity='n',
            worst_case_description='irrelevant - with this variant, all inputs require exactly one pass through the entire task list',
            space_complexity='1',
        )

    def get_worst_case_arguments(self, input_size: LoadBalancingTaskSize) -> dict[str, Any]:
        """
        As the time complexity of the Round Robin algorithm is always the same irrespective of the input, the generated worst case is constant easy input with one task and one server.

        Parameters
        ----------
        input_size : LoadBalancingTaskSize
            Tuple of desired number of tasks and number of servers

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with the created tuple of one task and one server.
        """
        return {'input_instance': ([LoadTask(identifier='worst_case', size=1)], [Server()])}

    def run_algorithm(
            self, input_instance: tuple[Iterable[LoadTask], list[Server]], verbosity_level: VERBOSITY_LEVELS = 0,
            server_weights: Optional[dict[Server, int]] = None, *args: Any, **kwargs: Any
    ) -> tuple[bool, tuple[Iterable[LoadTask], list[Server]]]:
        """
        Run function of the Round Robin algorithm. Iterates over provided servers and assigns the next task in a sequence to them until all tasks are assigned or no more can fit.
        This algorithm assumes the silent overflow ignoring variant, which skips any tasks that the current server in the sequence cannot fit.
        This limits the time complexity to O(n) instead of O(n^2) as in the case of trying to find capable subsequent server.

        Parameters
        ----------
        input_instance : tuple[Iterable[LoadTask], Iterable[Server]]
            Pair - sequence of tasks to be distributed and dictionary of available servers and their weights or an iterable of these for uniform variant.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print of the assignment after termination of the algorithm and
            2 meaning also print the assignment after each newly assigned task.
        server_weights : Optional[dict[Server, int]] (default None)
            Mapping of server weights. If not given, uniform distribution of tasks across servers will be used.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, tuple[Iterable[LoadTask], Iterable[Server]]]
            Returns True in the first index if all tasks were assigned, otherwise False.
            Also returns back tuple of the unassigned tasks and the initial list of servers with tasks assigned to them.
        """

        self.reset_n_ops()
        server_weights_ordered = {}
        if server_weights is None:
            server_weights = {}
        for server in input_instance[1]:
            server_weights_ordered[server] = server_weights.get(server, 1)
        server_index_cycler = itertools.cycle(self._virtualize_probability(server_weights_ordered))

        unassigned_tasks: list[LoadTask] = []
        for task in input_instance[0]:
            current_server_index = next(server_index_cycler)
            self.increment_n_ops()
            if input_instance[1][current_server_index].can_handle_task(task):
                input_instance[1][current_server_index].add_task(task)
            else:
                unassigned_tasks.append(task)
            print_problem_instance(input_instance[1], verbosity_level, 2)

        print_problem_instance(input_instance[1], verbosity_level, 1)
        return len(unassigned_tasks) > 0, (unassigned_tasks, input_instance[1])

    @staticmethod
    def _virtualize_probability(server_weights: dict[Server, int]) -> list[int]:
        """
        Helper method to unroll the servers to a list of their indices repeated with respect to weights of the servers.

        Parameters
        ----------
        server_weights : dict[Server, int]
            Mapping of servers to their weights in the order corresponding to the desired indices.

        Returns
        -------
        unrolled_indices : list[int]
            List of server indices repeated with respect to weights of the servers.
        """
        server_indices: list[int] = []
        for i, weight in enumerate(server_weights.values()):
            if not isinstance(weight, int):
                raise ValueError('Server weights were expected to be integers.')
            if weight < 0:
                raise ValueError('Server weights were expected to be positive.')
            server_indices.extend([i] * weight)
        return server_indices
