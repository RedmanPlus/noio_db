from string import Template

from .base import BaseSQLObject


class SelectSQLObject(BaseSQLObject):

    template = Template("SELECT $what")
    template_keys = [
        "what",
    ]


class FromSQLObject(BaseSQLObject):

    template = Template("FROM $what")
    template_keys = [
        "what",
    ]


class JoinSQLObject(BaseSQLObject):

    template = Template("$one $join JOIN $two ON $condition")
    template_keys = ["one", "two", "join", "condition"]


class WhereSQLObject(BaseSQLObject):

    template = Template("WHERE $what")
    template_keys = ["what"]


class GroupBySQLObject(BaseSQLObject):

    template = Template("GROUP BY $what")
    template_keys = ["what"]


class HavingSQLObject(BaseSQLObject):

    template = Template("HAVING $what")
    template_keys = ["what"]


class OrderBySQLObject(BaseSQLObject):

    template = Template("ORDER BY $what")
    template_keys = ["what"]


class LimitSQLObject(BaseSQLObject):

    template = Template("LIMIT $by")
    template_keys = ["by"]
