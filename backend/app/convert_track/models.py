from enum import Enum


class StreamingPlatform(str, Enum):
    TIDAL = "tidal"
    SPOTIFY = "spotify"

    @classmethod
    def from_id(cls, id: str) -> "StreamingPlatform":
        if id.isnumeric():
            return cls.TIDAL
        else:
            return cls.SPOTIFY
