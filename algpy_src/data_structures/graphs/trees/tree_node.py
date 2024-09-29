from __future__ import annotations

from typing import Generic, TypeVar, Optional, Self

_K = TypeVar('_K')


class TreeNode(Generic[_K]):

    def __init__(self, key: _K, parent: Optional[Self] = None) -> None:
        """
        Constructor for the TreeNode class.

        Parameters
        ----------
        key : _K
            Key to represent the node.
        parent : Optional[Self] (default: None)
            Parent of this node within the tree. If not given, this node will be root-like.
        """
        self._key = key
        self._children: list[Self] = []
        self._depth = 0
        self._parent: Optional[Self] = None
        if parent is not None:
            parent.add_child(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TreeNode) and self.key == other.key

    @property
    def key(self) -> _K:
        return self._key

    @property
    def degree(self) -> int:
        return len(self._children)

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def parent(self) -> Optional[Self]:
        return self._parent

    @property
    def children(self) -> list[Self]:
        return self._children

    @property
    def leftmost_child(self) -> Optional[Self]:
        return self._children[0] if len(self._children) > 0 else None

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__} ({str(self)}, '
            f'parent={str(self._parent) if self._parent else None}, '
            f'children=[{[str(child) for child in self._children]}])'
        )

    def __str__(self) -> str:
        return f'(key={self._key!r})'

    def change_key(self, new_key: _K) -> None:
        self._key = new_key

    def add_child(self, child: Self) -> None:
        self._children.append(child)
        child.change_parent(self)

    def change_parent(self, new_parent: Optional[Self]) -> None:
        self._parent = new_parent
        self._depth = self._parent.depth + 1 if self._parent is not None else 0

    def remove_parent(self) -> None:
        self.change_parent(None)

    def remove_child(self, child: Self) -> None:
        self._children.remove(child)
        child.remove_parent()

    def remove_children(self) -> None:
        while leftmost := self.leftmost_child:
            self.remove_child(leftmost)