from dataclasses import dataclass
from typing import List, Optional, Self


@dataclass()
class ASTNode:
    """An AST node containing information about specific part of a query
    Can contian other nodes inside it for nested structure
    """

    name: str
    children: Optional[List[str] | List[Self]] = None

    def __iter__(self):
        return self.children

    def to_query(self):
        children = self.children
        if isinstance(self.children, ASTNode):
            children = [obj.to_query() for obj in self.children]
        return {self.name: children}

    # pylint: disable=R1710
    def get_child(self, name: str) -> Optional[Self]:

        for child in self.children:
            if child.name == name:
                return child

            inner_search = child.get_child(name)
            if inner_search is not None:
                return inner_search

    # pylint: enable=R1710

    @classmethod
    def get_args(cls, annotations: dict, **kwargs) -> list:
        params = []

        for k, v in kwargs.items():
            field_val = annotations.get(k, False)

            if not field_val:
                continue

            if not isinstance(v, field_val):
                raise Exception(
                    f"Wrong attribute type: is {type(v)}, must be {field_val}"
                )

            if isinstance(v, dict):
                node = cls.from_args(**v)
                params.append(node)
                continue

            params.append(f"{k} = {v}")

        return params

    @classmethod
    def from_args(cls, members: list, node_name: str, **kwargs) -> Self:

        param_lists = [
            cls.get_args(member.__annotations__, **kwargs) for member in members
        ]
        node = cls(name=node_name, children=param_lists)

        return node


@dataclass()
class AST:
    """An Abstract Syntax Tree (AST) of the resulting SQL query
    Forms a tree structure containing multiple nodes with related information.
    Can be extended or modified for purposes of creating full AST of any given
    query
    """

    root: ASTNode = ASTNode(name="root")

    def __getitem__(self, item):
        for child in self.root:
            child.get_child(item)

    def __setitem__(self, key, value):
        pass

    def to_query(self) -> dict:
        query = {}
        for child in self.root.children:
            q = child.to_query()
            query.update(**q)

        return query

    def __str__(self) -> str:
        return str(self.to_query())
