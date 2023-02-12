import sqlite3

import pytest


@pytest.fixture(scope="module")
def small_db():

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

    cur.execute(
        """
        INSERT INTO user (name, age, email)
        VALUES
            ("Jane", 25, "my_email@mail.ru");
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
