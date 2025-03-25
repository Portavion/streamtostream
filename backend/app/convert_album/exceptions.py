from typing import Optional


class APIError(Exception):
    """Custom exception for API-related errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
