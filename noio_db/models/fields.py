from typing import Any

from noio_db.utils.mappings import SQLITE_MAPPINGS


class ID:
    def __new__(cls, id_type: Any = int, id_val: Any = None):
        self = super().__new__(cls)

        self._id_type = id_type
        self._id_val = id_val

        return self

    def __str__(self):
        return str(self._id_val)

    @property
    def sql_definition(self):

        sql_type_signature = SQLITE_MAPPINGS.get(self._id_type, False)

        if not sql_type_signature:
            raise Exception("Can't find matching type signature")

        return f"{sql_type_signature} PRIMARY KEY"
