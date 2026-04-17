import sys
from pathlib import Path

# Add src and scripts directories to sys.path for all tests
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "src"))
sys.path.insert(0, str(root_dir / "scripts"))
