from typing import Any

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.constants import GraphSize, VERBOSITY_LEVELS, Node
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.shortest_paths_graph import ShortestPathsGraph


class DijkstraShortestPathsAlgorithm(Algorithm[Graph | DiGraph, GraphSize]):
    """
    Dijkstra's shortest path(s) algorithm.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return "Uni-directional Dijsktra's Shortest Path(s) Algorithm"

    @property
    def is_deterministic(self) -> bool:
        return True

    @property
    def best_case_time_complexity(self) -> str:
        return '1'

    @property
    def best_case_description(self) -> str:
        return 'starting from searched for element'

    @property
    def average_case_time_complexity(self) -> str:
        return '|E| + |V| * log(|V|)'

    @property
    def worst_case_time_complexity(self) -> str:
        return '|V| * [|E| + |V|* log(|V|)]'

    @property
    def worst_case_description(self) -> str:
        return 'all-pairs shortest paths'

    @property
    def space_complexity(self) -> str:
        return '|V| ^ 2'

    def get_worst_case_arguments(self, input_size: GraphSize) -> dict[str, Any]:
        """
        Generate a graph with input_size.nodes nodes and input_size.edges edges and find the shortest paths to all nodes in the graph from the root.
        The graph instance starts as a star graph, sequentially adding new star roots until desired number of edges is reached or until the graph is fully connected.

        Parameters
        ----------
        input_size : GraphSize
            Tuple of n_nodes, n_edges with desired graph size.

        Returns
        -------
        run_algorithm_kwargs : dict[str, Any]
            A dictionary with the created graph as 'input_instance' value, 'source' as the first node and 'target' as NoNode() object.
        """
        g: Graph = Graph()
        g.add_nodes_from(range(0, input_size.nodes))
        num_edges = 0
        root = 0
        while num_edges < input_size.edges and root + 1 < input_size.nodes:
            for new_neighbour in range(root + 1, input_size.nodes):
                g.add_edge((root, new_neighbour, 1))
                num_edges += 1
                if num_edges == input_size.edges:
                    break
            root += 1
        return {'input_instance': g, 'source': 0, 'target': NoNode()}

    def run_algorithm(self, input_instance: Graph | DiGraph, verbosity_level: VERBOSITY_LEVELS = 0, source: Node | NoNode = NoNode(),
                      target: Node | NoNode = NoNode(), *args: Any, **kwargs: Any) -> tuple[bool, ShortestPathsGraph]:
        """
        Run function of Dijkstra's uni-directional shortest path(s) algorithm.

        Parameters
        ----------
        input_instance : Graph | DiGraph
            Graph in which to run the search.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print the shortest path traversal graph at the end and
            2 meaning also print the shortest path traversal graph after every expanded node.
        source : Node | NoNode (default NoNode())
            Root node to find the shortest path(s) from. If not given, shortest paths from all nodes are found.
        target : Node | NoNode (default NoNode())
            Target node to find the shortest path(s) to. If not given, shortest paths to all nodes are found.
        *args : Any
            Additional arguments passed to the algorithm.
        **kwargs : Any
            Additional keyword arguments passed to the algorithm.

        Returns
        -------
        result : tuple[bool, ShortestPathsGraph]
            Returns True in the first index if the shortest path to target was found or if no target was specified.
            Also returns a ShortestPathsGraph object carrying the respective path lengths and predecessor and capable of reconstructing the path.
        """
        raise NotImplementedError()
    