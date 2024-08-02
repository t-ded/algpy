from typing import Optional

import numpy as np
import pytest

from algpy_src.algorithms.load_balancing.round_robin import RoundRobinAlgorithm
from algpy_src.base.constants import LoadBalancingTaskSize
from algpy_src.data_structures.system_design.load_task import LoadTask
from algpy_src.data_structures.system_design.server import Server


@pytest.fixture
def round_robin() -> RoundRobinAlgorithm:
    return RoundRobinAlgorithm()


def test_round_robin_basics(round_robin: RoundRobinAlgorithm) -> None:
    assert round_robin.name == 'Round Robin'
    assert round_robin.is_deterministic is True
    assert round_robin.best_case_time_complexity == round_robin.average_case_time_complexity == round_robin.worst_case_time_complexity == 'n'
    assert round_robin.space_complexity == '1'
    assert round_robin.best_case_description == round_robin.worst_case_description == 'irrelevant - with this variant, all inputs require exactly one pass through the entire task list'


def test_round_robin_default_worst_case_arguments(round_robin: RoundRobinAlgorithm) -> None:
    assert round_robin.get_worst_case_arguments(LoadBalancingTaskSize(*(100, 100))) == {'input_instance': ([LoadTask(identifier='worst_case', size=1)], [Server()])}


def test_round_robin_weights_do_not_support_invalid_input(round_robin: RoundRobinAlgorithm) -> None:
    with pytest.raises(ValueError):
        round_robin.run_algorithm(input_instance=([], [Server()]), server_weights={Server(): -5})


@pytest.mark.parametrize(
    ('server_capacities', 'server_weights', 'task_loads', 'expected_task_assignment'),
    [
        pytest.param([np.inf], None, [10, 20, 30, 40, 50], [0, 0, 0, 0, 0], id='One server which can handle all'),
        pytest.param([100], None, [10, 20, 30, 40, 50, 50, 0], [0, 0, 0, 0, None, None, 0], id='One server which has to skip two'),
        pytest.param([np.inf, np.inf, np.inf], None, [10, 20, 30, 10, 20, 30], [0, 1, 2, 0, 1, 2], id='Three servers which can handle all'),
        pytest.param([np.inf, np.inf, 0], None, [10, 20, 30, 10, 20, 30], [0, 1, None, 0, 1, None], id='Three servers but third cannot handle anything'),
        pytest.param([np.inf, np.inf], {1: 2}, [10, 20, 30, 40, 50, 60, 70], [0, 1, 1, 0, 1, 1, 0], id='Two servers, one has double weight'),
    ]
)
def test_round_robin_run_algorithm(
        round_robin: RoundRobinAlgorithm, server_capacities: list[float], server_weights: Optional[dict[int, int]],
        task_loads: list[float], expected_task_assignment: list[int | None]
) -> None:

    servers = [Server(capacity=server_capacity, identifier=f'test_server_{i}') for i, server_capacity in enumerate(server_capacities)]
    tasks = [LoadTask(identifier=f'test_task_{i}', size=task_load) for i, task_load in enumerate(task_loads)]

    server_weights_mapping: Optional[dict[Server, int]] = None
    if server_weights is not None:
        server_weights_mapping = {}
        for index, weight in server_weights.items():
            server_weights_mapping[servers[index]] = weight

    all_assigned, (unassigned, servers_with_assignment) = round_robin.run_algorithm(input_instance=(tasks, servers), server_weights=server_weights_mapping)

    assert all_assigned is (None in expected_task_assignment)
    for task, expected_assignment in zip(tasks, expected_task_assignment):
        if expected_assignment is None:
            assert task in unassigned
        else:
            assert task in servers_with_assignment[expected_assignment].tasks
    assert round_robin.n_ops == len(tasks)
