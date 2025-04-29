from typing import Optional

from .workflows import Scheduler, Workflow


class FastFlow:
    __slots__ = [
        "_app_name",
        "_scheduler",
        "_workflows",
    ]

    def __init__(
        self,
        app_name: Optional[str] = "fastflow",
        scheduler: Scheduler = Scheduler(),
    ):
        self._app_name = app_name
        self._scheduler = scheduler
        self._workflows = {}

    def workflow(self, name: str) -> Workflow:
        wf = Workflow(name)
        self._workflows[name] = wf
        return wf
