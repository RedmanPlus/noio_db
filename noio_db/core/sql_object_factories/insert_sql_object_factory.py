from noio_db.core.sql_object_factories import AbstractSQLObjectFactory
from noio_db.core.sql_objects import (
    ArgInBracesSQLObject,
    BaseSQLObject,
    InsertSQLObject,
)
from noio_db.utils import list_into_comma_sql_object


class InsertSQLObjectFactory(AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        if len(args) < 3:
            raise Exception(
                f"Must have at least 3 args for the insert factoty, got {len(args)}"
            )

        destination = args[0]

        field_mappings = ArgInBracesSQLObject(list_into_comma_sql_object(*args[1]))

        values = []
        if len(args[2:]) == 1:

            values = ArgInBracesSQLObject(list_into_comma_sql_object(*args[2]))

        else:
            for val_group in args[2:]:

                val_mappings = ArgInBracesSQLObject(
                    list_into_comma_sql_object(*val_group)
                )
                values.append(val_mappings)

            values = list_into_comma_sql_object(*values)

        return InsertSQLObject(destination, field_mappings, values)
