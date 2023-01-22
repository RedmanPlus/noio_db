from noio_db.utils.arg_manipulation import reformat_dict
from noio_db.utils.consts import ARG_METHOD_NAMES, KWARG_METHOD_NAMES


# pylint: disable=R1710, R1714, E0203, W0201
class AST:
    def __getattr__(self, item):
        if item in ARG_METHOD_NAMES.union(KWARG_METHOD_NAMES):
            other = AST()
            other.__name__ = item
            self.__dict__[item[1:]] = other
            setattr(self.__class__, item, other)
            return self.__dict__[item[1:]]

    def __call__(self, *args, **kwargs):
        if self.__name__ in ARG_METHOD_NAMES:
            self.__dict__["_"] = list(args)
        else:
            self.__dict__ = kwargs

    def to_dict(self) -> dict:
        result_dict: dict = {}
        for k, v in self.__dict__.items():
            if k == "__name__":
                continue
            if isinstance(v, AST):
                v = v.to_dict()

            if k == "_":
                return v

            result_dict[k] = v

        for k, v in result_dict.items():
            if (k == "where" or k == "having") and isinstance(v, dict):
                newargs = reformat_dict(v)
                result_dict[k] = newargs[0]

        return result_dict


# pylint: enable=R1710, R1714, E0203, W0201
