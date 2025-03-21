from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class NewKafkaTopic:
    name: str
    num_partitions: int
    replication_factor: int
    replica_assignments: Optional[Dict] = None
    topic_configs: Optional[Dict] = None
