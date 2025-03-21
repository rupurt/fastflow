from fastflow import FastFlow, Topology, State
import pytest


@pytest.fixture
def app():
    return FastFlow(
        app_name="test-app",
        topology=Topology(),
        state=State(),
    )


@pytest.fixture
def wf(app: FastFlow):
    return app.workflow(name="test-workflow")
