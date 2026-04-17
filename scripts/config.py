import os
from pathlib import Path

# Load from environment variables with defaults matching the spec
MEMORY_PROJECT_ID = os.environ.get("MEMORY_PROJECT_ID", "project")
MEMORY_SCHEMA_VERSION = os.environ.get("MEMORY_SCHEMA_VERSION", "1.0")

# Paths
_repo_root = Path(__file__).resolve().parents[1]

_env_memory_root = os.environ.get("MEMORY_ROOT")
if _env_memory_root:
    MEMORY_ROOT = Path(_env_memory_root)
else:
    MEMORY_ROOT = _repo_root / ".storage"

_env_cache_root = os.environ.get("MEMORY_CACHE_ROOT")
if _env_cache_root:
    MEMORY_CACHE_ROOT = Path(_env_cache_root)
else:
    MEMORY_CACHE_ROOT = _repo_root / ".cache"

_env_global_root = os.environ.get("MEMORY_GLOBAL_ROOT")
if _env_global_root:
    MEMORY_GLOBAL_ROOT = Path(_env_global_root).expanduser()
else:
    MEMORY_GLOBAL_ROOT = Path("~/.trae/global_storage/").expanduser()

MEMORY_MAX_RESULTS = int(os.environ.get("MEMORY_MAX_RESULTS", "3"))

# Derived directories
REVIEWS_DIR = MEMORY_ROOT / "reviews"
CACHE_REVIEWS_DIR = MEMORY_CACHE_ROOT / "reviews"
GLOBAL_REVIEWS_DIR = MEMORY_GLOBAL_ROOT / "reviews"


def ensure_directories():
    """Ensure necessary directories exist."""
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    # Note: Global dir is only created if explicitly used/needed by scripts.
