from typing import Iterable, Any

import pytest

from algpy_src.data_structures.linear.queue import Queue


@pytest.fixture
def queue() -> Queue:
    return Queue()


def test_queue_base(queue: Queue) -> None:
    assert queue.name == "Queue"
    assert queue.size == 0
    assert queue.is_empty is True
    assert queue.space_complexity == 'n'


@pytest.mark.parametrize(
    ('in_stream', ),
    [
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], id='Numbers'),
        pytest.param(['a', 'b', 'c'], id='Letters'),
        pytest.param(['a', 2, 'c', 4], id='Combination'),
        pytest.param(['a', None, 'c'], id='Include None'),
    ]
)
def test_queue_in_out(queue: Queue, in_stream: Iterable[Any]) -> None:

    for element in in_stream:
        assert queue.is_empty is True

        queue.enqueue(element)
        assert queue.is_empty is False
        assert queue.size == 1
        assert queue.peek() == element

        assert queue.dequeue() == element
        with pytest.raises(IndexError):
            queue.peek()
        assert queue.is_empty is True
