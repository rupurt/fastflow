from pydantic import BaseModel, Field


class BaseServerSettings(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field()
    log_level: str = Field(default="info")
    debug: bool = Field(default=False)
