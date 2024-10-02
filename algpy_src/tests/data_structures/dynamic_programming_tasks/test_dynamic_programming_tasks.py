from algpy_src.data_structures.dynamic_programming_tasks.fibonacci_task import NThFibonacciNumberTask
from algpy_src.data_structures.dynamic_programming_tasks.zero_one_knapsack_task import ZeroOneKnapsackTask, ZeroOneKnapsackTaskState


class TestDynamicProgrammingTasks:

    def test_nth_fib_number(self) -> None:
        fib = NThFibonacciNumberTask(2)
        assert fib.is_optimization is False
        value_comp = fib.value_computation()
        assert value_comp[0] == []
        assert value_comp[1]() == 1
        assert fib.value_computation()[0] == [], lambda: 1
        for n in range(3, 20):
            assert fib.state == n - 1
            fib.set_state(n)
            assert fib.state == n
            value_comp = fib.value_computation()
            assert value_comp[0] == [n - 1, n - 2]
            assert value_comp[1](n - 1, n - 2) == 2 * n - 3

    def test_knapsack(self) -> None:
        knapsack = ZeroOneKnapsackTask(10, [2, 5, 8], [20, 50, 80])
        assert knapsack.is_optimization is True
        assert knapsack.value_computation()[0] == []
        assert knapsack.value_computation()[1]() == 0
        assert knapsack.get_state_transitions() == [
            ZeroOneKnapsackTaskState(*(2, 20, 1)),
            ZeroOneKnapsackTaskState(*(0, 0, 1)),
            ZeroOneKnapsackTaskState(*(5, 50, 2)),
            ZeroOneKnapsackTaskState(*(0, 0, 2)),
            ZeroOneKnapsackTaskState(*(8, 80, 3)),
            ZeroOneKnapsackTaskState(*(0, 0, 3)),
        ]
        knapsack.set_state(ZeroOneKnapsackTaskState(8, 80, 3))
        assert knapsack.value_computation()[0] == []
        assert knapsack.value_computation()[1]() == 80
        assert knapsack.get_state_transitions() == []