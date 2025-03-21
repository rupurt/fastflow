from enum import Enum


class Status(str, Enum):
    """
    Represents the current state of a workflow run.

    This enum inherits from str to allow for easy serialization and
    string comparison. Valid states are:

    - `UNSTARTED`: Initial state before execution begins
    - `IN_PROGRESS`: Workflow is currently executing
    - `PAUSED`: Execution has been temporarily suspended
    - `CANCELED`: Execution was terminated before completion
    - `SUCCESS`: Workflow completed successfully
    - `ERROR`: Workflow encountered an error during execution
    """

    UNSTARTED = "unstarted"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    CANCELED = "canceled"
    SUCCESS = "success"
    ERROR = "error"
