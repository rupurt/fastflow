from typing import Callable, List


class ProducerActivity:
    __slots__ = [
        "_wrapper",
        "_topic",
        "_after",
    ]

    def __init__(
        self,
        wrapper: Callable,
        topic: str,
        after: List[Callable] = [],
    ):
        self._wrapper = wrapper
        self._topic = topic
        self._after = after

    async def __call__(self):
        return await self._wrapper()
