from algpy_src.data_structures.system_design.load_task import LoadTask


def test_load_task_equivalence() -> None:

    task_1 = LoadTask('task', 50.0)
    task_2 = LoadTask('task_2', 50.0)
    task_3 = LoadTask('task', 150.0)

    assert task_1 != task_2
    assert task_1 == task_3


def test_load_task_string_representation() -> None:
    task_1 = LoadTask('task_1', 50.0)
    task_2 = LoadTask('task_2', 1_012_950.01025)
    assert str(task_1) == 'LoadTask (id=task_1, size=50.0)'
    assert str(task_2) == 'LoadTask (id=task_2, size=1_012_950)'
