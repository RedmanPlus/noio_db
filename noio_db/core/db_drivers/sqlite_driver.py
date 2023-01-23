import sqlite3

from noio_db.core.db_drivers import BaseDriver


class SQLiteDriver(BaseDriver):

    db_engine = sqlite3
