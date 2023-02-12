from string import Template

from noio_db.core.sql_objects import BaseSQLObject


class DeleteSQLObject(BaseSQLObject):

    template = Template("DELETE FROM $where")
    template_keys = [
        "where",
    ]
