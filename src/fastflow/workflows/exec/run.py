from collections import OrderedDict
import datetime as dt
from inspect import Parameter
from typing import Optional

import pyarrow
import pyarrow.flight
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from fastflow import fast_depends
from fastflow.workflows.workflow import Workflow

from .id import ID
from .status import Status


class Run(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    workflow: Workflow = Field()
    id: ID = Field(default_factory=ID)
    status: Status = Field(default=Status.UNSTARTED)
    error: Optional[Exception] = Field(default=None)
    started_at: Optional[dt.datetime] = Field(default=None)
    completed_at: Optional[dt.datetime] = Field(default=None)

    @field_serializer("workflow")
    def serialize_workflow(self, workflow: Workflow, _):
        return workflow.name

    @field_serializer("id")
    def serialize_id(self, id: ID, _):
        return str(id)

    @field_serializer("error")
    def serialize_error(self, error: Exception, _):
        return str(error)

    async def execute(self) -> None:
        self.started_at = _now()
        self.status = Status.IN_PROGRESS
        stage_results = OrderedDict()
        try:
            for stage in self.workflow.stage_graph:
                sig = stage.signature
                args = []
                kwargs = {}
                for param in sig.parameters.values():
                    if isinstance(param.default, fast_depends.dependencies.Depends):
                        continue
                    elif (
                        param.kind == Parameter.POSITIONAL_ONLY
                        or param.kind == Parameter.POSITIONAL_OR_KEYWORD
                    ):
                        args.append(stage_results[param.name])
                    elif param.kind == Parameter.KEYWORD_ONLY:
                        kwargs[param.name] = stage_results[param.name]
                    else:
                        raise NotImplementedError(
                            f"Unhandled parameter kind: {param.kind}"
                        )
                result = await stage(*args, **kwargs)
                if isinstance(result, pyarrow.flight.FlightServerBase):
                    result.serve()
                stage_results[stage.name] = result
            self.completed_at = _now()
            self.status = Status.SUCCESS
        except Exception as e:
            self.completed_at = _now()
            self.status = Status.ERROR
            self.error = e

    async def pause(self):
        self.status = Status.PAUSED


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)
