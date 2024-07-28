import pytest

from algpy_src.base.constants import Edge
from algpy_src.data_structures.graphs.feature_graph import FeatureGraph
from algpy_src.data_structures.graphs.graph_utils.no_node_object import NoNode


@pytest.fixture
def line_feature_graph_empty_features() -> FeatureGraph:

    nodes: list[int] = [1, 2, 3, 4, 5]
    edges: list[Edge] = [(1, 2, None), (2, 3, None), (3, 4, None), (4, 5, None)]

    fg: FeatureGraph = FeatureGraph()
    fg.add_nodes_from(nodes)
    fg.add_edges_from(edges)

    return fg


@pytest.fixture
def line_feature_graph_with_features(line_feature_graph_empty_features: FeatureGraph) -> FeatureGraph:

    node_features: dict[int, str] = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
    edges: list[Edge] = [(1, 2, None), (2, 3, None), (3, 4, None), (4, 5, None)]

    fg: FeatureGraph = FeatureGraph()
    fg.add_nodes_with_features_from(node_features)
    fg.add_edges_from(edges)
    return fg


def test_feature_inequality(line_feature_graph_empty_features: FeatureGraph, line_feature_graph_with_features: FeatureGraph) -> None:
    fg1 = line_feature_graph_empty_features
    fg2 = line_feature_graph_with_features
    print(fg1.node_features)
    print(fg2.node_features)
    assert fg1 != fg2


def test_basic_methods(line_feature_graph_with_features: FeatureGraph) -> None:

    line_feature_graph_with_features.add_node_with_features(6, '6')
    assert line_feature_graph_with_features.get_node_features(6) == '6'

    line_feature_graph_with_features.add_node_with_features(6, '60')
    assert line_feature_graph_with_features.get_node_features(6) == '60'

    line_feature_graph_with_features.remove_node(6)
    assert line_feature_graph_with_features.get_node_features(6) == NoNode()
