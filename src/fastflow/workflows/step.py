from typing import Any, Awaitable, Callable

from .stage_graph import StageGraph
from .stages import AsyncStepStage


class Step:
    stage_graph: StageGraph
    persist: bool

    def __init__(
        self,
        stage_graph: StageGraph,
        persist: bool = True,
    ):
        self.stage_graph = stage_graph
        self.persist = persist

    def __call__(self, func: Callable[..., Any | Awaitable[Any]]):
        stage = AsyncStepStage(func=func)
        self.stage_graph.append(stage)
