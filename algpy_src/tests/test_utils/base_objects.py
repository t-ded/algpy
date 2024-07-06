from algpy_src.base.complexity_object import ComplexityObject


class ExampleComplexityObject(ComplexityObject):

    @property
    def name(self) -> str:
        return 'Example Complexity Object'

    @property
    def space_complexity(self) -> str:
        return 'N/A'
