from fastflow import Workflow
import pytest

from .run import Run
from .status import Status


@pytest.mark.asyncio
async def test_single_stage(wf: Workflow):
    @wf.step()
    async def step1():
        pass

    run = Run(workflow=wf)
    await run.execute()
    assert run.status == Status.SUCCESS


@pytest.mark.asyncio
async def test_multiple_stages(wf: Workflow):
    @wf.step()
    async def step1():
        pass

    @wf.step()
    async def step2():
        pass

    run = Run(workflow=wf)
    await run.execute()
    assert run.status == Status.SUCCESS
