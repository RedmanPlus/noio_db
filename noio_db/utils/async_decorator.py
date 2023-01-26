from inspect import currentframe, getouterframes


class ToAsync:
    def __init__(self, func):
        self.func = func

    async def _run_async(self, ref, *args, **kwargs):

        return self.func(ref, *args, **kwargs)

    def _run_sync(self, ref, *args, **kwargs):

        return self.func(ref, *args, **kwargs)

    def __call__(self, ref, *args, **kwargs):

        curframe = currentframe()
        outframe = getouterframes(curframe, 1)

        if "await" in outframe[1][4][0]:
            return self._run_async(ref, *args, **kwargs)

        return self._run_sync(ref, *args, **kwargs)
