import json
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import REVIEWS_DIR, ensure_directories

def migrate_v1_0_to_v1_1(data: dict) -> dict:
    """
    Migrates a memory record from v1.0 (nested) to v1.1 (flat).
    """
    new_data = {}
    new_data["review_id"] = data.get("review_id", "UNKNOWN")
    
    # Metadata
    metadata = data.get("metadata", {})
    new_data["timestamp"] = metadata.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    new_data["participants"] = metadata.get("participants", ["Unknown"])
    new_data["task_type"] = metadata.get("task_type", "Unknown")
    
    # Key findings -> decisions
    key_findings = data.get("key_findings", {})
    new_data["decisions"] = key_findings.get("decisions", [])
    
    # Lessons learned -> success_factors, failure_reasons
    lessons_learned = data.get("lessons_learned", {})
    new_data["success_factors"] = lessons_learned.get("success_factors", [])
    new_data["failure_reasons"] = lessons_learned.get("failure_reasons", [])
    
    # best_practices (new in 1.1)
    new_data["best_practices"] = []
    
    new_data["action_items"] = data.get("action_items", [])
    new_data["status"] = data.get("status", "active")
    
    return new_data

def is_v1_0(data: dict) -> bool:
    """Check if the data is in the old v1.0 nested format."""
    return "system_meta" in data or "metadata" in data or "key_findings" in data

def process_file(file_path: Path, backup_dir: Path, dry_run: bool = False):
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[{file_path.name}] Error reading JSON: {e}")
        return False
        
    if not is_v1_0(data):
        print(f"[{file_path.name}] Already up-to-date. Skipping.")
        return True
        
    print(f"[{file_path.name}] Needs migration.")
    
    new_data = migrate_v1_0_to_v1_1(data)
    
    if dry_run:
        print(f"[DRY-RUN] Migrated data for {file_path.name}:")
        print(json.dumps(new_data, indent=2, ensure_ascii=False))
    else:
        # Backup original
        backup_path = backup_dir / file_path.name
        shutil.copy2(file_path, backup_path)
        
        # Write new
        file_path.write_text(json.dumps(new_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[{file_path.name}] Successfully migrated. Original backed up to {backup_path}")
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Offline migration tool for memory records.")
    parser.add_argument("--dry-run", action="store_true", help="Print migrated JSON without modifying files.")
    args = parser.parse_args()
    
    ensure_directories()
    
    files = list(REVIEWS_DIR.glob("*.json"))
    if not files:
        print(f"No records found in {REVIEWS_DIR}")
        return
        
    print(f"Found {len(files)} record(s). Checking for migrations...")
    
    backup_dir = REVIEWS_DIR.parent / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
    if not args.dry_run:
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"Backups will be saved to {backup_dir}")
        
    success_count = 0
    for file_path in files:
        if process_file(file_path, backup_dir, dry_run=args.dry_run):
            success_count += 1
            
    print(f"Migration complete. Processed {success_count}/{len(files)} files successfully.")

if __name__ == "__main__":
    main()
