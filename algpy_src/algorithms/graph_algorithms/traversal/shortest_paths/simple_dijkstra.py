from typing import Any, Optional

from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.algorithms.base.algorithm_properties import AlgorithmProperties, AlgorithmFamily
from algpy_src.base.constants import GraphSize, VERBOSITY_LEVELS, Node
from algpy_src.base.utils import print_problem_instance
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph import Graph
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.shortest_paths_graph import ShortestPathsGraph
from algpy_src.data_structures.graphs.trees.heaps.fibonacci_heap import FibonacciHeap


class DijkstraShortestPathsAlgorithm(Algorithm[Graph | DiGraph, GraphSize]):
    """
    Dijkstra's shortest path(s) algorithm.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def algorithm_properties(self) -> AlgorithmProperties:
        return AlgorithmProperties(
            name="Uni-directional Dijsktra's Shortest Path(s) Algorithm",
            algorithm_family=AlgorithmFamily.GRAPH_TRAVERSAL,
            is_deterministic=True,
            best_case_time_complexity='1',
            best_case_description='starting from searched for element',
            average_case_time_complexity='|E| + |V| * log(|V|)',
            worst_case_time_complexity='|V| * [|E| + |V| * log(|V|)]',
            worst_case_description='all-pairs shortest paths',
            space_complexity='|V|^2',
        )

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
        return {'input_instance': g, 'source': NoNode(), 'target': NoNode()}

    def run_algorithm(self, input_instance: Graph | DiGraph, verbosity_level: VERBOSITY_LEVELS = 0, source: Node | NoNode = NoNode(),
                      target: Node | NoNode = NoNode(), fill_weight_value: Optional[float | int] = None, *args: Any, **kwargs: Any) -> tuple[bool, ShortestPathsGraph]:
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
        fill_weight_value : Optional[float | int] (default None)
            If given and None weight is encountered, fill the None with this value. Otherwise, an error will be raised.
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
        self.reset_n_ops()
        if source != NoNode() and source not in input_instance.nodes or target != NoNode() and target not in input_instance.nodes:
            raise ValueError('Either source or target node which are not present in the graph were given.')

        shortest_paths_lengths: dict[Node, dict[Node, int | float]] = {}
        shortest_paths_predecessors: dict[Node, dict[Node, Node | NoNode]] = {}

        sources = [source] if source != NoNode() else input_instance.nodes
        target_node_found = True if target == NoNode() else False

        for src in sources:
            success, single_source_sp_lengths, single_source_sp_predecessors = self._run_algorithm_single_source(input_instance, src, target, verbosity_level, fill_weight_value)
            if success:
                target_node_found = True
            shortest_paths_lengths[src] = single_source_sp_lengths
            shortest_paths_predecessors[src] = single_source_sp_predecessors

        if not target_node_found:
            return_graph = ShortestPathsGraph(input_instance.adjacency_list, {}, {})
        else:
            return_graph = ShortestPathsGraph(input_instance.adjacency_list, shortest_paths_lengths, shortest_paths_predecessors)

        print_problem_instance(return_graph, verbosity_level, 1)
        return target_node_found, return_graph

    def _run_algorithm_single_source(
            self, input_instance: Graph | DiGraph, source: Node, target: Node | NoNode = NoNode(),
            verbosity_level: VERBOSITY_LEVELS = 0, fill_weight_value: Optional[float | int] = None
    ) -> tuple[bool, dict[Node, int | float], dict[Node, Node | NoNode]]:
        """
        Convenience run function of Dijkstra's uni-directional shortest path(s) algorithm with a single source.

        Parameters
        ----------
        input_instance : Graph | DiGraph
            Graph in which to run the search.
        source : Node
            Root node to find the shortest path(s) from. Has to be given.
        target : Node | NoNode (default NoNode())
            Target node to find the shortest path(s) to. If not given, shortest paths to all nodes are found.
        verbosity_level : int (default 0)
            Select the amount of information to print throughout run of the algorithm.
            One of 0, 1, 2 with 0 referring to no printing, 1 leading to print the shortest path traversal graph at the end and
            2 meaning also print the shortest path traversal graph after every expanded node.
        fill_weight_value : Optional[float | int] (default None)
            If given and None weight is encountered, fill the None with this value. Otherwise, an error will be raised.

        Returns
        -------
        result : tuple[bool, dict[Node, int | float], dict[Node, Node | NoNode]]
            Returns True in the first index if the shortest path to target was found or if no target was specified.
            In the next two positions, return lengths of shortest paths from the given source to other nodes and the predecessors on the respective paths.
        """
        sp_lengths: dict[Node, int | float] = {source: 0}
        sp_predecessors: dict[Node, Node | NoNode] = {source: NoNode()}
        target_node_found = True if target == NoNode() else False

        to_visit: FibonacciHeap[Node, int | float] = FibonacciHeap()
        for node in input_instance.nodes:
            priority = float('inf') if node != source else 0
            to_visit.insert(node, priority)

        while not to_visit.is_empty:
            self.increment_n_ops()
            min_node = to_visit.extract_min_node()
            if isinstance(min_node, NoNode):
                raise IndexError('Fibonacci heap is said to not be empty while the extracted min node is a NoNode() object.')
            v_min = min_node.key
            print_problem_instance(sp_lengths, verbosity_level, 2)

            if v_min == target:
                self.increment_n_ops(to_visit.n_ops)
                return min_node.priority < float('inf'), sp_lengths, sp_predecessors

            for neighbour in input_instance.neighbors(v_min):
                weight = input_instance.get_edge_data(v_min, neighbour)
                if weight is None:
                    weight = fill_weight_value
                if not isinstance(weight, int | float):
                    raise ValueError('Edge weight is not of numeric type.')
                if weight < 0:
                    raise ValueError("Dijkstra's shortest path algorithm expects non-negative weights.")

                alt = sp_lengths.get(v_min, float('inf')) + weight
                if alt < sp_lengths.get(neighbour, float('inf')):
                    neighbour_in_heap = to_visit.find(neighbour)
                    if isinstance(neighbour_in_heap, NoNode):
                        continue
                    to_visit.decrease_priority(neighbour_in_heap, alt)
                    sp_lengths[neighbour] = alt
                    sp_predecessors[neighbour] = v_min

        self.increment_n_ops(to_visit.n_ops)
        return target_node_found, sp_lengths, sp_predecessors
