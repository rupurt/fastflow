from fastflow.fast_depends import inject

from .stage_graph import StageGraph
from .triggers import (
    NoTrigger,
    CronTrigger,
    StreamTrigger,
    QueueTrigger,
    HttpDeleteTrigger,
    HttpPutTrigger,
    HttpGetTrigger,
    HttpPatchTrigger,
    HttpPostTrigger,
)


type TriggerType = (
    NoTrigger
    | CronTrigger
    | StreamTrigger
    | QueueTrigger
    | HttpDeleteTrigger
    | HttpGetTrigger
    | HttpPutTrigger
    | HttpPatchTrigger
    | HttpPostTrigger
)


class Trigger:
    """
    A collection of decorators for defining workflow triggers.

    The `Trigger` class provides decorators that can be used to define how and when
    workflow functions should be executed. It supports various trigger types including:

    - Cron-based scheduling
    - Stream processing
    - Queue-based triggers
    - HTTP endpoints (GET, POST, PUT, PATCH, DELETE)
    """

    trigger: TriggerType
    stage_graph: StageGraph

    def __init__(self, stage_graph: StageGraph):
        self.trigger = NoTrigger()
        self.stage_graph = stage_graph

    def cron(self, schedule: str):
        def decorator(func):
            self.trigger = CronTrigger(func=func, schedule=schedule)
            return func

        return decorator

    def stream(self):
        def decorator(func):
            self.trigger = StreamTrigger(func=func)
            return func

        return decorator

    def queue(self):
        def decorator(func):
            self.trigger = QueueTrigger(func=func)
            return func

        return decorator

    def http_get(self):
        def decorator(func):
            self.trigger = HttpGetTrigger(func=func)
            return func

        return decorator

    def http_post(self):
        def decorator(func):
            self.trigger = HttpPostTrigger(func=func)
            return func

        return decorator

    def http_put(self):
        def decorator(func):
            self.trigger = HttpPutTrigger(func=func)
            return func

        return decorator

    def http_patch(self):
        def decorator(func):
            self.trigger = HttpPatchTrigger(func=func)
            return func

        return decorator

    def http_delete(self):
        def decorator(func):
            self.trigger = HttpDeleteTrigger(func=func)
            return func

        return decorator

    def __str__(self):
        trigger = str(self.trigger) if self.trigger else "-"
        return f"{trigger}"
