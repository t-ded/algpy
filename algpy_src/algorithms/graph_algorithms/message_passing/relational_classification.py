from typing import Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.constants import GraphSize, VERBOSITY_LEVELS
from algpy_src.data_structures.graphs.feature_graph import FeatureGraph


class RelationalClassificationAlgorithm(Algorithm[FeatureGraph, GraphSize]):
    """
    Relational classification message passing algorithm (explained in more detail in https://www.youtube.com/watch?v=QUO-HQ44EDc)
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return 'Relational Classification'

    @property
    def is_deterministic(self) -> bool:
        return True

    @property
    def best_case_time_complexity(self) -> str:
        return '|V|'

    @property
    def best_case_description(self) -> str:
        return 'all nodes pre-labelled'

    @property
    def average_case_time_complexity(self) -> str:
        return '|E| * n_iterations'

    @property
    def worst_case_time_complexity(self) -> str:
        return 'N/A'

    @property
    def worst_case_description(self) -> str:
        return 'does not converge'

    @property
    def space_complexity(self) -> str:
        return '|V|'

    def get_worst_case_arguments(self, input_size: GraphSize) -> dict[str, Any]:
        """
        Generate a FeatureGraph with 3 nodes and 2 edges for which the method does not converge.
        In the worst case, this would lead to an infinite loop - max number of iterations is specified for the worst case arguments, too, to avoid this.
        This is created as a graph with one node without a ground truth label that is influenced from both sides by the same number of labelled nodes.

        Parameters
        ----------
        input_size : GraphSize
            Tuple of n_nodes, n_edges with desired graph size.
            Is not used for this algorithm's worst case arguments generation.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with the created FeatureGraph as 'input_instance' value and 'max_iterations' set to sufficiently high number.
        """
        feature_graph: FeatureGraph = FeatureGraph()
        feature_graph.add_node_with_features(1, 0)
        feature_graph.add_node_with_features(3, 1)
        feature_graph.add_edges_from([(1, 2, None), (3, 2, None)])
        return {'input_instance': feature_graph, 'max_iterations': 10_000}

    def run_algorithm(
            self, input_instance: FeatureGraph, verbosity_level: VERBOSITY_LEVELS = 0,
            max_iterations: int = 100_000,
            *args: Any, **kwargs: Any
    ) -> tuple[bool, FeatureGraph]:

        raise NotImplementedError()
        # label_assignment: dict[Node, float] = defaultdict(lambda: 0.5)
        # if ground_truth is not None:
        #     label_assignment.update(ground_truth)

