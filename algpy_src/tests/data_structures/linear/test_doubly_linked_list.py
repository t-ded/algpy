import logging
from typing import TypeVar, Optional

import pytest

from algpy_src.data_structures.linear.linked_list import LinkedList

T = TypeVar('T')


@pytest.fixture()
def dll() -> LinkedList:
    return LinkedList(linked_list_type='doubly')


def traverse_and_check_equals_expected_sequence(ll: LinkedList, expected_state: list[T]):
    assert ll.length == len(expected_state)
    if len(expected_state) == 0:
        assert ll.head is None
        assert ll.tail is None
    else:
        current = ll.head
        pred = None
        for value in expected_state:
            assert current is not None
            assert current.value == value
            assert current.predecessor == pred
            pred = current
            current = current.successor
        assert ll.tail is not None
        assert ll.tail.value == expected_state[-1]
        assert ll.tail.successor is None
        if len(expected_state) == 1:
            assert ll.head == ll.tail
        else:
            assert ll.tail.predecessor is not None
            assert ll.tail.predecessor.value == expected_state[-2]


class TestDoublyLinkedList:

    def test_doubly_linked_list_base(self, dll: LinkedList) -> None:
        assert dll.name == 'Doubly Linked List'

        assert dll.best_case_insert_time_complexity == '1'
        assert dll.best_case_insert_description == 'index 0 or index -1'
        assert dll.average_case_insert_time_complexity == 'n'
        assert dll.worst_case_insert_time_complexity == 'n'
        assert dll.worst_case_insert_description == 'index equals half of length'

        assert dll.best_case_search_time_complexity == '1'
        assert dll.best_case_search_description == 'item in head'
        assert dll.average_case_search_time_complexity == 'n'
        assert dll.worst_case_search_time_complexity == 'n'
        assert dll.worst_case_search_description == 'item not present'

        assert dll.best_case_delete_time_complexity == '1'
        assert dll.best_case_delete_description == 'item in head or index -1'
        assert dll.average_case_delete_time_complexity == 'n'
        assert dll.worst_case_delete_time_complexity == 'n'
        assert dll.worst_case_delete_description == 'item at tail if index not provided, otherwise item in the middle'

    def test_insert_to_empty(self, dll: LinkedList) -> None:
        assert dll.head is None

        dll.insert_to_empty('A')
        assert dll.head is not None
        assert dll.head.value == 'A'
        assert dll.head.predecessor is None
        assert dll.head.successor is None
        assert dll.length == 1

    def test_insert_to_empty_via_insert(self, dll: LinkedList) -> None:
        assert dll.head is None

        dll.insert('A', 0)
        assert dll.head is not None
        assert dll.head.value == 'A'
        assert dll.head.predecessor is None
        assert dll.head.successor is None
        assert dll.length == 1

    def test_insert_index_out_of_bounds_does_nothing(self, dll: LinkedList, caplog) -> None:

        assert dll.head is None
        with caplog.at_level(logging.WARNING):
            dll.insert('A', 5)
        assert dll.head is None
        assert caplog.records[0].levelname == 'WARNING'
        assert caplog.records[0].message == 'Index out of range.'

        with caplog.at_level(logging.WARNING):
            dll.insert('A', -2)
        assert dll.head is None
        assert caplog.records[1].levelname == 'WARNING'
        assert caplog.records[1].message == 'Index out of range.'

    def test_insert_to_second_half_starts_from_tail(self, dll: LinkedList) -> None:
        vals_to_insert = [str(i) for i in range(100)]
        dll.insert('0', 0)
        for i, value in enumerate(vals_to_insert[1:]):
            dll.insert(value, -1)
            assert dll.n_ops == 3
            traverse_and_check_equals_expected_sequence(dll, vals_to_insert[:i + 2])

    @pytest.mark.parametrize(
        ('insert_value_sequence', 'insert_index_sequence', 'expected_state_after_insert'),
        [
            pytest.param([1], [0], [[1]], id='Insert one node to empty list index 0'),
            pytest.param([1], [-1], [[1]], id='Insert one node to empty list index -1'),
            pytest.param([1, 2], [0, 1], [[1], [1, 2]], id='Insert two nodes append'),
            pytest.param([1, 2], [-1, -1], [[1], [1, 2]], id='Append two nodes via index -1'),
            pytest.param([1, 0], [0, 0], [[1], [0, 1]], id='Insert two nodes prepend'),
            pytest.param([0, 2, 1], [0, 1, 1], [[0], [0, 2], [0, 1, 2]], id='Insert three nodes one in between'),
            pytest.param([0, 'B', None, (4, 5), ['6', '7']], [-1, -1, -1, -1, -1], [[0], [0, 'B'], [0, 'B', None], [0, 'B', None, (4, 5)], [0, 'B', None, (4, 5), ['6', '7']]],
                         id='Append various objects'),

        ]
    )
    def test_doubly_linked_list_insert(self, dll: LinkedList, insert_value_sequence: list[T], insert_index_sequence: list[int], expected_state_after_insert: list[list[T]]) -> None:
        assert dll.head is None
        for insert_value, insert_index, expected_state in zip(insert_value_sequence, insert_index_sequence, expected_state_after_insert):
            dll.insert(insert_value, insert_index)
            traverse_and_check_equals_expected_sequence(dll, expected_state)

    def test_invalid_delete_value_or_index_does_nothing(self, dll: LinkedList, caplog) -> None:

        assert dll.head is None
        try:
            dll.delete('A')
        except Exception as e:
            pytest.fail(f'Deletion with null head rose an error {e}')
        dll.insert('A', 0)
        with caplog.at_level(logging.WARNING):
            dll.delete('A', 2)
        assert caplog.records[0].levelname == 'WARNING'
        assert caplog.records[0].message == 'Index out of range.'
        try:
            dll.delete('B')
        except Exception as e:
            pytest.fail(f'Deletion of item which is not present rose an error {e}')

    def test_delete_in_second_half_starts_from_tail(self, dll: LinkedList) -> None:
        vals_to_insert = [str(i) for i in range(100)]
        dll.insert('0', 0)
        for i, value in enumerate(vals_to_insert[1:]):
            dll.insert(value, -1)
        for i, value in enumerate(vals_to_insert[:5:-1]):
            dll.delete(value, -1)
            assert dll.n_ops == 4
            traverse_and_check_equals_expected_sequence(dll, vals_to_insert[:(-i - 1)])

    @pytest.mark.parametrize(
        ('initial_state', 'delete_value_sequence', 'delete_index_sequence', 'expected_state_after_delete'),
        [
            pytest.param([0], [0], [None], [[]], id='Delete only item by value'),
            pytest.param([0], [0], [0], [[]], id='Delete only item by value and index 0'),
            pytest.param([0], [0], [-1], [[]], id='Delete only item by value and index -1'),
            pytest.param([0, 1], [0], [None], [[1]], id='Delete first item of two by value'),
            pytest.param([0, 1], [0], [0], [[1]], id='Delete first item of two by value and index 0'),
            pytest.param([0, 1], [1], [None], [[0]], id='Delete second item of two by value'),
            pytest.param([0, 1], [1], [-1], [[0]], id='Delete second item of two by value and index -1'),
            pytest.param([0, 1, 2], [1], [None], [[0, 2]], id='Delete middle item of three by value'),
            pytest.param([0, 1, 2], [1], [1], [[0, 2]], id='Delete middle item of three by value and index'),
            pytest.param([0, 0], [0], [None], [[0]], id='Delete first encountered value'),
        ]
    )
    def test_doubly_linked_list_delete(self, dll: LinkedList, initial_state: list[T], delete_value_sequence: list[T],
                                       delete_index_sequence: list[Optional[int]], expected_state_after_delete: list[list[Optional[T]]]) -> None:
        assert dll.head is None
        for insert_value in initial_state:
            dll.insert(insert_value, -1)
        for delete_value, delete_index, expected_state in zip(delete_value_sequence, delete_index_sequence, expected_state_after_delete):
            dll.delete(delete_value, delete_index)
            traverse_and_check_equals_expected_sequence(dll, expected_state)

    @pytest.mark.parametrize(
        ('initial_state', 'value_to_search', 'expected_result'),
        [
            pytest.param([], 1, None, id='Returns None on empty linked list'),
            pytest.param([0, 2, 3, 4], 1, None, id='Returns None if value not found'),
            pytest.param([0, 1], 1, 1, id='Returns correctly if value found'),
            pytest.param([1, 1, 1], 1, 0, id='Returns index of first value if multiple matching present'),
        ]
    )
    def test_doubly_linked_list_search(self, dll: LinkedList, initial_state: list[T], value_to_search: T, expected_result: Optional[int]) -> None:
        assert dll.head is None
        for insert_value in initial_state:
            dll.insert(insert_value, -1)
        assert dll.search(value_to_search) == expected_result
