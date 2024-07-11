import pytest

from algpy_src.data_structures.linear.linked_list import LinkedList


@pytest.fixture()
def dll() -> LinkedList:
    return LinkedList(linked_list_type='doubly')


def traverse_and_check_equals_expected_sequence(ll: LinkedList, expected_state: list[object]):
    if len(expected_state) == 0:
        assert ll.head is None
    else:
        current = ll.head
        pred = None
        for value in expected_state:
            assert current is not None
            assert current.value == value
            assert current.predecessor == pred
            pred = current
            current = current.successor


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
