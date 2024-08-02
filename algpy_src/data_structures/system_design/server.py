from typing import Any

import numpy as np

from algpy_src.base.utils import underscore_formatter
from algpy_src.data_structures.data_structure import DataStructure
from algpy_src.data_structures.system_design.load_task import LoadTask


class Server(DataStructure):
    """
    Class for simple servers used for demonstrative purposes in system design algorithms such as load balancing.
    """

    def __init__(self, capacity: float = np.inf, identifier: Any = 0) -> None:
        """
        Constructor of the Server class. Sets up a mock server object that is capable of handling load up to desired capacity.

        Parameters
        ----------
        capacity : Optional[float] (default: np.inf)
            Capacity of the server object. If not given, infinite capacity is assumed.
        identifier : Any (default: 0)
            Identifier for the server.
        """
        super().__init__()
        self._capacity = capacity
        self._identifier = identifier
        self._tasks: list[LoadTask] = []

    def __str__(self) -> str:
        load_str = underscore_formatter(self.current_load) if self.current_load > 1_000 else self.current_load
        capacity_str = underscore_formatter(self._capacity) if (self._capacity is not np.inf and self._capacity > 1_000) else self._capacity
        return f'Server (id={self._identifier}, current_load={load_str}, capacity={capacity_str})'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Server) and self._identifier == other._identifier

    def __hash__(self) -> int:
        return hash(self._identifier)

    @property
    def name(self) -> str:
        return 'Server'

    @property
    def space_complexity(self) -> str:
        return 'n'

    @property
    def identifier(self) -> Any:
        return self._identifier

    @property
    def capacity(self) -> float:
        return self._capacity

    @property
    def current_load(self) -> float:
        return sum(task.size for task in self._tasks)

    @property
    def tasks(self) -> list[LoadTask]:
        return self._tasks

    def can_handle_task(self, task: LoadTask) -> bool:
        """
        Convenience function to check if adding given load task overflows capacity of the server.

        Parameters
        ----------
        task : LoadTask
            New load task to be added to the current load of the server.

        Returns
        -------
        can_handle : bool
            Whether the given new task can be handled by the server.
        """
        return self.current_load + task.size <= self._capacity

    def add_task(self, task: LoadTask) -> None:
        """
        Adds a new load task to the server. If this overflows capacity, MemoryError is raised.

        Parameters
        ----------
        task : LoadTask
            Load to add to the current load of the server.
        """
        if not self.can_handle_task(task):
            raise MemoryError('Capacity of the server exceeded')
        self._tasks.append(task)

    def remove_task(self, task: LoadTask) -> None:
        """
        Removes desired load task from the server.

        Parameters
        ----------
        task : LoadTask
            Load task to remove from the current load of the server.
        """
        self._tasks.remove(task)
