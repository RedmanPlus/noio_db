from string import Template

from .base import BaseSQLObject


class AlterTableSQLObject(BaseSQLObject):

    template = Template("ALTER TABLE $what")
    template_defaults = [
        "what",
    ]


class AddSQLObject(BaseSQLObject):

    template = Template("ADD COLUMN $what")
    template_defaults = ["what"]


class DropSQLObject(BaseSQLObject):

    template = Template("DROP COLUMN $what")
    template_defaults = ["what"]


class AlterColumnSQLObject(BaseSQLObject):

    template = Template("ALTER COLUMN $what TYPE $that")
    template_defaults = ["what", "that"]


class RenameColumnSQLObject(BaseSQLObject):

    template = Template("RENAME COLUMN $what TO $that")
    template_defaults = ["what", "that"]
