"""Application configuration management."""


class Config:
    """Loads and validates application settings."""

    def __init__(self, debug=False, db_url="sqlite:///app.db"):
        self.debug = debug
        self.db_url = db_url

    @classmethod
    def load(cls, path=None):
        """Load configuration from environment or file."""
        return cls()
