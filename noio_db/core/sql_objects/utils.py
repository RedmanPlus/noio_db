from string import Template

from .base import BaseSQLObject


class ArgInBracesSQLObject(BaseSQLObject):

    template = Template("($what)")
    template_keys = [
        "what",
    ]


class AsSQLObject(BaseSQLObject):

    template = Template("$one AS $two")
    template_keys = ["one", "two"]


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


class CommaSQLObject(BaseSQLObject):

    template = Template("$one, $two")
    template_keys = [
        "one",
        "two",
    ]
