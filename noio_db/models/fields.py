class IDField:
    def __init__(self, parent):
        self.__counter__ = 1
        self.parent = parent
        self.parent_id = self.__counter__
