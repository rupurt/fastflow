from pathlib import Path

from fastflow import Workflow, Depends
import pytest

from .run import Run
from .status import Status


@pytest.mark.asyncio
async def test_init(wf: Workflow):
    run = Run(workflow=wf)
    assert run.id is not None
    assert run.status == Status.UNSTARTED
    assert run.started_at is None
    assert run.completed_at is None


@pytest.mark.asyncio
async def test_executes_stages(
    wf: Workflow,
    tmp_path: Path,
):
    @wf.step()
    async def step1():
        with open(tmp_path / "hello.txt", "w") as fd:
            fd.write("hello world")

    run = Run(workflow=wf)
    await run.execute()
    assert run.status == Status.SUCCESS
    assert run.started_at is not None
    assert run.completed_at is not None
    assert run.completed_at >= run.started_at
    with open(tmp_path / "hello.txt", "r") as fd:
        assert fd.read() == "hello world"


@pytest.mark.asyncio
async def test_inject_stage_dependencies(
    wf: Workflow,
    tmp_path: Path,
):
    def greeting() -> str:
        return "hello world"

    @wf.step()
    async def step1(greeting: str = Depends(greeting)):
        with open(tmp_path / "hello.txt", "w") as fd:
            fd.write(greeting)

    run = Run(workflow=wf)
    await run.execute()
    assert run.status == Status.SUCCESS
    with open(tmp_path / "hello.txt", "r") as fd:
        assert fd.read() == "hello world"


@pytest.mark.asyncio
async def test_inject_positional_and_keyword_arguments_from_prior_stage(
    wf: Workflow,
    tmp_path: Path,
):
    @wf.step()
    async def step1() -> str:
        return "one"

    @wf.step()
    async def step2(step1: str):
        with open(tmp_path / "step2.txt", "w") as fd:
            fd.write(",".join([step1, "two"]))

    @wf.step()
    async def step3(step1: str):
        with open(tmp_path / "step3.txt", "w") as fd:
            fd.write(",".join([step1, "three"]))

    @wf.step()
    async def step4(*, step1: str):
        with open(tmp_path / "step4.txt", "w") as fd:
            fd.write(",".join([step1, "four"]))

    run = Run(workflow=wf)
    await run.execute()
    assert run.status == Status.SUCCESS
    with open(tmp_path / "step2.txt", "r") as fd:
        assert fd.read() == "one,two"
    with open(tmp_path / "step3.txt", "r") as fd:
        assert fd.read() == "one,three"
    with open(tmp_path / "step4.txt", "r") as fd:
        assert fd.read() == "one,four"


@pytest.mark.asyncio
async def test_execute_error(wf: Workflow):
    @wf.step()
    async def step1():
        raise RuntimeError("step 1")

    run = Run(workflow=wf)
    await run.execute()
    assert run.status == Status.ERROR
    assert isinstance(run.error, RuntimeError)
    assert str(run.error) == "step 1"
    assert run.started_at is not None
    assert run.completed_at is not None
    assert run.completed_at >= run.started_at
