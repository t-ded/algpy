import logging
from typing import Optional

import pytest

from algpy_src.data_structures.linear.linked_list import LinkedList


@pytest.fixture()
def sll() -> LinkedList:
    return LinkedList(linked_list_type='singly')


def traverse_and_check_equals_expected_sequence(ll: LinkedList, expected_state: list[object]):
    if len(expected_state) == 0:
        assert ll.head is None
    else:
        current = ll.head
        for value in expected_state:
            assert current is not None
            assert current.value == value
            current = current.successor


class TestSinglyLinkedList:

    def test_singly_linked_list_base(self, sll: LinkedList) -> None:
        assert sll.name == 'Singly Linked List'
        assert sll.length == 0

        assert sll.best_case_insert_time_complexity == '1'
        assert sll.best_case_insert_description == 'index 0'
        assert sll.average_case_insert_time_complexity == 'n'
        assert sll.worst_case_insert_time_complexity == 'n'
        assert sll.worst_case_insert_description == 'index equals length'

        assert sll.best_case_search_time_complexity == '1'
        assert sll.best_case_search_description == 'item in head'
        assert sll.average_case_search_time_complexity == 'n'
        assert sll.worst_case_search_time_complexity == 'n'
        assert sll.worst_case_search_description == 'item not present'

        assert sll.best_case_delete_time_complexity == '1'
        assert sll.best_case_delete_description == 'item in head'
        assert sll.average_case_delete_time_complexity == 'n'
        assert sll.worst_case_delete_time_complexity == 'n'
        assert sll.worst_case_delete_description == 'item at tail'

    def test_insert_to_empty(self, sll: LinkedList) -> None:
        assert sll.head is None

        sll.insert_to_empty('A')
        assert sll.head is not None
        assert sll.head.value == 'A'
        assert sll.head.predecessor is None
        assert sll.head.successor is None
        assert sll.length == 1

    def test_insert_to_empty_via_insert(self, sll: LinkedList) -> None:
        assert sll.head is None

        sll.insert('A', 0)
        assert sll.head is not None
        assert sll.head.value == 'A'
        assert sll.head.predecessor is None
        assert sll.head.successor is None
        assert sll.length == 1

    def test_insert_index_out_of_bounds_does_nothing(self, sll: LinkedList, caplog) -> None:

        assert sll.head is None
        with caplog.at_level(logging.WARNING):
            sll.insert('A', 5)
        assert sll.head is None
        assert caplog.records[0].levelname == 'WARNING'
        assert caplog.records[0].message == 'Index out of range.'

        with caplog.at_level(logging.WARNING):
            sll.insert('A', -2)
        assert sll.head is None
        assert caplog.records[1].levelname == 'WARNING'
        assert caplog.records[1].message == 'Index out of range.'

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
    def test_singly_linked_list_insert(self, sll: LinkedList, insert_value_sequence: list[object], insert_index_sequence: list[int], expected_state_after_insert: list[list[object]]) -> None:
        assert sll.head is None
        for insert_value, insert_index, expected_state in zip(insert_value_sequence, insert_index_sequence, expected_state_after_insert):
            sll.insert(insert_value, insert_index)
            traverse_and_check_equals_expected_sequence(sll, expected_state)

    def test_invalid_delete_value_or_index_does_nothing(self, sll: LinkedList, caplog) -> None:

        assert sll.head is None
        try:
            sll.delete('A')
        except Exception as e:
            pytest.fail(f'Deletion with null head rose an error {e}')
        sll.insert('A', 0)
        with caplog.at_level(logging.WARNING):
            sll.delete('A', 2)
        assert caplog.records[0].levelname == 'WARNING'
        assert caplog.records[0].message == 'Index out of range.'
        try:
            sll.delete('B')
        except Exception as e:
            pytest.fail(f'Deletion of item which is not present rose an error {e}')

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
        ]
    )
    def test_singly_linked_list_delete(self, sll: LinkedList, initial_state: list[object], delete_value_sequence: list[object],
                                       delete_index_sequence: list[Optional[int]], expected_state_after_delete: list[list[Optional[object]]]) -> None:
        assert sll.head is None
        for insert_value in initial_state:
            sll.insert(insert_value, -1)
        sll_len = sll.length
        for delete_value, delete_index, expected_state in zip(delete_value_sequence, delete_index_sequence, expected_state_after_delete):
            sll.delete(delete_value, delete_index, verbosity_level=2)
            traverse_and_check_equals_expected_sequence(sll, expected_state)
            sll_len -= 1
            assert sll_len == sll.length
