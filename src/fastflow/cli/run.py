from typing import Annotated

from fastflow import FastFlow
from typer import Argument, Typer


def command(app: Typer, flow: FastFlow):
    @app.command()
    def run(
        name: Annotated[
            str,
            Argument(
                help="Workflow name",
            ),
        ],
    ):
        import asyncio

        import duckdb
        import pyarrow as pa

        runs = asyncio.run(flow.run([name]))
        schema = pa.schema(
            [
                pa.field("id", pa.string()),
                pa.field("status", pa.string()),
                pa.field("error", pa.string()),
                pa.field("started_at", pa.timestamp("us", tz="UTC")),
                pa.field("completed_at", pa.timestamp("us", tz="UTC")),
            ],
        )
        workflow_runs = pa.Table.from_pylist(
            [run.model_dump() for run in runs],
            schema=schema,
        )
        with duckdb.connect() as con:
            print(
                con.sql(
                    """
                    SELECT *
                    FROM workflow_runs
                    ORDER BY started_at ASC
                    """,
                )
            )
