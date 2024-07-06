from algpy_src.algorithms.algorithm import Algorithm


def print_time_complexity_info_algorithm(algorithm: Algorithm) -> None:
    """
    Print the time complexity information of the given algorithm.

    Parameters
    ----------
    algorithm : Algorithm
        Algorithm whose time complexity info to print.
    """
    print(f'Time complexity breakdown of the {algorithm.name} algorithm:')
    print(f'\tBest case time complexity is O({algorithm.best_case_time_complexity}) with best case being {algorithm.best_case_description}.')
    print(f'\tAverage case time complexity is O({algorithm.average_case_time_complexity}).')
    print(f'\tWorst case time complexity is O({algorithm.worst_case_time_complexity}) with worst case being {algorithm.worst_case_description}.')
