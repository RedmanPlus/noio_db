from string import Template

from noio_db.core.sql_objects import BaseSQLObject


class CreateTableSQLObject(BaseSQLObject):

    template = Template("CREATE TABLE $what $where")
    template_keys = [
        "what",
        "where",
    ]


class CreateTableArgSQLObject(BaseSQLObject):

    template = Template("$what $type")
    template_keys = ["what", "type"]


class ArgSpecialParametersSQLObject(BaseSQLObject):

    template = Template("$what $params")
    template_keys = ["what", "params"]
