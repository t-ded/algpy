from typing import Callable, Any


def affects_adjacency_matrix(func: Callable) -> Callable:
    """
    Decorator to specify that the given method affects adjacency matrix, thus its cache is not usable anymore.

    Parameters
    ----------
    func : Callable
        The function to decorate.
        This decorator is used as an identifier of this function rendering the graph's adjacency matrix cache unusable.

    Returns
    -------
    wrapper : Callable
        The wrapper for the input function.
    """
    def wrapper(self, *args, **kwargs) -> Any:
        self._adjacency_matrix = []
        self._adjacency_matrix_is_actual = False
        return func(self, *args, **kwargs)
    return wrapper
