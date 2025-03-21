from dataclasses import dataclass
import inspect
from typing import Any, Awaitable, Callable

from fastflow.fast_depends import inject


@dataclass
class ABCStage:
    func: Callable[..., Awaitable[Any]]

    def __str__(self):
        return self.func.__name__

    async def __call__(self, *args, **kwargs):
        return await inject(self.func)(*args, **kwargs)

    @property
    def name(self) -> str:
        return self.func.__name__

    @property
    def qualname(self) -> str:
        return self.func.__qualname__

    @property
    def signature(self) -> inspect.Signature:
        return inspect.signature(self.func)
