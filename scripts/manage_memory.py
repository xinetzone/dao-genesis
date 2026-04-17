import argparse
import json
import sys
from pathlib import Path

def load_record(review_id: str, reviews_dir: Path) -> dict:
    file_path = reviews_dir / f"{review_id}.json"
    if not file_path.exists():
        print(f"Error: Record {review_id} not found at {file_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        return data
    except Exception as e:
        print(f"Error: Failed to parse {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def save_record(review_id: str, data: dict, reviews_dir: Path):
    file_path = reviews_dir / f"{review_id}.json"
    try:
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"Error: Failed to write {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_archive(args, reviews_dir: Path):
    review_id = args.review_id
    data = load_record(review_id, reviews_dir)
    
    if data.get("status") == "archived":
        print(f"[{review_id}] 归档成功")
        return
    
    data["status"] = "archived"
    save_record(review_id, data, reviews_dir)
    print(f"[{review_id}] 归档成功")

def cmd_update(args, reviews_dir: Path):
    review_id = args.review_id
    field = args.field
    value = args.value
    append = args.append
    
    data = load_record(review_id, reviews_dir)
    
    # Valid fields mapping
    array_fields = {
        "participants",
        "decisions",
        "success_factors",
        "failure_reasons",
        "best_practices",
        "action_items"
    }
    string_fields = {
        "task_type",
        "status"
    }
    
    if field not in array_fields and field not in string_fields:
        print(f"Error: Field '{field}' is not allowed to be updated.", file=sys.stderr)
        sys.exit(1)
        
    if field in string_fields and append:
        print(f"Error: Cannot append to a string field '{field}'.", file=sys.stderr)
        sys.exit(1)
        
    print(f"[{review_id}]")
    
    if field in array_fields:
        if field not in data or not isinstance(data[field], list):
            data[field] = []
            
        if append:
            data[field].append(value)
            print(f"{field}: [新增] {value}")
        else:
            # Overwrite the array with a single element
            data[field] = [value]
            print(f"{field}: [修改] {value}")
    else:
        # String fields
        data[field] = value
        print(f"{field}: [修改] {value}")
        
    save_record(review_id, data, reviews_dir)

def main():
    parser = argparse.ArgumentParser(description="Manage local memory records (Update & Archive).")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # Archive command
    parser_archive = subparsers.add_parser("archive", help="Archive a memory record.")
    parser_archive.add_argument("review_id", type=str, help="The ID of the review record (e.g., REV-20260417-001)")
    
    # Update command
    parser_update = subparsers.add_parser("update", help="Update a field in a memory record.")
    parser_update.add_argument("review_id", type=str, help="The ID of the review record")
    parser_update.add_argument("--field", "-f", type=str, required=True, help="Field to update")
    parser_update.add_argument("--value", "-v", type=str, required=True, help="New value to set or append")
    parser_update.add_argument("--append", "-a", action="store_true", help="Append to an array field instead of overwriting")
    
    args = parser.parse_args()
    
    repo_root = Path(__file__).resolve().parents[1]
    reviews_dir = repo_root / ".storage" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    
    if args.command == "archive":
        cmd_archive(args, reviews_dir)
    elif args.command == "update":
        cmd_update(args, reviews_dir)

if __name__ == "__main__":
    main()
