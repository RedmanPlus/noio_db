from typing import Tuple, Union

from pydantic import BaseSettings


class BaseDriver:

    db_engine = None

    def __init__(self, parent, settings: BaseSettings):

        self.parent = parent

        if settings.type == "sqlite":

            self._connection = self.db_engine.connect(settings.db_name)

        elif settings.database_backend.port:

            self._connection = self.db_engine.connect(
                host=settings.database_backend.host,
                dbname=settings.database_backend.db_name,
                user=settings.database_backend.user,
                password=settings.database_backend.password,
                port=settings.database_backend.port,
            )

        elif settings.database_backend.type != "sqlite3":

            self._connection = self.db_engine.connect(
                host=settings.database_backend.host,
                dbname=settings.database_backend.db_name,
                user=settings.database_backend.user,
                password=settings.database_backend.password,
            )

        self._cursor = self._connection.cursor()

    def execute_sync(self, *args, **kwargs) -> Union[Tuple[str], None]:
        query_result = self._cursor.execute(*args, **kwargs)
        result = query_result.fetchall()
        if not result:
            self._connection.commit()

        return result

    async def execute_async(self, *args, **kwargs):

        return self.execute_sync(*args, **kwargs)

    def __call__(self, *args, **kwargs):

        if self.parent.is_called_async:

            return self.execute_async(*args, **kwargs)

        return self.execute_sync(*args, **kwargs)

    def __del__(self):

        self._connection.close()

        self._cursor = None
        self._connection = None
