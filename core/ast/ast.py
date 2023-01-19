from typing import Self


class ASTNode:

    def __init__(self, name: str, content: str | Self):
        self.name = name
        self.content =  content


class AST:

    def __getattr__(self, item):

