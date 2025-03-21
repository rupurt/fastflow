from pydantic import Field
from upath import UPath

from .base_obstore_settings import BaseObstoreSettings


class ObstoreColdSettings(BaseObstoreSettings):
    url: UPath = Field(default=UPath("gs://default-bucket"))
