import pytest

from algpy_src.base.constants import TEST_SEED
from algpy_src.data_structures.linear.linked_list import LinkedList
from algpy_src.data_structures.linear.linked_list_node import LinkedListNode


@pytest.fixture
def ll_node():
    return LinkedListNode(TEST_SEED)


@pytest.fixture()
def sll():
    return LinkedList(linked_list_type='singly')


@pytest.fixture()
def dll():
    return LinkedList(linked_list_type='doubly')


def test_singly_linked_list_base(sll):
    assert sll.name == 'Singly Linked List'

    assert sll.best_case_insert_time_complexity == '1'
    assert sll.best_case_insert_description == 'index 0'
    assert sll.average_case_insert_time_complexity == 'n'
    assert sll.worst_case_insert_time_complexity == 'n'
    assert sll.worst_case_insert_description == 'index equals length'


