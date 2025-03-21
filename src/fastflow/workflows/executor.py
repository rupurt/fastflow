from typing import List

from .exec import Run
from .workflow import Workflow


class Executor:
    workflows: List[Workflow]

    def __init__(self, workflows: List[Workflow]):
        self.workflows = workflows

    async def run(self) -> List[Run]:
        runs = []
        for workflow in self.workflows:
            run = Run(workflow=workflow)
            runs.append(run)
            await run.execute()
        return runs
