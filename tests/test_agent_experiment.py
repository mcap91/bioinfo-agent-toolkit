#!/usr/bin/env python3
"""Phase 5: Agent A/B Experiment

Proves that /check_graph helps a Claude agent catch distant-impact changes.
Two Claude Code agents get the same rename task — one with graph tooling
(KB_INDEX.md, /check_graph skill, CLAUDE.md rules), one without.

The fixture project is enhanced with db_url references scattered across
multiple files at different graph depths, plus 25 noise files that do NOT
reference db_url. A correct rename touches all db_url references; any
remaining `db_url` is a miss.

Requirements:
    - Claude Code CLI (`claude` command on PATH)
    - API access configured (ANTHROPIC_API_KEY or OAuth)
    - kb-graph installed (`kb-graph` on PATH)

Usage:
    python3 tests/test_agent_experiment.py                  # 1 trial, default model
    python3 tests/test_agent_experiment.py --trials 3       # 3 trials
    python3 tests/test_agent_experiment.py --model sonnet   # use sonnet
    python3 tests/test_agent_experiment.py --save-transcripts  # keep agent output
    python3 tests/test_agent_experiment.py --clean          # wipe previous results first

Results are printed as a table and can be appended to phoam_paint/README.md.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "sample_project"

# ── Logging ──────────────────────────────────────────────────────────────
# All output goes to both stdout and the log file (if set).
# tail -f tests/experiment.log to watch progress.

_log_file = None


def log(msg=""):
    """Print to stdout and append to log file (if open)."""
    print(msg)
    if _log_file is not None:
        _log_file.write(msg + "\n")
        _log_file.flush()


# ── Version Info ─────────────────────────────────────────────────────────

def get_claude_version():
    """Get Claude CLI version string."""
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip() or result.stderr.strip() or "unknown"
    except Exception:
        return "unknown"


# ── Fixture Enhancement ─────────────────────────────────────────────────
# These rewrites add db_url references at multiple graph depths so the
# experiment has something for agents to miss.  Applied to COPIES only.
#
# The enhanced project has ~45 files total:
#   - 10 files with db_url references across 6 directories (depth 0-3)
#   - 25 noise files (no db_url) across multiple directories
#   - Original fixture files (some overwritten with enhanced versions)

ENHANCED_CONFIG_PY = """\
\"\"\"Application configuration management.\"\"\"


class Config:
    \"\"\"Loads and validates application settings.\"\"\"

    def __init__(self, debug=False, db_url="sqlite:///app.db"):
        self.debug = debug
        self.db_url = db_url

    @classmethod
    def load(cls, path=None):
        \"\"\"Load configuration from environment or file.\"\"\"
        return cls()

    def as_dict(self):
        \"\"\"Return config as a dictionary.\"\"\"
        return {"debug": self.debug, "db_url": self.db_url}
"""

ENHANCED_DATABASE_PY = """\
\"\"\"Database connection pool and query helpers.\"\"\"
from core.config import Config


class Database:
    \"\"\"Manages database connections.\"\"\"

    def __init__(self, config: Config):
        self.config = config
        self.db_url = config.db_url
        self._pool = []

    def get_connection(self):
        \"\"\"Get a connection from the pool.\"\"\"
        return self.db_url

    def execute(self, query, params=None):
        \"\"\"Execute a query and return results.\"\"\"
        return []
"""

ENHANCED_MAIN_PY = """\
\"\"\"Application entry point.\"\"\"
from core.config import Config
from api.routes import create_app


def main():
    config = Config(db_url="postgres://localhost/myapp")
    app = create_app(config)
    app.run()


if __name__ == "__main__":
    main()
"""

ENHANCED_ROUTES_PY = """\
\"\"\"REST API route definitions.\"\"\"
from core.database import Database
from core.config import Config
from .auth import verify_token


def create_app(config):
    \"\"\"Create and configure the application.\"\"\"
    db = Database(config)
    return App(db)


class App:
    \"\"\"Simple application wrapper.\"\"\"

    def __init__(self, db):
        self.db = db

    def run(self):
        \"\"\"Start the application.\"\"\"
        pass

    def health(self):
        \"\"\"Health check endpoint.\"\"\"
        return {"db_url": self.db.db_url, "status": "ok"}
"""

ENHANCED_SETTINGS_YAML = """\
# Application settings
app:
  name: "Sample Project"
  version: "1.0.0"

paths:
  config_module: "src/core/config.py"

database:
  db_url: "sqlite:///app.db"
  pool_size: 5
"""

# ── New files with db_url references (added to copies) ──────────────────

NEW_TEST_CONFIG_PY = """\
\"\"\"Tests for configuration loading.\"\"\"
import unittest


class TestConfig(unittest.TestCase):
    \"\"\"Verify Config class behavior.\"\"\"

    def test_default_db_url(self):
        from core.config import Config
        cfg = Config()
        self.assertEqual(cfg.db_url, "sqlite:///app.db")

    def test_custom_db_url(self):
        from core.config import Config
        cfg = Config(db_url="postgres://localhost/test")
        self.assertEqual(cfg.db_url, "postgres://localhost/test")

    def test_as_dict_includes_db_url(self):
        from core.config import Config
        cfg = Config()
        d = cfg.as_dict()
        self.assertIn("db_url", d)
