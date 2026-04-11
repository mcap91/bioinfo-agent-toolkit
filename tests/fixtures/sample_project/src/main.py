"""Application entry point."""
from core.config import Config
from api.routes import create_app


def main():
    config = Config.load()
    app = create_app(config)
    app.run()


if __name__ == "__main__":
    main()
