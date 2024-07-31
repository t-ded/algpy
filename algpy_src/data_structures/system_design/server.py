import logging
from typing import Any

import numpy as np

from algpy_src.data_structures.data_structure import DataStructure


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
        self._load = 0.0
        self._capacity = capacity
        self._identifier = identifier

    def __str__(self) -> str:
        return f'Server (id={self._identifier}, current_load={self._load}), capacity={self._capacity}'

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
        return self._load

    def can_handle_load(self, load: float) -> bool:
        """
        Convenience function to check if adding given load overflows capacity of the server.

        Parameters
        ----------
        load : float
            New load to be added to the current load of the server.

        Returns
        -------
        can_handle : bool
            Whether the given new load can be handled by the server.
        """
        return self._load + load <= self._capacity

    def add_load(self, load: float) -> None:
        """
        Adds a new load to the server. If this overflows capacity, MemoryError is raised.

        Parameters
        ----------
        load : float
            Load to add to the current load of the server.
        """
        if not self.can_handle_load(load):
            raise MemoryError('Capacity of the server exceeded')
        self._load += load

    def remove_load(self, load: float) -> None:
        """
        Removes desired load from the server. If the desired amount is more than present amount, all present load is removed.

        Parameters
        ----------
        load : float
            Load to remove from the current load of the server.
        """
        if self._load - load < 0:
            logging.warning(f'Tried removing more load than currently present in server {self.identifier}. Removing all present load instead.')
        self._load = max(0.0, self._load - load)
