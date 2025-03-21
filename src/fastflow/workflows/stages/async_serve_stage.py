from .abc import ABCStage


class AsyncServeStage(ABCStage):
    async def __call__(self, **kwargs):
        return await self.func(**kwargs)
