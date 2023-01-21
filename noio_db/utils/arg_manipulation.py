from typing import List


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
