import pytest


@pytest.fixture()
def query():

    return {
        "select": "*",
        "from": "users",
        "where": {"and": ["name = 'John Doe'", "age = 25"]},
    }


@pytest.fixture()
def full_query():

    return {
        "select": ["users.name", "users.age", "estate.price"],
        "from": [
            "users",
            "estate",
            "id",
        ],
        "where": {
            "and": ["users.name = 'John Doe'", "users.age = 25", "estate.price > 60000"]
        },
        "group_by": "users.country",
        "order_by": "estate.price",
    }
