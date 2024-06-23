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
