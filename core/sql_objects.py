from abc import ABC
from string import Template
from typing import Optional, List, Dict


class BaseSQLObject(ABC):
    
    template: Optional[Template]
    template_keys: List[str]

    def __init__(
        self,
        *args,
    ) -> None:
        self.object_args = self.prepare_args(*args)
    
    def prepare_args(
        self,
        *args
    ) -> Dict[str, str]:
        kwargs: dict = {}
        for i, arg in enumerate(args):
            if isinstance(arg, BaseSQLObject) :
                arg = arg.compile()
            kwargs[self.template_keys[i]] = arg

        return kwargs

    def compile(self) -> str:
        return self.template.substitute(**self.object_args)

    def __str__(self) -> str:
        return self.compile()


class SelectSQLObject(BaseSQLObject):

    template = Template("SELECT $what")
    template_keys = [
        "what",
    ]


class ArgInBracesSQLObject(BaseSQLObject):

    template = Template("($what)")
    template_keys = [
        "what",
    ]


class AsSQLObject(BaseSQLObject):

    template = Template("$one AS $two")
    template_keys = [
        "one",
        "two"
    ]


class FromSQLObject(BaseSQLObject):

    template = Template("FROM $what")
    template_keys = [
        "what",
    ]


class JoinSQLObject(BaseSQLObject):

    template = Template("$one $join JOIN $two ON $condition")
    template_keys = [
        "one",
        "two",
        "join",
        "condition"
    ]


class WhereSQLObject(BaseSQLObject):

    template = Template("WHERE $what")
    template_keys = [
        "what"
    ]


class AndSQLObject(BaseSQLObject):

    template = Template("$one AND $two")
    template_keys = [
        "one",
        "two",
    ]


class OrSQLObject(BaseSQLObject):

    template = Template("$one OR $two")
    template_keys = [
        "one",
        "two",
    ]


class InsertSQLObject(BaseSQLObject):

    template = Template("INSERT INTO $where $what")
    template_keys = [
        "where",
        "what",
    ]
