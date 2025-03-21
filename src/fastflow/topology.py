from typing import List, Optional

from .settings import KafkaSettings
from .workflows import Workflow


class Topology:
    kafka: Optional[KafkaSettings]

    def __init__(
        self,
        kafka: Optional[KafkaSettings] = None,
    ):
        self.kafka = kafka

    async def migrate(
        self,
        app_name: str,
        workflows: List[Workflow],
    ):
        pass
