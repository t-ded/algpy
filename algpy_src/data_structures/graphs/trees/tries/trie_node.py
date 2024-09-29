from typing import Self, Optional

from algpy_src.data_structures.graphs.trees.tree_node import TreeNode


class TrieNode(TreeNode[str]):

    def __init__(self, key: str, is_marked: bool = False, parent: Optional[Self] = None) -> None:
        super().__init__(key, parent)
        self._is_marked = is_marked

    @property
    def is_marked(self) -> bool:
        return self._is_marked
    