from algpy_src.base.complexity_object import ComplexityObject


class ExampleComplexityObject(ComplexityObject):

    @property
    def name(self) -> str:
        return 'Example Complexity Object'

    def print_time_complexity_info(self) -> None:
        """
        Print the time complexity information of the example complexity object.
        """
        raise NotImplementedError()

    def print_space_complexity_info(self) -> None:
        """
        Print the space complexity information of the example complexity object.
        """
        raise NotImplementedError()
