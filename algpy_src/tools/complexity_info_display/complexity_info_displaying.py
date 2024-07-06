from algpy_src.algorithms.algorithm import Algorithm
from algpy_src.base.complexity_object import ComplexityObject
from algpy_src.base.constants import COMPLEXITIES
from algpy_src.base.utils import print_delimiter
from algpy_src.data_structures.data_structure import DataStructure
from algpy_src.tools.complexity_info_display.algorithms_complexity_info_displays import print_time_complexity_info_algorithm
from algpy_src.tools.complexity_info_display.data_structures_complexity_info_display import print_time_complexity_info_data_structure


def print_space_complexity_info(complexity_object: ComplexityObject) -> None:
    """
    Print the space complexity information of the given complexity object.

    Parameters
    ----------
    complexity_object : ComplexityObject
        Complexity object whose space complexity info to print.
    """
    obj_type = 'data structure' if isinstance(complexity_object, DataStructure) else 'algorithm'
    print(f'Space complexity of the {complexity_object.name} {obj_type} is O({complexity_object.space_complexity}).')


def print_time_complexity_info(complexity_object: ComplexityObject) -> None:
    """
    Print the time complexity information of the given complexity object.

    Parameters
    ----------
    complexity_object : ComplexityObject
        Complexity object whose time complexity info to print.
    """
    if isinstance(complexity_object, DataStructure):
        print(f'Time complexity breakdown of the {complexity_object.name} data structure:')
        print_time_complexity_info_data_structure(complexity_object)
    elif isinstance(complexity_object, Algorithm):
        print(f'Time complexity breakdown of the {complexity_object.name} algorithm:')
        print_time_complexity_info_algorithm(complexity_object)


def print_complexity_info(complexity_object: ComplexityObject, which: COMPLEXITIES = 'both') -> None:
    """
    Print the complexity information for the complexity object.

    Parameters
    ----------
    complexity_object : ComplexityObject
        Complexity object whose complexity info to print.
    which : str (default 'both')
        What kind of complexity info to print (one of 'time', 'space' or 'both').
    """
    print_delimiter()
    if which == 'time' or which == 'both':
        print_time_complexity_info(complexity_object)
        print_delimiter(n=5)
    if which == 'space' or which == 'both':
        print_space_complexity_info(complexity_object)
    print_delimiter()
