from fastflow import FastFlow
from typer import Typer


def command(app: Typer, flow: FastFlow):
    @app.command()
    def migrate():
        import asyncio

        asyncio.run(flow.migrate())
