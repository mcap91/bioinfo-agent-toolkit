"""REST API route definitions."""
from core.database import Database
from core.config import Config
from .auth import verify_token


def create_app(config):
    """Create and configure the application."""
    db = Database(config)
    return App(db)


class App:
    """Simple application wrapper."""

    def __init__(self, db):
        self.db = db

    def run(self):
        """Start the application."""
        pass
