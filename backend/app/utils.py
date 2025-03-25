from fastapi import HTTPException
from .models import StreamingPlatform


def validate_platform_id(id: str) -> StreamingPlatform:
    """
    Validates the provided ID and returns the corresponding streaming platform.
    """
    try:
        return StreamingPlatform.from_id(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid album ID format.")
