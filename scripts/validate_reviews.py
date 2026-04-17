import json
import re
import sys
from datetime import datetime
from pathlib import Path


def _parse_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except Exception:
        return False


def _is_string_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(x, str) for x in value)


def validate_record(path: Path, schema: dict) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"invalid json: {e}"]

    if not isinstance(data, dict):
        return ["root must be an object"]

    required = schema.get("required", [])
    properties = schema.get("properties", {})

    missing = [k for k in required if k not in data]
    if missing:
        errors.append(f"missing required keys: {', '.join(missing)}")

    extra = [k for k in data.keys() if k not in properties]
    if extra:
        errors.append(f"unknown keys: {', '.join(extra)}")

    if "review_id" in data:
        if not isinstance(data["review_id"], str) or not re.match(r"^REV-[0-9]{8}-[0-9]{3}$", data["review_id"]):
            errors.append("review_id must match ^REV-[0-9]{8}-[0-9]{3}$")

    if "timestamp" in data:
        if not isinstance(data["timestamp"], str) or not _parse_datetime(data["timestamp"]):
            errors.append("timestamp must be ISO 8601 date-time")

    if "participants" in data:
        if not _is_string_list(data["participants"]) or len(data["participants"]) < 1:
            errors.append("participants must be a non-empty array of strings")

    if "task_type" in data:
        if not isinstance(data["task_type"], str) or not data["task_type"].strip():
            errors.append("task_type must be a non-empty string")

    for key in ["decisions", "success_factors", "failure_reasons", "best_practices", "action_items"]:
        if key in data and not _is_string_list(data[key]):
            errors.append(f"{key} must be an array of strings")

    if "status" in data:
        allowed = set(schema.get("properties", {}).get("status", {}).get("enum", []))
        if not isinstance(data["status"], str) or (allowed and data["status"] not in allowed):
            errors.append(f"status must be one of: {', '.join(sorted(allowed))}")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    schema_path = repo_root / "src" / "memory-schema.json"
    reviews_dir = repo_root / ".storage" / "reviews"

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"failed to read schema: {e}", file=sys.stderr)
        return 2

    if not reviews_dir.exists():
        print("no .storage/reviews directory", file=sys.stderr)
        return 2

    files = sorted(reviews_dir.glob("REV-*.json"))
    if not files:
        print("no review files found", file=sys.stderr)
        return 2

    failed = 0
    for f in files:
        errors = validate_record(f, schema)
        if errors:
            failed += 1
            for err in errors:
                print(f"{f.as_posix()}: {err}", file=sys.stderr)

    if failed:
        return 1

    print(f"validated {len(files)} review file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
