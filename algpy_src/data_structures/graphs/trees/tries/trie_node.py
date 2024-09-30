from typing import Self, Optional

from typing_extensions import TypeVar

from algpy_src.data_structures.graphs.trees.tree_node import TreeNode

T = TypeVar('T')


class TrieNode(TreeNode[T]):

    def __init__(self, key: T, alphabet_length: int, is_terminal: bool = False, parent: Optional[Self] = None) -> None:
        super().__init__(key, parent)
        self._children = [None] * alphabet_length
        self._is_terminal = is_terminal

    @property
    def is_terminal(self) -> bool:
        return self._is_terminal

    def set_terminal(self, is_terminal: bool) -> None:
        self._is_terminal = is_terminal
    