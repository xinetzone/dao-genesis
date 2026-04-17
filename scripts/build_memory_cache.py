import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import REVIEWS_DIR, CACHE_REVIEWS_DIR, ensure_directories

def build_index():
    ensure_directories()
    
    files = list(REVIEWS_DIR.glob("*.json"))
    if not files:
        print(f"No records found in {REVIEWS_DIR}")
        return
        
    index_data = []
    
    for file_path in files:
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[{file_path.name}] Error reading JSON: {e}", file=sys.stderr)
            continue
            
        # Only index active records by default, or maybe include archived with a flag
        # Let's include them but mark them.
        
        status = data.get("status", "active")
        
        # Build a concise summary to save tokens
        # Combine decisions and key points
        conclusions = data.get("decisions", []) + data.get("success_factors", []) + data.get("failure_reasons", [])
        
        # Take the most important action items (e.g., first 2)
        actions = data.get("action_items", [])
        
        index_entry = {
            "review_id": data.get("review_id", file_path.stem),
            "timestamp": data.get("timestamp", ""),
            "task_type": data.get("task_type", ""),
            "status": status,
            "conclusions": conclusions,
            "action_items": actions[:2]  # Limit to save tokens
        }
        
        index_data.append(index_entry)
        
    # Sort by timestamp descending
    index_data.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Write to cache
    index_file = CACHE_REVIEWS_DIR / "search_index.json"
    try:
        index_file.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Successfully built memory cache index with {len(index_data)} records at {index_file}")
    except Exception as e:
        print(f"Failed to write cache index: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Build memory cache index for efficient retrieval.")
    args = parser.parse_args()
    build_index()

if __name__ == "__main__":
    main()
