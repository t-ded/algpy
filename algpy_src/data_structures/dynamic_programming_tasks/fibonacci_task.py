from algpy_src.data_structures.dynamic_programming_tasks.generic_dynamic_programming_task import GenericDynamicProgrammingTask


class NThFibonacciNumber(GenericDynamicProgrammingTask[int, int]):

    def __init__(self, n: int) -> None:
        super().__init__()
        self._n = n

    def get_state_value(self, state: int) -> int:
        if state <= 1:
            return 1
        return self.get_state_value(state - 1) + self.get_state_value(state - 2)