"""

NEW_MIGRATE_PY = """\
\"\"\"Database migration runner.\"\"\"
import sys

from core.config import Config


def run_migrations(config):
    \"\"\"Apply pending migrations to the database.\"\"\"
    url = config.db_url
    print(f"Connecting to {url} for migrations...")
    # In production this would run Alembic or similar
    return True


def rollback(config, steps=1):
    \"\"\"Roll back the last N migrations.\"\"\"
    print(f"Rolling back {steps} migration(s) on {config.db_url}")
    return True


if __name__ == "__main__":
    cfg = Config(db_url=sys.argv[1] if len(sys.argv) > 1 else None)
    run_migrations(cfg)
"""

NEW_MIDDLEWARE_PY = """\
\"\"\"Request middleware for logging and metrics.\"\"\"
from core.database import Database


class RequestLogger:
    \"\"\"Logs each request with database connection info.\"\"\"

    def __init__(self, database: Database):
        self._db = database
        # Attribute access through intermediate variable
        self._connection_url = database.db_url

    def log_request(self, method, path):
        \"\"\"Log an incoming request.\"\"\"
        return f"{method} {path} -> {self._connection_url}"
"""

NEW_CLI_PY = """\
\"\"\"CLI entry point — wraps the application for command-line usage.\"\"\"
from api.routes import create_app
from core.config import Config


def cli_main():
    \"\"\"Parse CLI args and start the app.\"\"\"
    config = Config.load()
    app = create_app(config)

    # Print startup info including connection details
    health = app.health()
    print(f"Starting server with db_url={health['db_url']}")
    app.run()


if __name__ == "__main__":
    cli_main()
"""

NEW_DEPLOYMENT_MD = """\
# Deployment Guide

## Environment Variables

Set the following before deploying:

```python
# Production database configuration
config = Config(db_url="postgres://prod-host:5432/myapp")
```

## Docker Compose

```yaml
services:
  app:
    environment:
      - DB_URL=postgres://db:5432/app
```

## Health Check

After deploying, verify the `/health` endpoint returns the correct `db_url`.
"""

NEW_SEED_PY = """\
\"\"\"Database seeding script — populates initial data.\"\"\"
from core.config import Config
from core.database import Database


def seed_database():
    \"\"\"Insert seed data into the database.\"\"\"
    config = Config()
    db = Database(config)
    # Dict unpacking — db_url is a key in the config dict
    config_dict = config.as_dict()
    merged = {**config_dict, "pool_size": 10}
    print(f"Seeding database at {merged['db_url']}...")
    return True


if __name__ == "__main__":
    seed_database()
"""

NEW_HEALTH_CHECK_SH = """\
#!/usr/bin/env bash
# Health check script — verifies the app is running
set -euo pipefail

RESPONSE=$(curl -s http://localhost:8000/health)
DB_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['db_url'])")

if [ -z "$DB_URL" ]; then
    echo "FAIL: db_url not found in health response"
    exit 1
fi

echo "OK: connected to $DB_URL"
"""

NEW_ENV_EXAMPLE = """\
# Environment configuration template
# Copy to .env and fill in values

# Database
DB_URL=sqlite:///dev.db

# Application
DEBUG=true
PORT=8000
"""

# Map of NEW files to create (paths relative to project root)
NEW_FILES = {
    "tests/test_config.py": NEW_TEST_CONFIG_PY,
    "scripts/migrate.py": NEW_MIGRATE_PY,
    "src/api/middleware.py": NEW_MIDDLEWARE_PY,
    "src/cli.py": NEW_CLI_PY,
    "docs/deployment.md": NEW_DEPLOYMENT_MD,
    "scripts/seed.py": NEW_SEED_PY,
    "scripts/health_check.sh": NEW_HEALTH_CHECK_SH,
    ".env.example": NEW_ENV_EXAMPLE,
}

# ── Noise files (no db_url references) ──────────────────────────────────
# These make the project large enough that exhaustive grep is expensive.
# The agent has to search through ~45 files total; the graph cuts through
# the noise by surfacing only the connected files.

NOISE_FILES = {
    # src/core/ — utility modules
    "src/core/logging.py": '''\
"""Structured logging for the application."""


class Logger:
    """JSON-based structured logger."""

    def __init__(self, name, level="INFO"):
        self.name = name
        self.level = level

    def info(self, msg, **kwargs):
        """Log an info-level message."""
        print(f"[{self.level}] {self.name}: {msg}")

    def error(self, msg, **kwargs):
        """Log an error-level message."""
        print(f"[ERROR] {self.name}: {msg}")

    def with_context(self, **ctx):
        """Return a child logger with extra context."""
        return Logger(f"{self.name}.child", self.level)
''',
    "src/core/cache.py": '''\
"""In-memory cache with TTL support."""
import time


class Cache:
    """Simple TTL cache backed by a dict."""

    def __init__(self, default_ttl=300):
        self._store = {}
        self._ttl = default_ttl

    def get(self, key):
        """Retrieve a cached value if it hasn't expired."""
        entry = self._store.get(key)
        if entry and entry["expires"] > time.time():
            return entry["value"]
        return None

    def set(self, key, value, ttl=None):
        """Store a value with optional TTL override."""
        self._store[key] = {
            "value": value,
            "expires": time.time() + (ttl or self._ttl),
        }

    def clear(self):
        """Remove all cached entries."""
        self._store.clear()
