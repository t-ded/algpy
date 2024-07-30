from typing import Optional, TypeVar

import pytest

from algpy_src.algorithms.graph_algorithms.message_passing.relational_classification import RelationalClassificationAlgorithm
from algpy_src.base.constants import Node, SingleEdgeData
from algpy_src.data_structures.graphs.feature_graph import FeatureGraph

F = TypeVar('F')


@pytest.fixture
def relational_classification() -> RelationalClassificationAlgorithm:
    return RelationalClassificationAlgorithm()


def test_relational_classification_worst_case(relational_classification: RelationalClassificationAlgorithm) -> None:
    worst_case_args = relational_classification.get_worst_case_arguments()
    expected_feature_graph: FeatureGraph = FeatureGraph({1: {2: True}})
    expected_feature_graph.add_nodes_with_features_from({1: 0, 2: 1})
    assert relational_classification.run_algorithm(**worst_case_args) == (False, expected_feature_graph)


@pytest.mark.parametrize(
    ('input_adjacency_list', 'input_node_features', 'expected_mapping'),
    [
        pytest.param({}, {}, {}, id='Empty graph'),
        pytest.param({1: {2: None}}, {}, None, id='Crashes on edge data other than int, float or bool'),
        pytest.param({1: {2: True}}, {1: 'Feature'}, None, id='Crashes on node data other than int, float or bool'),
        pytest.param({1: {2: True}}, {1: -1}, None, id='Crashes on int node data outside (0, 1) range'),
        pytest.param({1: {2: True}, 3: {2: True}}, {1: 1, 3: 1}, {1: 1, 2: 1, 3: 1}, id='Correctly propagates on toy example'),
        pytest.param({
            1: {2: True, 3: True, 4: True}, 2: {1: True, 3: True}, 3: {1: True, 2: True, 4: True}, 4: {1: True, 3: True, 5: True, 6: True}, 5: {4: True, 6: True, 7: True, 8: True},
            6: {4: True, 5: True, 7: True, 8: True}, 7: {5: True, 6: True, 8: True, 9: True}, 8: {5: True, 6: True, 7: True}, 9: {7: True}
        }, {1: 0, 2: 0, 6: 1, 7: 1}, {1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, id='Correctly propagates on example from the lecture'),
    ]
)
def test_relational_classification_run_algorithm(
        relational_classification: RelationalClassificationAlgorithm, input_adjacency_list: dict[Node, dict[Node, SingleEdgeData]],
        input_node_features: dict[Node, F], expected_mapping: Optional[dict[Node, F]]
) -> None:

    feature_graph: FeatureGraph = FeatureGraph(input_adjacency_list)
    feature_graph.add_nodes_with_features_from(input_node_features)

    if expected_mapping is not None:
        expected_feature_graph: FeatureGraph = FeatureGraph(input_adjacency_list)
        expected_feature_graph.add_nodes_with_features_from(expected_mapping)
        assert relational_classification.run_algorithm(feature_graph) == (True, expected_feature_graph)
    else:
        with pytest.raises(ValueError):
            relational_classification.run_algorithm(feature_graph)
