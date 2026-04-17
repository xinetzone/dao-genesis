import json
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Ensure we can import from the same directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import REVIEWS_DIR

def archive_stale_memories(days=365):
    """
    Parse all JSON records in .storage/reviews/.
    For any record older than `days`, change status to `archived` and save.
    Returns the number of archived records.
    """
    if not REVIEWS_DIR.exists():
        return 0

    archived_count = 0
    now = datetime.now(timezone.utc)
    cutoff_date = now - timedelta(days=days)

    for file_path in REVIEWS_DIR.glob("*.json"):
        try:
            content = file_path.read_text(encoding="utf-8")
            record = json.loads(content)
            
            # Skip if already archived
            if record.get("status") == "archived":
                continue
            
            timestamp_str = record.get("timestamp")
            if not timestamp_str:
                continue
                
            # Parse timestamp (handle Z suffix for UTC)
            if timestamp_str.endswith("Z"):
                timestamp_str = timestamp_str[:-1] + "+00:00"
                
            record_date = datetime.fromisoformat(timestamp_str)
            
            if record_date < cutoff_date:
                record["status"] = "archived"
                file_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
                archived_count += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)

    return archived_count

if __name__ == "__main__":
    count = archive_stale_memories(days=365)
    print(f"Archived {count} stale memories.")
