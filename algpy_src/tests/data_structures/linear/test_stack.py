from typing import Iterable, Any

import pytest

from algpy_src.data_structures.linear.stack import Stack


@pytest.fixture
def stack() -> Stack:
    return Stack()


def test_stack_base(stack: Stack) -> None:
    assert stack.name == "Stack"
    assert stack.size == 0
    assert stack.is_empty is True
    assert stack.space_complexity == 'n'


@pytest.mark.parametrize(
    ('in_stream', ),
    [
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Numbers'),
        pytest.param(['a', 'b', 'c'], id='Letters'),
        pytest.param(['a', 2, 'c', 4], id='Combination'),
        pytest.param(['a', None, 'c'], id='Include None'),
    ]
)
def test_stack_in_out(stack: Stack, in_stream: Iterable[Any]) -> None:

    for element in in_stream:
        assert stack.is_empty is True

        stack.push(element)
        assert stack.is_empty is False
        assert stack.size == 1
        assert stack.peek() == element

        assert stack.pop() == element
        assert stack.peek() is None
        with pytest.raises(IndexError):
            stack.pop()
        assert stack.is_empty is True


@pytest.mark.parametrize(
    ('in_stream', ),
    [
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Numbers'),
        pytest.param(['a', 'b', 'c'], id='Letters'),
        pytest.param(['a', 2, 'c', 4], id='Combination'),
        pytest.param(['a', None, 'c'], id='Include None'),
    ]
)
def test_ordering(stack: Stack, in_stream: list[Any]) -> None:

    for element in in_stream:
        stack.push(element)

    i = 1
    while not stack.is_empty:
        assert stack.pop() == in_stream[-i]
        i += 1
