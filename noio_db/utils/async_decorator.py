from inspect import currentframe, getouterframes


class ToAsync:
    def __init__(self, func):
        self.func = func

    async def _run_async(self, *args, **kwargs):

        return self.func(*args, **kwargs)

    def _run_sync(self, *args, **kwargs):

        return self.func(*args, **kwargs)

    def __call__(self, *args, **kwargs):

        curframe = currentframe()
        outframe = getouterframes(curframe, 1)

        if "await" in outframe[1][4][0]:
            return self._run_async(*args, **kwargs)

        return self._run_sync(*args, **kwargs)
