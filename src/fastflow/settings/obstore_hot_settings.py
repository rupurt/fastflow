from pydantic import Field
from upath import UPath

from .base_obstore_settings import BaseObstoreSettings


class ObstoreHotSettings(BaseObstoreSettings):
    url: UPath = Field(default=UPath("memory://"))
