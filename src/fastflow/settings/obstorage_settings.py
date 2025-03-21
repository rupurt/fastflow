from pydantic import Field, BaseModel

from .obstore_cold_settings import ObstoreColdSettings
from .obstore_warm_settings import ObstoreWarmSettings
from .obstore_hot_settings import ObstoreHotSettings


class ObstorageSettings(BaseModel):
    cold: ObstoreColdSettings = Field(default_factory=ObstoreColdSettings)
    warm: ObstoreWarmSettings = Field(default_factory=ObstoreWarmSettings)
    hot: ObstoreHotSettings = Field(default_factory=ObstoreHotSettings)
