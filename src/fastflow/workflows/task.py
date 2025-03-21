from typing import Any, Awaitable, Callable, Optional

from fastflow.fast_depends import inject

from .stage_graph import StageGraph
from .stages import (
    AsyncTaskFanOutStage,
    AsyncTaskStepStage,
)


class Task:
    stage_graph: StageGraph

    def __init__(self, stage_graph: StageGraph):
        self.stage_graph = stage_graph

    def step(
        self,
        persist: bool = True,
    ):
        def decorator(func: Callable[..., Any | Awaitable[Any]]):
            stage = AsyncTaskStepStage(func=inject(func))
            self.stage_graph.append(stage)
            return func

        return decorator

    def fan_out(
        self,
        partitions: Optional[int] = None,
        batch_size: Optional[int] = None,
        persist: bool = True,
    ):
        def decorator(func: Callable[..., Any | Awaitable[Any]]):
            stage = AsyncTaskFanOutStage(func=inject(func))
            self.stage_graph.append(stage)
            return func

        return decorator
