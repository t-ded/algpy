from typing import Any, Generic, cast

import numpy as np

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import GraphSize, VERBOSITY_LEVELS, Node, EdgeData
from algpy_src.base.utils import print_problem_instance
from algpy_src.data_structures.graphs.feature_graph import FeatureGraph
from algpy_src.data_structures.graphs.graph_utils.no_feature_object import NoFeature


class RelationalClassificationAlgorithm(Algorithm[FeatureGraph, GraphSize], Generic[Node, EdgeData]):
    """
    Relational classification message passing algorithm (explained in more detail in https://www.youtube.com/watch?v=QUO-HQ44EDc)
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name='Relational Classification',
            algorithm_family=AlgorithmFamily.MESSAGE_PASSING,
            is_deterministic=True,
            best_case_time_complexity='|V|',
            best_case_description='all nodes pre-labelled',
            average_case_time_complexity='|E| * n_iterations',
            worst_case_time_complexity='N/A',
            worst_case_description='not reaching convergence',
            space_complexity='|V|',
        )

    def get_worst_case_arguments(self, input_size: GraphSize = GraphSize(*(1, 1))) -> dict[str, Any]:
        """
        Generate a FeatureGraph with 3 nodes and 2 edges for which the method does not converge.
        In the worst case, this would lead to an infinite loop - max number of iterations is specified for the worst case arguments, too, to avoid this.
        This is created as a graph with one node without a ground truth label that is influenced from both sides by the same number of labelled nodes.

        Parameters
        ----------
        input_size : GraphSize (default GraphSize(*(1, 1)))
            Tuple of n_nodes, n_edges with desired graph size.
            Is not used for this algorithm's worst case arguments generation since it would not influence the result (running into max iterations) anyhow.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with the created FeatureGraph as 'input_instance' value and 'max_iterations' set to sufficiently high number.
        """
        feature_graph: FeatureGraph = FeatureGraph({1: {2: True}})
        feature_graph.add_node_with_features(1, 0)
        feature_graph.add_node_with_features(2, 1)
        return {'input_instance': feature_graph, 'max_iterations': 1_000, 'convergence_threshold': -0.01}

    def run_algorithm(
            self, input_instance: FeatureGraph, verbosity_level: VERBOSITY_LEVELS = 0,
            max_iterations: int = 100_000, convergence_threshold: float = 0.01, classification_threshold: float = 0.5,
            *args: Any, **kwargs: Any
    ) -> tuple[bool, FeatureGraph]:
        """
        Run function for the relational classification algorithm.
        This function takes in a FeatureGraph object and assumes some of the nodes to have binary (0, 1) ground truth labels assigned as features.
        Then, it iteratively determines the label for other nodes.

        Parameters
        ----------
        input_instance : FeatureGraph
            The graph with ground truth labels as node features for specific nodes.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print node label assignment at the beginning and at the end and
            2 meaning also print the label probability for each node after every iteration.
        max_iterations : int (default 100_000)
            Maximum number of iterations to run the algorithm for if it does not converge naturally.
        convergence_threshold : float (default 0.01)
            Maximum change in label probability assignment to consider the given node label probability stable.
        classification_threshold : float (default 0.5)
            The probability threshold above which the predict class is 1 for each node, otherwise 0.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, FeatureGraph]
            Returns True in the first index if the algorithm terminated due to convergence and not reaching max number of iterations.
            Also returns the graph with assigned labels to each node as features.
        """

        self.reset_n_ops()
        print_problem_instance(input_instance, verbosity_level, 1)
        for node, neighbourhood in input_instance.adjacency_list.items():
            if not all(isinstance(edge_data, (int, float, bool)) for edge_data in neighbourhood.values()):
                raise ValueError('Relational classification algorithm can only be ran with numerical edge values.')

        nodes_without_label: set[Node] = set()
        for node in input_instance.nodes:
            inp_feature = input_instance.get_node_features(node)
            if inp_feature == NoFeature():
                nodes_without_label.add(node)
                input_instance.add_node_with_features(node, 0.5)
            elif not isinstance(inp_feature, (int, float, bool)) or not 0 <= inp_feature <= 1:
                raise ValueError('Relational classification algorithm can only be ran with numerical node feature values between 0 and 1.')

        max_label_change = np.inf
        n_iterations = 0
        while max_label_change > convergence_threshold and n_iterations < max_iterations:

            max_label_change = 0
            for node in nodes_without_label:

                norm_constant = 0.0
                prob_sum = 0.0

                for neighbour, edge_data in input_instance.adjacency_list[node].items():
                    self.increment_n_ops()
                    norm_constant += edge_data
                    prob_sum += edge_data * cast(float, input_instance.get_node_features(neighbour))

                new_prob = 1 / norm_constant * prob_sum
                max_label_change = max(max_label_change, abs(new_prob - cast(float, input_instance.get_node_features(node))))
                input_instance.add_node_with_features(node, new_prob)

            n_iterations += 1
            print_problem_instance(input_instance, verbosity_level, 2)

        print_problem_instance(input_instance, verbosity_level, 1)
        for node in nodes_without_label:
            input_instance.add_node_with_features(node, 1 if cast(float, input_instance.get_node_features(node)) > classification_threshold else 0)

        return n_iterations < max_iterations, input_instance
