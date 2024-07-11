import logging

import pytest

from algpy_src.data_structures.linear.linked_list import LinkedList


@pytest.fixture()
def sll() -> LinkedList:
    return LinkedList(linked_list_type='singly')


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

        ]
    )
    def test_singly_linked_list_insert(self, sll: LinkedList, insert_value_sequence: list[object], insert_index_sequence: list[int], expected_state_after_insert: list[list[object]]) -> None:
        assert sll.head is None
        for insert_value, insert_index, expected_state in zip(insert_value_sequence, insert_index_sequence, expected_state_after_insert):
            sll.insert(insert_value, insert_index, verbosity_level=2)
            current = sll.head
            assert current is not None
            for value in expected_state:
                assert current.value == value
                current = current.successor



@pytest.fixture()
def dll() -> LinkedList:
    return LinkedList(linked_list_type='doubly')


def test_doubly_linked_list_base(dll: LinkedList) -> None:
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
