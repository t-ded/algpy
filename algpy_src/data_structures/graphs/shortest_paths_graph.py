from algpy_src.base.constants import Node, SingleEdgeData
from algpy_src.data_structures.graphs.digraph import DiGraph
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode
from algpy_src.data_structures.graphs.traversal_graph import TraversalGraph
from algpy_src.data_structures.linear.stack import Stack


class ShortestPathsGraph(DiGraph):

    def __init__(self, adjacency_list: dict[Node, dict[Node, SingleEdgeData]], shortest_path_lengths: dict[Node, dict[Node, int | float]],
                 shortest_path_predecessors: dict[Node, dict[Node, Node | NoNode]]) -> None:
        """
        Constructor of the ShortestPathsGraph class.

        Parameters
        ----------
        adjacency_list : adjacency_list: Optional[dict[Node, dict[Node, SingleEdgeData]]] (default None)
            Optional adjacency list from which to build the shortest paths graph.
        shortest_path_lengths : dict[Node, dict[Node, int | float]]
            Mapping of shortest path lengths from node i to node j.
        shortest_path_predecessors : dict[Node, dict[Node, Node | NoNode]]
            Mapping of predecessors of node j on shortest path from node i.
        """
        super().__init__(adjacency_list)
        self._shortest_path_lengths = shortest_path_lengths
        self._shortest_path_predecessors = shortest_path_predecessors

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, ShortestPathsGraph) and self._adjacency_list == other.adjacency_list and
                self._shortest_path_lengths == other._shortest_path_lengths and self._shortest_path_predecessors == other._shortest_path_predecessors)

    @property
    def name(self) -> str:
        return 'Shortest Paths Graph'

    @property
    def shortest_path_lengths(self) -> dict[Node, dict[Node, int | float]]:
        return self._shortest_path_lengths

    @property
    def shortest_path_predecessors(self) -> dict[Node, dict[Node, Node | NoNode]]:
        return self._shortest_path_predecessors

    def shortest_path_length(self, source: Node, target: Node) -> int | float:
        """
        Return length of the shortest path between two nodes or inf if such path does not exist.

        Parameters
        ----------
        source : Node
            Starting node.
        target : Node
            End node.

        Returns
        -------
        shortest_path_length : int | float
            Length of the shortest path from source to target or inf if such path does not exist.
        """
        return self._shortest_path_lengths.get(source, {}).get(target, float('inf'))

    def shortest_path(self, source: Node, target: Node) -> TraversalGraph | None:
        """
        Return the shortest path between two nodes as line traversal graph if it exists.

        Parameters
        ----------
        source : Node
            Starting node.
        target : Node
            End node.

        Returns
        -------
        shortest_path_graph : TraversalGraph | None
            Shortest path from source to target given as line traversal graph or None if it does not exist.
        """
        if self.shortest_path_length(source, target) == float('inf'):
            return None
        shortest_path_nodes: Stack[Node] = Stack()
        shortest_path_nodes.push(target)
        if target == source:
            one_node_traversal_graph = TraversalGraph()
            one_node_traversal_graph.add_node(source)
            return one_node_traversal_graph

        predecessor = self._shortest_path_predecessors[source][target]
        while not isinstance(predecessor, NoNode):
            shortest_path_nodes.push(predecessor)
            if predecessor == source:
                return self._reconstruct_path(shortest_path_nodes)
            predecessor = self._shortest_path_predecessors[source][predecessor]
        return None

    def _reconstruct_path(self, reverse_order_nodes: Stack[Node]) -> TraversalGraph:
        """
        Convenience function to reconstruct the path from a stack of nodes in reverse order.

        Parameters
        ----------
        reverse_order_nodes : Stack[Node]
            Stack of nodes, whose LIFO order corresponds to the desired path order.

        Returns
        -------
        path_graph : TraversalGraph
            Line traversal graph corresponding to the LIFO order of the given stack.
        """
        current = reverse_order_nodes.pop()
        path_graph: TraversalGraph = TraversalGraph()
        path_graph.add_node(current)

        while not reverse_order_nodes.is_empty:
            following = reverse_order_nodes.pop()
            path_graph.add_edge((current, following, self._adjacency_list[current].get(following, 0)))
            current = following

        return path_graph
