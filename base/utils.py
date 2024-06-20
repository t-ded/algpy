import numpy as np
import time
from typing import Iterable

from algorithms.algorithm import Algorithm


def time_alg_runtime(alg: Algorithm, input_size: int | Iterable[int], n: int = 10, *args, **kwargs) -> None:

    runtimes: list[float] = []
    for _ in range(n):
        input_instance = alg.generate_random_input(input_size)
        start = time.time()
        alg.run_algorithm(input_instance, args, kwargs)
        runtimes.append(time.time() - start)

    avg = np.mean(runtimes)
    std = np.std(runtimes)
    print(f'\tRun with input size {input_size} took {avg:_.2f}', u'\u00B1', f'{std:_2f} seconds ({n=} samples)')

