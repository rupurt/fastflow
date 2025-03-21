from typing import List, OrderedDict

# from .settings import KafkaSettings

from .state import State
from .topology import Topology
from .workflows import (
    Executor,
    Workflow,
)
from .workflows.exec import Run


class FastFlow:
    app_name: str
    # kafka: KafkaSettings
    topology: Topology
    state: State
    workflows: OrderedDict[str, Workflow]

    def __init__(
        self,
        app_name: str,
        topology: Topology,
        state: State,
    ):
        self.app_name = app_name
        self.topology = topology
        self.state = state
        self.workflows = OrderedDict()

    def workflow(self, name: str) -> Workflow:
        workflow = Workflow(name)
        self.workflows[name] = workflow
        return workflow

    async def migrate(self) -> None:
        await self.topology.migrate(self.app_name, list(self.workflows.values()))

    async def run(self, workflow_names: List[str]) -> List[Run]:
        workflows = []
        for name in workflow_names:
            workflows.append(self.workflows[name])
        return await Executor(workflows).run()
