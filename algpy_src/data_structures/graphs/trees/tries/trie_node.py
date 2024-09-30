from typing import Self, Optional

from typing_extensions import TypeVar

from algpy_src.data_structures.graphs.trees.tree_node import TreeNode

T = TypeVar('T')


class TrieNode(TreeNode[T]):

    def __init__(self, key: T, is_marked: bool = False, parent: Optional[Self] = None) -> None:
        super().__init__(key, parent)
        self._is_marked = is_marked

    @property
    def is_marked(self) -> bool:
        return self._is_marked
    