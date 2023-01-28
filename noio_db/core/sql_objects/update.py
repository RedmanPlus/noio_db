from string import Template

from noio_db.core.sql_objects import BaseSQLObject


class UpdateSQLObject(BaseSQLObject):

    template = Template("UPDATE $what")
    template_keys = ["what"]


class SetSQLObject(BaseSQLObject):

    template = Template("SET $what")
    template_keys = ["what"]
