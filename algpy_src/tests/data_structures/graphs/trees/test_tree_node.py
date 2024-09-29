from algpy_src.base.constants import TEST_SEED
from algpy_src.data_structures.graphs.trees.tree_node import TreeNode


def test_basic_node_properties() -> None:
    tree_node = TreeNode(TEST_SEED)
    tree_node_child_1 = TreeNode(TEST_SEED + 1, parent=tree_node)
    tree_node_child_2 = TreeNode(TEST_SEED + 2, parent=tree_node)
    tree_node_child_3 = TreeNode(TEST_SEED + 3, parent=tree_node)

    assert tree_node.depth == 0
    assert tree_node.degree == 3

    assert tree_node.parent is None
    assert tree_node_child_1.parent == tree_node
    assert tree_node_child_1.depth == 1
    assert tree_node_child_1.degree == 0
    assert tree_node_child_2.parent == tree_node
    assert tree_node_child_2.depth == 1
    assert tree_node_child_2.degree == 0
    assert tree_node_child_3.parent == tree_node
    assert tree_node_child_3.depth == 1
    assert tree_node_child_3.degree == 0

    tree_node.remove_child(tree_node_child_1)
    assert tree_node.degree == 2
    assert tree_node_child_1.parent is None
    assert tree_node_child_1.depth == 0

    tree_node.remove_children()
    assert tree_node.degree == 0
    assert tree_node_child_1.depth == 0
    assert tree_node_child_2.depth == 0
    assert tree_node_child_3.depth == 0