from algpy_src.data_structures.container import Container
from algpy_src.data_structures.data_structure import DataStructure


def print_time_complexity_info_container(container: Container) -> None:
    """
    Print the time complexity information of the given container.

    Parameters
    ----------
    container : Container
        Container whose time complexity info to print.
        Expected to have property methods for breaking down insert, search, delete time complexities and best and worst cases.
    """
    for operation in ['insert', 'delete', 'search']:
        print(f'  {operation.capitalize()}:')
        print(f'\tBest case time complexity is O({getattr(container, f"best_case_{operation}_time_complexity")}) with best case being',
              f'{getattr(container, f"best_case_{operation}_description")}.')
        print(f'\tAverage case time complexity is O({getattr(container, f"average_case_{operation}_time_complexity")}).')
        print(f'\tWorst case time complexity is O({getattr(container, f"worst_case_{operation}_time_complexity")}) with best case being ',
              f'{getattr(container, f"best_case_{operation}_description")}.')


def print_time_complexity_info_data_structure(data_structure: DataStructure) -> None:
    """
    Print the time complexity information of the given data structure.

    Parameters
    ----------
    data_structure : DataStructure
        Data structure whose time complexity info to print.
    """
    if isinstance(data_structure, Container):
        print_time_complexity_info_container(data_structure)
