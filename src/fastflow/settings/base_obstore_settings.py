from obstore.store import (
    LocalStore,
    MemoryStore,
    GCSStore,
    S3Store,
    AzureStore,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from upath.implementations.cloud import (
    AzurePath,
    GCSPath,
    S3Path,
)
from upath.implementations.local import FilePath
from upath.implementations.memory import MemoryPath
from upath import UPath


type ObjectStore = MemoryStore | LocalStore | AzureStore | GCSStore | S3Store


class BaseObstoreSettings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    url: UPath = Field(default=UPath("memory://"))

    @property
    def obstore(self) -> ObjectStore:
        match self.url:
            case MemoryPath():
                return MemoryStore()
            case FilePath():
                return LocalStore.from_url(str(self.url))
            case AzurePath():
                return AzureStore.from_url(str(self.url))
            case GCSPath():
                return GCSStore.from_url(str(self.url))
            case S3Path():
                return S3Store.from_url(str(self.url))
            case _:
                raise RuntimeError(f"Unsupported url {self.url}")
