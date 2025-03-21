from typing import Any, Awaitable, Callable

from fastflow.fast_depends import inject

from .stage_graph import StageGraph
from .stages import AsyncServeStage


class Serve:
    stage_graph: StageGraph

    def __init__(self, stage_graph: StageGraph):
        self.stage_graph = stage_graph

    def __call__(self, func: Callable[..., Any | Awaitable[Any]]):
        stage = AsyncServeStage(func=inject(func))
        self.stage_graph.append(stage)
