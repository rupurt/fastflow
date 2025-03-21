from typing import List, Optional

from pydantic import BaseModel, Field


class KafkaSettings(BaseModel):
    bootstrap_servers: List[str] = Field(default_factory=list)
    service_provider: Optional[str] = Field(default=None)
    topic_prefix: str = Field(default="fastflow")
