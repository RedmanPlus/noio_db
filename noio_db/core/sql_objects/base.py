from abc import ABC
from string import Template
from typing import Dict, List, Optional, Union


class BaseSQLObject(ABC):

    template: Optional[Template]
    template_keys: List[str]
    template_defaults: Union[Dict[str, str], None] = None

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
        if self.template_defaults is not None:
            return self.template.substitute(self.template_defaults, **self.object_args)

        return self.template.substitute(**self.object_args)

    def __str__(self) -> str:
        return self.compile()
