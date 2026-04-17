import argparse
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import REVIEWS_DIR, ensure_directories

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
    review_ids = args.review_id
    if not isinstance(review_ids, list):
        review_ids = [review_ids]
        
    for review_id in review_ids:
        try:
            data = load_record(review_id, reviews_dir)
            if data.get("status") == "archived":
                print(f"[{review_id}] 已归档，无需操作")
                continue
                
            data["status"] = "archived"
            save_record(review_id, data, reviews_dir)
            print(f"[{review_id}] 归档成功")
        except Exception as e:
            print(f"[{review_id}] 归档失败: {e}", file=sys.stderr)

def cmd_update(args, reviews_dir: Path):
    review_ids = args.review_id
    if not isinstance(review_ids, list):
        review_ids = [review_ids]
        
    field = args.field
    value = args.value
    append = args.append
    
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
        
    for review_id in review_ids:
        try:
            data = load_record(review_id, reviews_dir)
            print(f"[{review_id}]")
            
            if field in array_fields:
                if field not in data or not isinstance(data[field], list):
                    data[field] = []
                    
                if append:
                    data[field].append(value)
                    print(f"  {field}: [新增] {value}")
                else:
                    data[field] = [value]
                    print(f"  {field}: [修改] {value}")
            else:
                data[field] = value
                print(f"  {field}: [修改] {value}")
                
            save_record(review_id, data, reviews_dir)
        except Exception as e:
            print(f"[{review_id}] 更新失败: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Manage local memory records (Update & Archive).")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # Archive command
    parser_archive = subparsers.add_parser("archive", help="Archive a memory record.")
    parser_archive.add_argument("review_id", type=str, nargs="+", help="The ID(s) of the review record (e.g., REV-20260417-001 REV-20260417-002)")
    
    # Update command
    parser_update = subparsers.add_parser("update", help="Update a field in a memory record.")
    parser_update.add_argument("review_id", type=str, nargs="+", help="The ID(s) of the review record")
    parser_update.add_argument("--field", "-f", type=str, required=True, help="Field to update")
    parser_update.add_argument("--value", "-v", type=str, required=True, help="New value to set or append")
    parser_update.add_argument("--append", "-a", action="store_true", help="Append to an array field instead of overwriting")
    
    args = parser.parse_args()
    
    ensure_directories()
    reviews_dir = REVIEWS_DIR
    
    if args.command == "archive":
        cmd_archive(args, reviews_dir)
    elif args.command == "update":
        cmd_update(args, reviews_dir)

if __name__ == "__main__":
    main()
