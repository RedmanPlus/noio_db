import sqlite3

import pytest


@pytest.fixture(scope="module")
def db():
    con = sqlite3.connect("test")
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        );
        """
    )

    con.commit()

    yield

    cur.execute(
        """
        DROP TABLE user;
        """
    )

    con.commit()
