from abc import ABC
from string import Template
from typing import Dict, List, Optional


class BaseSQLObject(ABC):

    template: Optional[Template]
    template_keys: List[str]

    def __init__(
        self,
        *args,
    ) -> None:
        self.object_args = self.prepare_args(*args)

    def prepare_args(self, *args) -> Dict[str, str]:
        kwargs: dict = {}
        for i, arg in enumerate(args):
            if isinstance(arg, BaseSQLObject):
                arg = arg.compile()
            kwargs[self.template_keys[i]] = arg

        return kwargs

    def compile(self) -> str:
        return self.template.substitute(**self.object_args)

    def __str__(self) -> str:
        return self.compile()
