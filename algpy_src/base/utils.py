from typing import Any

from algpy_src.base.constants import VERBOSITY_LEVELS, ProblemInstance


def print_delimiter(delimiter: str = '-', n: int = 10) -> None:
    """
    Prints the given delimiter for n times

    Parameters
    ----------
    delimiter : str (default '-')
        Delimiter to print.
    n : int (default 10)
        Number of delimiter's repetitions.
    """
    print(delimiter * n)

    
def print_gap(n: int = 3) -> None:
    """
    Prints n empty rows.

    Parameters
    ----------
    n : int (default 3)
        Number of rows to print.
    """
    print_delimiter('\n', n)


def print_problem_instance(instance: ProblemInstance, verbosity_level: VERBOSITY_LEVELS, min_verbosity_level: int = 1) -> None:
    """
    Convenience function to print the given ProblemInstance if the current verbosity_level is greater than or equal to min_verbosity_level.
    Parameters
    ----------
    instance : ProblemInstance
        ProblemInstance to print.
    verbosity_level : int
        The amount of information to print throughout run of the algorithm.
        One of 0, 1, 2 with 0 typically referring to no printing, 1 leading to print of given ProblemInstance before and after and 2 meaning every step.
    min_verbosity_level : int (default 0)
        Minimal verbosity level needed for the print to happen.
    """
    if verbosity_level >= min_verbosity_level:
        print(instance)


def underscore_formatter(x: int | float, *args: Any) -> str:
    """
    Convert the given input to integer and return it in underscore-formatted string form.

    Parameters
    ----------
    x : int | float
        The input numeric value to format.
    *args : Any
        Other arguments (e.g., 'pos' passed by matplotlib).

    Returns
    ----------
    formatted_input : str
        Return the given input value as integer in underscore-formatted string form.
    """
    return f'{int(x):_}'
