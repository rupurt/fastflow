from typing import Callable, List, Optional


class TaskActivity:
    __slots__ = [
        "_wrapper",
        "_after",
    ]

    def __init__(
        self,
        wrapper: Callable,
        after: List[Callable] = [],
    ):
        self._wrapper = wrapper
        self._after = after

    async def __call__(self):
        return await self._wrapper()
