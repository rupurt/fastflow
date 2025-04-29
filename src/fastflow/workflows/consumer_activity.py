from typing import Callable, List, Optional


class ConsumerActivity:
    __slots__ = [
        "_wrapper",
        "_topic",
        "_after",
        "_offset",
    ]

    def __init__(
        self,
        wrapper: Callable,
        topic: str,
        after: List[Callable] = [],
        offset: Optional[int | Callable] = None,
    ):
        self._wrapper = wrapper
        self._topic = topic
        self._after = after
        self._offset = offset

    async def __call__(self):
        return await self._wrapper()
