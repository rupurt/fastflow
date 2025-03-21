from fastflow import FastFlow
from typer import Typer


def command(app: Typer, flow: FastFlow):
    @app.command()
    def list():
        import duckdb
        import pyarrow as pa

        schema = pa.schema(
            [
                pa.field("name", pa.string()),
                pa.field("trigger", pa.string()),
                pa.field("stages", pa.string()),
            ],
        )
        workflows_pylist = []
        for wf in flow.workflows.values():
            if len(wf.stage_graph) == 0:
                stages = None
            else:
                stages = ", ".join(str(stage) for stage in wf.stage_graph)
            record = {
                "name": wf.name,
                "trigger": str(wf.trigger),
                "stages": stages,
            }
            workflows_pylist.append(record)
        workflows = pa.Table.from_pylist(
            workflows_pylist,
            schema=schema,
        )
        with duckdb.connect() as con:
            print(
                con.sql(
                    """
                    SELECT *
                    FROM workflows
                    ORDER BY name ASC
                    """,
                )
            )
