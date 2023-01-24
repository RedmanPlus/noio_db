from typing import List

from noio_db.core.sql_objects import CommaSQLObject
from noio_db.utils.consts import ARG_METHOD_NAMES, KWARG_METHOD_NAMES


def pair_up_args(*args) -> List[List[str]]:

    result: List[List[str]] = []

    for i, arg in enumerate(args):

        if i % 2 == 0 and i == len(args) - 1:
            result.append([arg])

        if i % 2 != 0:
            continue

        if i == len(args) - 1:
            break

        result.append([arg, args[i + 1]])

    return result


def construct_arg_pair(key: str, value: any) -> str:

    if isinstance(value, str):

        return f"{key} = '{value}'"

    if isinstance(value, (int, float)):

        return f"{key} = {value}"

    if isinstance(value, bool):

        return f"{key} = {int(value)}"

    raise Exception(f"Unsupported value type {type(value)}")


def reformat_dict(into: dict) -> list:
    result: list = []
    for k, v in into.items():
        if f"_{k}" not in ARG_METHOD_NAMES.union(KWARG_METHOD_NAMES):
            result.append(construct_arg_pair(k, v))
            continue

        if f"_{k}" in ARG_METHOD_NAMES.union(KWARG_METHOD_NAMES) and isinstance(
            v, dict
        ):
            inner = reformat_dict(v)
            result.append({k: inner})
            continue

        result.append(v)

    return result


def zip_into_dict(list_a: list, list_b: list) -> dict:
    result: dict = {}
    for a, b in zip(list_a, list_b):
        result[a] = b

    return result


def list_into_comma_sql_object(*args) -> CommaSQLObject:

    root = None
    for i, arg in enumerate(args):
        if i == 0:
            root = CommaSQLObject(arg, args[i + 1])
            continue
        if i == len(args) - 1:
            break

        root = CommaSQLObject(root, args[i + 1])

    return root
