from base.complexity_object import ComplexityObject


class ExampleComplexityObject(ComplexityObject):

    @property
    def name(self) -> str:
        return 'Example Complexity Object'


def test_complexity_object():
    obj = ExampleComplexityObject()
    assert obj.name == 'Example Complexity Object'
