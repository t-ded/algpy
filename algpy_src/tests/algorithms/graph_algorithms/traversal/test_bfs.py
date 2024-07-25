import pytest

from algpy_src.algorithms.graph_algorithms.traversal.bfs import BreadthFirstSearch
from algpy_src.base.constants import GraphSize
from algpy_src.data_structures.graphs.graph import Graph


@pytest.fixture
def bfs() -> BreadthFirstSearch:
    return BreadthFirstSearch()


def test_bfs_base(bfs: BreadthFirstSearch) -> None:
    assert bfs.name == 'Breadth First Search'
    assert bfs.best_case_time_complexity == '1'
    assert bfs.best_case_description == 'starting from searched for element'
    assert bfs.average_case_time_complexity == '|V| + |E|'
    assert bfs.worst_case_time_complexity == '|V| + |E|'
    assert bfs.worst_case_description == 'searched for element not present in the graph'
    assert bfs.space_complexity == '|V|'
    assert bfs.get_worst_case_arguments(GraphSize(*(5, 5))) == {
        'input_instance': Graph({0: {1: None, 2: None, 3: None, 4: None}, 1: {0: None, 2: None}, 2: {0: None, 1: None}, 3: {0: None}, 4: {0: None}}),
        'element_to_search': 6
    }
