from typing import Optional

from .settings import ObstorageSettings


class State:
    obstorage: Optional[ObstorageSettings]

    def __init__(
        self,
        obstorage: Optional[ObstorageSettings] = None,
    ):
        self.obstorage = obstorage

    async def migrate(self):
        pass
