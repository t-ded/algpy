from algpy_src.tests.test_utils.base_objects import ExampleComplexityObject


def test_complexity_object():
    obj = ExampleComplexityObject()
    assert obj.name == 'Example Complexity Object'