''',
    "src/core/exceptions.py": '''\
"""Application exception hierarchy."""


class AppError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


class NotFoundError(AppError):
    """Resource not found."""

    def __init__(self, resource, identifier):
        super().__init__(f"{resource} {identifier} not found", code=404)


class ValidationError(AppError):
    """Input validation failed."""

    def __init__(self, field, reason):
        super().__init__(f"Invalid {field}: {reason}", code=400)


class AuthenticationError(AppError):
    """Authentication failed."""

    def __init__(self, reason="invalid credentials"):
        super().__init__(reason, code=401)
''',
    "src/core/validators.py": '''\
"""Input validation utilities."""
import re


def validate_email(email):
    """Check if an email address is syntactically valid."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_slug(slug):
    """Check if a string is a valid URL slug."""
    return bool(re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug))


def validate_port(port):
    """Check if a port number is in valid range."""
    return isinstance(port, int) and 1 <= port <= 65535


def sanitize_string(value, max_length=255):
    """Strip whitespace and truncate to max length."""
    return value.strip()[:max_length] if value else ""
''',
    # src/api/ — more route handlers and serializers
    "src/api/serializers.py": '''\
"""Response serialization helpers."""
import json
from datetime import datetime


class JSONSerializer:
    """Serialize objects to JSON with datetime support."""

    @staticmethod
    def serialize(obj):
        """Convert an object to a JSON string."""
        return json.dumps(obj, default=str)

    @staticmethod
    def deserialize(data):
        """Parse a JSON string into a Python object."""
        return json.loads(data)


def format_response(data, status=200):
    """Wrap data in a standard API response envelope."""
    return {
        "status": status,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }


def paginate(items, page=1, per_page=20):
    """Paginate a list of items."""
    start = (page - 1) * per_page
    return {
        "items": items[start:start + per_page],
        "page": page,
        "per_page": per_page,
        "total": len(items),
    }
''',
    "src/api/users.py": '''\
"""User management endpoints."""


class UserService:
    """CRUD operations for user accounts."""

    def __init__(self):
        self._users = {}

    def create(self, username, email):
        """Create a new user account."""
        user_id = len(self._users) + 1
        self._users[user_id] = {"username": username, "email": email}
        return user_id

    def get(self, user_id):
        """Retrieve a user by ID."""
        return self._users.get(user_id)

    def list_all(self):
        """List all registered users."""
        return list(self._users.values())

    def delete(self, user_id):
        """Remove a user account."""
        return self._users.pop(user_id, None) is not None
''',
    "src/api/pagination.py": '''\
"""Cursor-based pagination for API endpoints."""


class Cursor:
    """Opaque cursor for stable pagination."""

    def __init__(self, offset=0, limit=20):
        self.offset = offset
        self.limit = limit

    def next(self):
        """Return the cursor for the next page."""
        return Cursor(self.offset + self.limit, self.limit)

    def prev(self):
        """Return the cursor for the previous page."""
        return Cursor(max(0, self.offset - self.limit), self.limit)

    def apply(self, queryset):
        """Slice a list according to this cursor."""
        return queryset[self.offset:self.offset + self.limit]
''',
    "src/api/rate_limiter.py": '''\
"""Token-bucket rate limiter for API endpoints."""
import time


class RateLimiter:
    """Per-client rate limiter using token bucket algorithm."""

    def __init__(self, rate=10, burst=20):
        self.rate = rate
        self.burst = burst
        self._buckets = {}

    def allow(self, client_id):
        """Check if a request from client_id should be allowed."""
        now = time.time()
        bucket = self._buckets.get(client_id, {"tokens": self.burst, "last": now})
        elapsed = now - bucket["last"]
        bucket["tokens"] = min(self.burst, bucket["tokens"] + elapsed * self.rate)
        bucket["last"] = now

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            self._buckets[client_id] = bucket
            return True
        self._buckets[client_id] = bucket
        return False
''',
    # src/workers/ — background task processing
    "src/workers/__init__.py": "",
    "src/workers/task_queue.py": '''\
"""Simple in-memory task queue for background processing."""
import threading
from collections import deque


class TaskQueue:
    """Thread-safe FIFO task queue."""

    def __init__(self):
        self._queue = deque()
        self._lock = threading.Lock()

    def enqueue(self, task):
        """Add a task to the queue."""
        with self._lock:
            self._queue.append(task)

    def dequeue(self):
        """Remove and return the next task, or None if empty."""
        with self._lock:
            return self._queue.popleft() if self._queue else None

    def size(self):
        """Return the number of pending tasks."""
        return len(self._queue)
''',
    "src/workers/email_worker.py": '''\
"""Worker for sending transactional emails."""


class EmailWorker:
    """Processes email sending tasks from the queue."""

    def __init__(self, smtp_host="localhost", smtp_port=587):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send(self, to, subject, body):
        """Send an email (stub — prints instead of sending)."""
        print(f"EMAIL to={to} subject={subject}")
        return True

    def send_welcome(self, user):
        """Send a welcome email to a new user."""
        return self.send(user["email"], "Welcome!", f"Hi {user['username']}")
''',
    "src/workers/cleanup_worker.py": '''\
"""Worker for periodic cleanup tasks."""
import time


class CleanupWorker:
    """Removes expired sessions and stale temp files."""

    def __init__(self, interval=3600):
        self.interval = interval
        self._last_run = 0

    def should_run(self):
        """Check if enough time has passed since last cleanup."""
        return time.time() - self._last_run > self.interval

    def run(self):
        """Execute cleanup tasks."""
        self._last_run = time.time()
        expired = self._cleanup_sessions()
        stale = self._cleanup_temp()
        return {"sessions": expired, "temp_files": stale}

    def _cleanup_sessions(self):
        return 0

    def _cleanup_temp(self):
        return 0
''',
    # tests/ — test files that don't reference db_url
    "tests/__init__.py": "",
    "tests/test_validators.py": '''\
"""Tests for input validation utilities."""
import unittest


class TestValidators(unittest.TestCase):
    """Verify validation functions work correctly."""

    def test_valid_email(self):
        self.assertTrue(True)  # placeholder

    def test_invalid_email(self):
        self.assertTrue(True)

    def test_valid_slug(self):
        self.assertTrue(True)

    def test_port_range(self):
        self.assertTrue(True)

    def test_sanitize_whitespace(self):
        self.assertTrue(True)
''',
    "tests/test_cache.py": '''\
"""Tests for the caching layer."""
import unittest


class TestCache(unittest.TestCase):
    """Verify cache get/set/clear operations."""

    def test_set_and_get(self):
        self.assertTrue(True)

    def test_expired_entry_returns_none(self):
        self.assertTrue(True)

    def test_clear_removes_all(self):
        self.assertTrue(True)
''',
    "tests/test_serializers.py": '''\
"""Tests for response serialization."""
import unittest


class TestSerializers(unittest.TestCase):
    """Verify JSON serialization and response formatting."""

    def test_serialize_dict(self):
        self.assertTrue(True)

    def test_format_response_envelope(self):
        self.assertTrue(True)

    def test_paginate_items(self):
        self.assertTrue(True)

    def test_paginate_empty_list(self):
        self.assertTrue(True)
''',
    "tests/test_users.py": '''\
"""Tests for user management service."""
import unittest


class TestUserService(unittest.TestCase):
    """Verify user CRUD operations."""

    def test_create_user(self):
        self.assertTrue(True)

    def test_get_user_by_id(self):
        self.assertTrue(True)

    def test_delete_user(self):
        self.assertTrue(True)

    def test_list_all_users(self):
        self.assertTrue(True)
''',
    "tests/test_rate_limiter.py": '''\
"""Tests for rate limiting."""
import unittest


class TestRateLimiter(unittest.TestCase):
    """Verify token-bucket rate limiter."""

    def test_allows_within_limit(self):
        self.assertTrue(True)

    def test_blocks_over_limit(self):
        self.assertTrue(True)

    def test_tokens_refill(self):
        self.assertTrue(True)
''',
    "tests/test_auth.py": '''\
"""Tests for authentication and authorization."""
import unittest


class TestAuth(unittest.TestCase):
    """Verify token validation and user lookup."""

    def test_valid_token(self):
        self.assertTrue(True)

    def test_invalid_token(self):
        self.assertTrue(True)

    def test_expired_token(self):
        self.assertTrue(True)
''',
    "tests/test_routes.py": '''\
"""Tests for API route handlers."""
import unittest


class TestRoutes(unittest.TestCase):
    """Verify endpoint behavior."""

    def test_health_endpoint(self):
        self.assertTrue(True)

    def test_create_returns_201(self):
        self.assertTrue(True)

    def test_not_found_returns_404(self):
        self.assertTrue(True)

    def test_auth_required(self):
        self.assertTrue(True)
''',
    # scripts/ — operational scripts without db_url
    "scripts/lint.sh": '''\
#!/usr/bin/env bash
# Run code quality checks
set -euo pipefail
echo "Running flake8..."
echo "Running mypy..."
echo "All checks passed."
''',
    "scripts/build.sh": '''\
#!/usr/bin/env bash
# Build the application for deployment
set -euo pipefail
echo "Building application..."
echo "Build complete."
''',
    # docs/ — documentation without db_url
    "docs/architecture.md": '''\
# Architecture

## Overview

The application follows a layered architecture:

1. **API Layer** — HTTP routing and request handling
2. **Service Layer** — Business logic and validation
3. **Data Layer** — Database access and query building

## Directory Structure

```
src/
  api/        HTTP handlers, middleware, serializers
  core/       Config, database, logging, caching
  workers/    Background task processing
```

## Design Decisions

- Single-process deployment for simplicity
- In-memory caching with configurable TTL
- Token-bucket rate limiting per client
''',
    "docs/contributing.md": '''\
# Contributing

## Setup

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run tests: `python -m pytest tests/`

## Code Style

- Follow PEP 8
- Use type hints for public APIs
- Write docstrings for all public functions

## Pull Requests

- One feature per PR
- Include tests for new functionality
- Update documentation as needed
''',
}

# Map of relative paths to enhanced content (overwrite existing fixture files)
ENHANCEMENTS = {
    "src/core/config.py": ENHANCED_CONFIG_PY,
    "src/core/database.py": ENHANCED_DATABASE_PY,
    "src/main.py": ENHANCED_MAIN_PY,
    "src/api/routes.py": ENHANCED_ROUTES_PY,
    "config/settings.yaml": ENHANCED_SETTINGS_YAML,
}

# Files that should contain db_url after enhancement (for measurement)
DB_URL_FILES = [
    "src/core/config.py",     # depth 0 — definition + as_dict()
    "src/core/database.py",   # depth 1 — direct usage
    "src/main.py",            # depth 1 — keyword arg
    "src/api/routes.py",      # depth 2 — via database, health endpoint
    "src/api/middleware.py",   # depth 2 — attribute access through intermediate var
    "src/cli.py",             # depth 3 — calls app.health() which has db_url
    "config/settings.yaml",   # config-ref — yaml key
    "tests/test_config.py",   # test — asserts on db_url
    "scripts/migrate.py",     # script — reads config.db_url
    "scripts/seed.py",        # script — dict unpacking with db_url key
    "scripts/health_check.sh",  # shell — parses db_url from JSON response
    "docs/deployment.md",     # doc — db_url in code fences
]

# ── Agent Prompts ────────────────────────────────────────────────────────

PROMPT_A = (
    "Rename the db_url parameter to database_url in config.py. "
    "Update all code that references db_url throughout this project. "
    "Do not explain, just make the changes."
)

PROMPT_B = (
    "First read CLAUDE.md, then run the check_graph skill to analyze the impact "
    "of renaming db_url to database_url in config.py. After reviewing the impact "
    "report, make the rename — update config.py and every file that references "
    "db_url. Do not explain, just make the changes."
)


# ── Helpers ──────────────────────────────────────────────────────────────

def check_prerequisites():
    """Verify claude CLI and kb-graph are available."""
    missing = []
    for cmd in ("claude", "kb-graph"):
        if shutil.which(cmd) is None:
            missing.append(cmd)
    if missing:
        msg = f"ERROR: Missing prerequisites: {', '.join(missing)}"
        log(msg)
        log("Install claude CLI and kb-graph before running this experiment.")
        sys.exit(1)


def create_enhanced_project(dest):
    """Copy fixture project to dest, apply enhancements, add new files and noise."""
    shutil.copytree(FIXTURE_DIR, dest)

    # Overwrite existing files with enhanced versions
    for rel_path, content in ENHANCEMENTS.items():
        filepath = Path(dest) / rel_path
        filepath.write_text(content)

    # Create new files with db_url references
    for rel_path, content in NEW_FILES.items():
        filepath = Path(dest) / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)

    # Create noise files (no db_url)
    for rel_path, content in NOISE_FILES.items():
        filepath = Path(dest) / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)


def init_graph(project_dir):
    """Run kb-graph init on a project directory."""
    # Need a git repo for init (it sets core.hooksPath)
    subprocess.run(
        ["git", "init", "-q"],
        cwd=project_dir,
        capture_output=True,
    )
    subprocess.run(
        ["git", "add", "."],
        cwd=project_dir,
        capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-q", "-m", "initial", "--no-gpg-sign"],
        cwd=project_dir,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@test",
             "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@test"},
    )
    result = subprocess.run(
        ["kb-graph", "init", "."],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log(f"WARNING: kb-graph init failed:\n{result.stderr}")
    return result.returncode == 0


def run_agent(project_dir, prompt, *, model=None, timeout=120):
    """Spawn a Claude Code subprocess and return (stdout, stderr, returncode, elapsed)."""
    cmd = [
        "claude",
        "-p", prompt,
        "--dangerously-skip-permissions",
        "--no-session-persistence",
    ]
    if model:
        cmd.extend(["--model", model])

    start = time.monotonic()
    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"},
        )
        elapsed = time.monotonic() - start
        return result.stdout, result.stderr, result.returncode, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        return "", f"TIMEOUT after {timeout}s", -1, elapsed


def _scan_file_for_pattern(filepath, pattern):
    """Scan a file for a regex pattern, returning matching lines.

    Handles text files only — skips binary files gracefully.
    """
    try:
        content = filepath.read_text()
    except (UnicodeDecodeError, PermissionError):
        return []
    matching = []
    for i, line in enumerate(content.splitlines(), 1):
        if re.search(pattern, line):
            matching.append(f"  L{i}: {line.strip()}")
    return matching


def count_db_url_refs(project_dir):
    """Count remaining db_url references (word-boundary match, excludes database_url).

    Scans the known DB_URL_FILES list. Returns dict: {relative_path: [matching_lines]}.
    """
    pattern = r'(?<![a-zA-Z_])db_url(?![a-zA-Z_])'
    hits = {}
    for rel_path in DB_URL_FILES:
        filepath = Path(project_dir) / rel_path
        if not filepath.exists():
            continue
        matching = _scan_file_for_pattern(filepath, pattern)
        if matching:
            hits[rel_path] = matching
    return hits


def count_database_url_refs(project_dir):
    """Count database_url references (the renamed version).

    Returns dict: {relative_path: count} for files with hits.
    """
    hits = {}
    for rel_path in DB_URL_FILES:
        filepath = Path(project_dir) / rel_path
        if not filepath.exists():
            continue
        try:
            content = filepath.read_text()
        except (UnicodeDecodeError, PermissionError):
            continue
        count = len(re.findall(r'(?<![a-zA-Z_])database_url(?![a-zA-Z_])', content))
        if count > 0:
            hits[rel_path] = count
    return hits


def total_expected_refs():
    """Count how many lines contain db_url in all enhanced/new files.

    Counts lines (not individual matches per line) to be consistent
    with count_db_url_refs which also counts lines.
    """
    pattern = r'(?<![a-zA-Z_])db_url(?![a-zA-Z_])'
    total = 0
    all_sources = {**ENHANCEMENTS, **NEW_FILES}
    for content in all_sources.values():
        for line in content.splitlines():
            if re.search(pattern, line):
                total += 1
    return total


# ── Trial Runner ─────────────────────────────────────────────────────────

def run_trial(trial_num, *, model=None, save_transcripts=False, timeout=120):
    """Run one A/B trial. Returns a result dict."""
    log(f"\n{'='*60}")
    log(f"  Trial {trial_num}")
    log(f"{'='*60}")

    tmpdir = tempfile.mkdtemp(prefix=f"kb_graph_ab_{trial_num}_")
    dir_a = os.path.join(tmpdir, "project_a")
    dir_b = os.path.join(tmpdir, "project_b")

    try:
        # Set up both projects
        log(f"  Setting up projects in {tmpdir}")
        create_enhanced_project(dir_a)
        create_enhanced_project(dir_b)

        # Verify enhancement worked
        expected = total_expected_refs()
        refs_a = count_db_url_refs(dir_a)
        pre_count = sum(len(v) for v in refs_a.values())
        log(f"  Enhanced fixture: {pre_count} db_url references across {len(refs_a)} files")
        assert pre_count == expected, f"Expected {expected} refs, got {pre_count}"

        # Init graph on project B only
        log("  Running kb-graph init on project B...")
        if not init_graph(dir_b):
            log("  WARNING: kb-graph init had issues, continuing anyway")

        # Verify B has the graph artifacts
        has_index = (Path(dir_b) / "KB_INDEX.md").exists()
        has_skill = (Path(dir_b) / ".claude" / "skills" / "check_graph" / "SKILL.md").exists()
        has_claude_md = (Path(dir_b) / "CLAUDE.md").exists()
        log(f"  Project B: KB_INDEX.md={has_index}, check_graph={has_skill}, CLAUDE.md={has_claude_md}")

        # Run Agent A (no graph)
        log(f"\n  Running Agent A (no graph)...")
        stdout_a, stderr_a, rc_a, elapsed_a = run_agent(
            dir_a, PROMPT_A, model=model, timeout=timeout
        )
        log(f"  Agent A finished in {elapsed_a:.1f}s (exit={rc_a})")

        # Run Agent B (with graph)
        log(f"  Running Agent B (with graph)...")
        stdout_b, stderr_b, rc_b, elapsed_b = run_agent(
            dir_b, PROMPT_B, model=model, timeout=timeout
        )
        log(f"  Agent B finished in {elapsed_b:.1f}s (exit={rc_b})")

        # Measure results
        remaining_a = count_db_url_refs(dir_a)
        remaining_b = count_db_url_refs(dir_b)
        renamed_a = count_database_url_refs(dir_a)
        renamed_b = count_database_url_refs(dir_b)

        missed_a = sum(len(v) for v in remaining_a.values())
        missed_b = sum(len(v) for v in remaining_b.values())
        updated_a = sum(renamed_a.values())
        updated_b = sum(renamed_b.values())

        files_missed_a = sorted(remaining_a.keys())
        files_missed_b = sorted(remaining_b.keys())

        log(f"\n  Results:")
        log(f"  Agent A: {updated_a}/{expected} renamed, {missed_a} remaining in {files_missed_a}")
        log(f"  Agent B: {updated_b}/{expected} renamed, {missed_b} remaining in {files_missed_b}")

        if remaining_a:
            log(f"\n  Agent A missed:")
            for f, lines in sorted(remaining_a.items()):
                log(f"    {f}:")
                for line in lines:
                    log(f"      {line}")

        if remaining_b:
            log(f"\n  Agent B missed:")
            for f, lines in sorted(remaining_b.items()):
                log(f"    {f}:")
                for line in lines:
                    log(f"      {line}")

        # Save transcripts
        if save_transcripts:
            ts_dir = REPO_ROOT / "tests" / "experiment_transcripts"
            ts_dir.mkdir(exist_ok=True)
            (ts_dir / f"trial_{trial_num}_agent_a.txt").write_text(
                f"=== PROMPT ===\n{PROMPT_A}\n\n=== STDOUT ===\n{stdout_a}\n\n=== STDERR ===\n{stderr_a}\n"
            )
            (ts_dir / f"trial_{trial_num}_agent_b.txt").write_text(
                f"=== PROMPT ===\n{PROMPT_B}\n\n=== STDOUT ===\n{stdout_b}\n\n=== STDERR ===\n{stderr_b}\n"
            )
            log(f"\n  Transcripts saved to {ts_dir}/trial_{trial_num}_*.txt")

        return {
            "trial": trial_num,
            "expected_refs": expected,
            "agent_a": {
                "renamed": updated_a,
                "remaining": missed_a,
                "files_missed": files_missed_a,
                "detail": remaining_a,
                "elapsed": elapsed_a,
                "exit_code": rc_a,
            },
            "agent_b": {
                "renamed": updated_b,
                "remaining": missed_b,
                "files_missed": files_missed_b,
                "detail": remaining_b,
                "elapsed": elapsed_b,
                "exit_code": rc_b,
            },
        }

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ── Summary ──────────────────────────────────────────────────────────────

def print_summary(results):
    """Print a summary table of all trials."""
    expected = results[0]["expected_refs"]

    log(f"\n{'='*70}")
    log(f"  EXPERIMENT SUMMARY — {len(results)} trial(s), {expected} db_url refs per project")
    log(f"{'='*70}\n")

    # Per-trial table
    log(f"  {'Trial':>5}  {'A missed':>8}  {'B missed':>8}  {'A files missed':>30}  {'B files missed':>30}  {'A time':>8}  {'B time':>8}")
    log(f"  {'─'*5}  {'─'*8}  {'─'*8}  {'─'*30}  {'─'*30}  {'─'*8}  {'─'*8}")
    for r in results:
        a = r["agent_a"]
        b = r["agent_b"]
        a_files = ", ".join(Path(f).name for f in a["files_missed"]) or "none"
        b_files = ", ".join(Path(f).name for f in b["files_missed"]) or "none"
        log(f"  {r['trial']:>5}  {a['remaining']:>8}  {b['remaining']:>8}  {a_files:>30}  {b_files:>30}  {a['elapsed']:>7.1f}s  {b['elapsed']:>7.1f}s")

    # Aggregates
    a_totals = [r["agent_a"]["remaining"] for r in results]
    b_totals = [r["agent_b"]["remaining"] for r in results]
    a_times = [r["agent_a"]["elapsed"] for r in results]
    b_times = [r["agent_b"]["elapsed"] for r in results]
    a_perfect = sum(1 for x in a_totals if x == 0)
    b_perfect = sum(1 for x in b_totals if x == 0)
    n = len(results)

    log(f"\n  Perfect runs (0 remaining): Agent A = {a_perfect}/{n} ({a_perfect/n*100:.0f}%), Agent B = {b_perfect}/{n} ({b_perfect/n*100:.0f}%)")
    log(f"  Avg remaining refs:         Agent A = {sum(a_totals)/n:.1f}, Agent B = {sum(b_totals)/n:.1f}")
    log(f"  Avg time:                   Agent A = {sum(a_times)/n:.1f}s, Agent B = {sum(b_times)/n:.1f}s")

    # Files most commonly missed
    a_miss_counts = {}
    b_miss_counts = {}
    for r in results:
        for f in r["agent_a"]["files_missed"]:
            a_miss_counts[f] = a_miss_counts.get(f, 0) + 1
        for f in r["agent_b"]["files_missed"]:
            b_miss_counts[f] = b_miss_counts.get(f, 0) + 1

    if a_miss_counts or b_miss_counts:
        log(f"\n  Files missed (across trials):")
        all_files = sorted(set(list(a_miss_counts.keys()) + list(b_miss_counts.keys())))
        for f in all_files:
            a_n = a_miss_counts.get(f, 0)
            b_n = b_miss_counts.get(f, 0)
            log(f"    {f}: Agent A = {a_n}/{n}, Agent B = {b_n}/{n}")

    # Verdict
    log(f"\n  Verdict:")
    if sum(b_totals) < sum(a_totals):
        improvement = (1 - sum(b_totals) / max(sum(a_totals), 1)) * 100
        log(f"  → Agent B (with /check_graph) missed {improvement:.0f}% fewer references overall.")
    elif sum(b_totals) == sum(a_totals):
        log(f"  → Both agents performed equally.")
    else:
        log(f"  → Agent A (no graph) caught more references — unexpected result.")

    return {
        "trials": n,
        "expected_refs": expected,
        "a_perfect": a_perfect,
        "b_perfect": b_perfect,
        "a_avg_remaining": sum(a_totals) / n,
        "b_avg_remaining": sum(b_totals) / n,
        "a_avg_time": sum(a_times) / n,
        "b_avg_time": sum(b_times) / n,
        "a_miss_files": a_miss_counts,
        "b_miss_files": b_miss_counts,
    }


# ── Main ─────────────────────────────────────────────────────────────────

def clean_previous_results():
    """Remove old transcripts, log, and results JSON."""
    targets = [
        REPO_ROOT / "tests" / "experiment.log",
        REPO_ROOT / "tests" / "experiment_results.json",
    ]
    ts_dir = REPO_ROOT / "tests" / "experiment_transcripts"
    removed = []
    for t in targets:
        if t.exists():
            t.unlink()
            removed.append(str(t.relative_to(REPO_ROOT)))
    if ts_dir.exists():
        shutil.rmtree(ts_dir)
        removed.append(str(ts_dir.relative_to(REPO_ROOT)))
    return removed


def count_project_files(project_dir):
    """Count total files in the project (for logging)."""
    count = 0
    for root, dirs, files in os.walk(project_dir):
        # Skip .git and __pycache__
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".claude")]
        count += len(files)
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Phase 5: Agent A/B Experiment — does /check_graph help agents catch distant-impact changes?"
    )
    parser.add_argument(
        "--trials", type=int, default=1,
        help="Number of A/B trials to run (default: 1)",
    )
    parser.add_argument(
        "--model", type=str, default=None,
        help="Claude model to use (e.g., 'sonnet', 'opus'). Default: Claude Code default.",
    )
    parser.add_argument(
        "--save-transcripts", action="store_true",
        help="Save full agent stdout/stderr to tests/experiment_transcripts/",
    )
    parser.add_argument(
        "--timeout", type=int, default=180,
        help="Timeout per agent in seconds (default: 180)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Set up fixtures and measure baseline without running agents",
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Wipe previous results (transcripts, log, results JSON) before starting",
    )
    parser.add_argument(
        "--log", type=str,
        default=str(REPO_ROOT / "tests" / "experiment.log"),
        help="Log file path (default: tests/experiment.log). Use 'tail -f' to watch.",
    )
    args = parser.parse_args()

    # Clean previous results if requested
    if args.clean:
        removed = clean_previous_results()
        if removed:
            print(f"  Cleaned: {', '.join(removed)}")
        else:
            print("  Nothing to clean.")

    # Open log file
    global _log_file
    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    _log_file = open(log_path, "a")

    # Version info
    claude_version = get_claude_version()
    model_id = args.model or "default"
    started_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    log(f"\n{'─'*60}")
    log(f"  Experiment started at {started_at}")
    log(f"  Claude CLI: {claude_version}")
    log(f"  Model: {model_id}")
    log(f"  Log file: {log_path}")
    log(f"  Watch progress: tail -f {log_path}")
    log(f"{'─'*60}")

    check_prerequisites()

    log("Phase 5: Agent A/B Experiment")
    log(f"  Trials: {args.trials}")
    log(f"  Model: {model_id}")
    log(f"  Timeout: {args.timeout}s per agent")
    log(f"  Expected db_url refs: {total_expected_refs()}")
    log(f"  DB_URL_FILES: {len(DB_URL_FILES)} files across {len(set(str(Path(f).parent) for f in DB_URL_FILES))} directories")
    log(f"  Noise files: {len(NOISE_FILES)}")

    if args.dry_run:
        # Just set up one fixture and show what it looks like
        tmpdir = tempfile.mkdtemp(prefix="kb_graph_ab_dry_")
        project = os.path.join(tmpdir, "project")
        create_enhanced_project(project)
        total_files = count_project_files(project)
        refs = count_db_url_refs(project)
        log(f"\n  Dry run — enhanced fixture: {total_files} files total")
        log(f"  db_url references:")
        for f, lines in sorted(refs.items()):
            log(f"    {f}:")
            for line in lines:
                log(f"      {line}")
        log(f"\n  Total: {sum(len(v) for v in refs.values())} references across {len(refs)} files")

        # Also show kb-graph init output
        log(f"\n  Testing kb-graph init...")
        if init_graph(project):
            log("  kb-graph init succeeded")
            index = Path(project) / "KB_INDEX.md"
            if index.exists():
                # Show first few lines
                lines = index.read_text().splitlines()[:5]
                for line in lines:
                    log(f"    {line}")
        shutil.rmtree(tmpdir, ignore_errors=True)
        return

    results = []
    for i in range(1, args.trials + 1):
        result = run_trial(
            i,
            model=args.model,
            save_transcripts=args.save_transcripts,
            timeout=args.timeout,
        )
        results.append(result)

    summary = print_summary(results)

    # Save results JSON
    results_path = REPO_ROOT / "tests" / "experiment_results.json"
    with open(results_path, "w") as f:
        serializable = []
        for r in results:
            sr = {**r}
            sr["agent_a"] = {**r["agent_a"]}
            sr["agent_b"] = {**r["agent_b"]}
            serializable.append(sr)
        json.dump({
            "meta": {
                "started_at": started_at,
                "claude_version": claude_version,
                "model": model_id,
                "total_project_files": len(ENHANCEMENTS) + len(NEW_FILES) + len(NOISE_FILES),
                "db_url_files": len(DB_URL_FILES),
                "expected_refs": total_expected_refs(),
            },
            "results": serializable,
            "summary": summary,
        }, f, indent=2)
    log(f"\n  Results saved to {results_path}")

    if _log_file is not None:
        _log_file.close()


if __name__ == "__main__":
    main()
