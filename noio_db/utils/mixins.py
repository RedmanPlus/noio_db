class OneArgMixin:
    def get_object(self, *args):

        field = args[0]

        if len(args) > 1:

            raise Exception(f"{self.__class__.__name__} can take only one argument")

        return field
