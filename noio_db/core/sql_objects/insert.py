from string import Template

from .base import BaseSQLObject


class InsertSQLObject(BaseSQLObject):

    template = Template("INSERT INTO $where $fields VALUES $what")
    template_keys = [
        "where",
        "fields",
        "what",
    ]
