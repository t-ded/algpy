from typing import Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import GraphSize, VERBOSITY_LEVELS, Node
from algpy_src.base.utils import print_problem_instance
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.traversal_graph import TraversalGraph
from algpy_src.data_structures.linear.stack import Stack


class DepthFirstSearch(Algorithm[Graph | DiGraph, GraphSize]):
    """
    Depth First Search algorithm.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name='Depth First Search',
            algorithm_family=AlgorithmFamily.GRAPH_TRAVERSAL,
            is_deterministic=True,
            best_case_time_complexity='1',
            best_case_description='starting from searched for element',
            average_case_time_complexity='|V| + |E|',
            worst_case_time_complexity='|V| + |E|',
            worst_case_description='searched for element not present in the graph',
            space_complexity='|V|',
        )

    def get_worst_case_arguments(self, input_size: GraphSize) -> dict[str, Any]:
        """
        Generate a graph with input_size.nodes nodes and input_size.edges edges and search for element that is not present in the graph.
        The graph instance starts as a star graph, sequentially adding new star roots until desired number of edges is reached or until the graph is fully connected.

        Parameters
        ----------
        input_size : GraphSize
            Tuple of n_nodes, n_edges with desired graph size.

        Returns
        -------
        run_algorithm_kwargs: dict[str, Any]
            A dictionary with the created graph as 'input_instance' value and 'element_to_search' which is not present in the graph.
        """
        g: Graph = Graph()
        g.add_nodes_from(range(0, input_size.nodes))
        num_edges = 0
        root = 0
        while num_edges < input_size.edges and root + 1 < input_size.nodes:
            for new_neighbour in range(root + 1, input_size.nodes):
                g.add_edge((root, new_neighbour, None))
                num_edges += 1
                if num_edges == input_size.edges:
                    break
            root += 1
        return {'input_instance': g, 'element_to_search': input_size.nodes + 1}

    def run_algorithm(self, input_instance: Graph | DiGraph, verbosity_level: VERBOSITY_LEVELS = 0, root: Node | NoNode = NoNode(),
                      element_to_search: Node | NoNode = NoNode(), *args: Any, **kwargs: Any) -> tuple[bool, TraversalGraph]:
        """
        Run function of the depth first search (DFS) algorithm.

        Parameters
        ----------
        input_instance : Graph | DiGraph
            Graph in which to run the search.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print of the traversal order nodes at the end and 2 meaning also print the traversal order nodes after every expanded node.
        root : Node | NoNode (default NoNode())
            Root node to start the traversal from. If not given, go in order of input_instance.nodes.
            If more connected components are present in the graph, they are also traversed in order corresponding to input_instance.nodes.
        element_to_search : Node | NoNode (default NoNode())
            Element to look for in the graph. If not given, whole graph is traversed.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, TraversalGraph]
            Returns True in the first index if the element was found in the graph or if no element was given for search.
            Also returns a new tree graph with node order corresponding to the order of traversal.
        """

        self.reset_n_ops()
        traversal_graph: TraversalGraph = TraversalGraph()
        visited: set[Node] = set()
        stack: Stack[Node] = Stack()

        for node in [root] if root != NoNode() else input_instance.nodes:
            if node not in visited:
                visited.add(node)
                stack.push(node)
                self.increment_n_ops()

                while stack.size > 0:
                    current = stack.pop()
                    print_problem_instance(traversal_graph.nodes, verbosity_level, 2)
                    traversal_graph.add_node(current)
                    self.increment_n_ops()
                    if current == element_to_search:
                        print_problem_instance(traversal_graph.nodes, verbosity_level, 1)
                        return True, traversal_graph

                    for neighbor in input_instance.neighbors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            stack.push(neighbor)
                            self.increment_n_ops()

        print_problem_instance(traversal_graph.nodes, verbosity_level, 1)
        return element_to_search == NoNode(), traversal_graph
