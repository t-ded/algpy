from contextlib import nullcontext as does_not_raise

import pytest

from algpy_src.data_structures.system_design.load_task import LoadTask
from algpy_src.data_structures.system_design.server import Server


@pytest.fixture
def default_server() -> Server:
    return Server(identifier='Base-Infinite-Capacity-Server')


@pytest.fixture
def capacity_server() -> Server:
    return Server(identifier='Capacity-100-Server', capacity=100.0)


class TestServer:

    def test_server_basic(self, default_server: Server) -> None:

        server_1 = Server(identifier='Base-Infinite-Capacity-Server')
        server_2 = Server(identifier='Not-Base-Infinite-Capacity-Server')
        assert server_1 == default_server
        assert server_2 != default_server

        assert str(default_server) == 'Server (id=Base-Infinite-Capacity-Server, current_load=0, capacity=inf)'
        default_server.add_task(LoadTask(identifier='test_1', size=10_000.0))
        assert str(default_server) == 'Server (id=Base-Infinite-Capacity-Server, current_load=10_000, capacity=inf)'

    def test_infinite_capacity_task_loading(self, default_server: Server) -> None:

        expected_load = 0.0
        for i, task_size in enumerate([10 ** 10, 20 ** 10, 30 ** 10, 40 ** 10]):
            task = LoadTask(identifier=f'test_{i}', size=task_size)
            default_server.add_task(task)
            expected_load += task_size
            assert default_server.current_load == expected_load

    def test_limited_capacity_server(self, capacity_server: Server) -> None:

        task_1 = LoadTask(identifier='test_1', size=100.0)
        task_2 = LoadTask(identifier='test_2', size=100.0)

        capacity_server.add_task(task_1)
        assert capacity_server.current_load == 100.0
        assert capacity_server.can_handle_task(task_2) is False
        with pytest.raises(MemoryError):
            capacity_server.add_task(task_2)

        capacity_server.remove_task(task_1)
        assert capacity_server.current_load == 0
        assert capacity_server.can_handle_task(task_2) is True
        with does_not_raise():
            capacity_server.add_task(task_2)
