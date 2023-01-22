from typing import List

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


def reformat_dict(into: dict) -> list:
    result: list = []
    for k, v in into.items():
        if f"_{k}" not in ARG_METHOD_NAMES.union(KWARG_METHOD_NAMES):
            result.append(f"{k}={v}")
            continue

        if f"_{k}" in ARG_METHOD_NAMES.union(KWARG_METHOD_NAMES) and isinstance(
            v, dict
        ):
            inner = reformat_dict(v)
            result.append({k: inner})
            continue

        result.append(v)

    return result
