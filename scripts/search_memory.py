import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CACHE_REVIEWS_DIR, REVIEWS_DIR

def search_index(query: str, limit: int = 5, include_archived: bool = False):
    index_file = CACHE_REVIEWS_DIR / "search_index.json"
    if not index_file.exists():
        print(f"Error: Search index not found at {index_file}.", file=sys.stderr)
        print("Please run `python scripts/build_memory_cache.py` first.", file=sys.stderr)
        sys.exit(1)
        
    try:
        index_data = json.loads(index_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading search index: {e}", file=sys.stderr)
        sys.exit(1)
        
    query_lower = query.lower()
    results = []
    
    for entry in index_data:
        if not include_archived and entry.get("status") == "archived":
            continue
            
        # Basic scoring: check if query is in task_type, conclusions, or action_items
        score = 0
        if query_lower in entry.get("task_type", "").lower():
            score += 5
            
        for conclusion in entry.get("conclusions", []):
            if query_lower in conclusion.lower():
                score += 3
                
        for action in entry.get("action_items", []):
            if query_lower in action.lower():
                score += 2
                
        if score > 0:
            results.append((score, entry))
            
    # Sort by score (descending), then timestamp (descending)
    results.sort(key=lambda x: (x[0], x[1].get("timestamp", "")), reverse=True)
    
    return [r[1] for r in results[:limit]]

def display_results(results, verbose=False):
    if not results:
        print("No matching records found.")
        return
        
    print(f"Found {len(results)} matching record(s):\n")
    
    for i, entry in enumerate(results, 1):
        review_id = entry.get("review_id", "Unknown")
        status_tag = f" [{entry.get('status')}]" if entry.get("status") != "active" else ""
        print(f"{i}. {review_id}{status_tag} ({entry.get('timestamp', 'Unknown Date')})")
        print(f"   Task: {entry.get('task_type', 'N/A')}")
        
        conclusions = entry.get("conclusions", [])
        if conclusions:
            print(f"   Conclusion: {conclusions[0]}")
            
        actions = entry.get("action_items", [])
        if actions:
            print(f"   Action: {actions[0]}")
            
        if verbose:
            # Load full record
            full_path = REVIEWS_DIR / f"{review_id}.json"
            if full_path.exists():
                print("\n   --- Full Details ---")
                try:
                    full_data = json.loads(full_path.read_text(encoding="utf-8"))
                    print(json.dumps(full_data, indent=4, ensure_ascii=False))
                except:
                    print("   [Error loading full details]")
            else:
                print("   [Full record file missing]")
                
        print()

def main():
    parser = argparse.ArgumentParser(description="Interactive CLI tool to search memory records.")
    parser.add_argument("query", type=str, nargs="?", help="Search query (keywords). If not provided, enters interactive mode.")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum number of results to return (default: 5)")
    parser.add_argument("--all", "-a", action="store_true", help="Include archived records in search")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print full JSON for matching records")
    
    args = parser.parse_args()
    
    if args.query:
        # CLI Mode
        results = search_index(args.query, limit=args.limit, include_archived=args.all)
        display_results(results, verbose=args.verbose)
    else:
        # Interactive Mode
        print("=== Memory Search Interactive Mode ===")
        print("Type 'exit' or 'quit' to quit.")
        
        while True:
            try:
                query = input("\nSearch query: ").strip()
                if not query:
                    continue
                if query.lower() in ['exit', 'quit']:
                    break
                    
                results = search_index(query, limit=args.limit, include_archived=args.all)
                display_results(results, verbose=args.verbose)
                
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
