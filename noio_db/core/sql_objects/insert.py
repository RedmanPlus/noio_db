from string import Template

from .base import BaseSQLObject


class InsertSQLObject(BaseSQLObject):

    template = Template("INSERT INTO $where $what")
    template_keys = [
        "where",
        "what",
    ]
