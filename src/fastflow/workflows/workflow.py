from .serve import Serve
from .stage_graph import StageGraph
from .step import Step
from .task import Task
from .trigger import Trigger


class Workflow:
    name: str
    stage_graph: StageGraph
    trigger: Trigger
    task: Task

    def __init__(self, name: str):
        self.name = name
        self.stage_graph = StageGraph()
        self.trigger = Trigger(self.stage_graph)
        self.task = Task(self.stage_graph)

    def step(self, persist: bool = True):
        return Step(self.stage_graph, persist)

    def serve(self):
        return Serve(self.stage_graph)
