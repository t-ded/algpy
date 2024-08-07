from algpy_src.tests.test_utils.example_base_objects import ExampleComplexityObject


def test_complexity_object():
    obj = ExampleComplexityObject()
    assert obj.name == 'Example Complexity Object'
    assert obj.n_ops == 0
    obj.increment_n_ops(5)
    assert obj.n_ops == 5
    obj.reset_n_ops()
    assert obj.n_ops == 0
