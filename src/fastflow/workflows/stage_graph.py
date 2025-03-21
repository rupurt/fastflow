from typing import Iterator, List

from .stages import (
    AsyncServeStage,
    AsyncStepStage,
    AsyncTaskFanOutStage,
    AsyncTaskStepStage,
)

type Stage = (
    AsyncServeStage | AsyncStepStage | AsyncTaskFanOutStage | AsyncTaskStepStage
)


class StageGraph:
    stages: List[Stage]

    def __init__(self):
        self.stages = []

    def append(self, stage: Stage) -> None:
        """
        Add a new step to the workflow.

        Args:
            step (AsyncStep): The workflow step to append to the sequence

        Returns:
            None
        """
        self.stages.append(stage)

    def __iter__(self) -> Iterator[Stage]:
        """
        Make `WorkflowSteps` iterable.

        Returns:
            Iterator[Stage]: An iterator over the workflow steps
        """
        return iter(self.stages)

    def __len__(self) -> int:
        """
        Return the number of steps in the workflow.

        Returns:
            int: The count of workflow steps
        """
        return len(self.stages)
