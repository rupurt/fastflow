from fastflow import Workflow
import pytest

from .run import Run
from .status import Status


@pytest.mark.asyncio
async def test_single_stage(wf: Workflow):
    @wf.serve()
    async def serve1():
        pass

    run = Run(workflow=wf)
    await run.execute()
    assert run.status == Status.SUCCESS
