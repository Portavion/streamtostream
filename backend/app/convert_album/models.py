from pydantic import BaseModel
from enum import Enum


class Album(BaseModel):
    artist: str
    album_name: str
    release_date: str
    upc: str


class StreamingPlatform(str, Enum):
    TIDAL = "tidal"
    SPOTIFY = "spotify"

    @classmethod
    def from_id(cls, id: str) -> "StreamingPlatform":
        if id.isnumeric():
            return cls.TIDAL
        else:
            return cls.SPOTIFY
