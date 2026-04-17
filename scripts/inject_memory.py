import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


class IDGenerator:
    def __init__(self, reviews_dir: Path, date_str: str):
        self.prefix = f"REV-{date_str}-"
        self.max_num = 0
        for f in reviews_dir.glob(f"{self.prefix}*.json"):
            match = re.match(rf"^{self.prefix}(\d{{3}})\.json$", f.name)
            if match:
                self.max_num = max(self.max_num, int(match.group(1)))

    def next_id(self) -> str:
        self.max_num += 1
        return f"{self.prefix}{self.max_num:03d}"


def normalize_bullet(line: str) -> str | None:
    """
    尝试归一化行：去除列表前缀（-、*、1.、(1)、[xxx]等），并清理多余空白。
    如果不是一个列表项格式，则返回 None。
    """
    # 匹配中括号/粗括号整行：[xxx] 或 【xxx】
    match_brackets = re.match(r"^[\(（\[【](.+?)[\)）\]】]$", line)
    if match_brackets:
        return match_brackets.group(1).strip()
    
    # 匹配数字前缀：1. 1) (1) ①
    match_num = re.match(r"^(?:\d+[\.\)]|\(\d+\)|（\d+）|①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩)\s*(.+)$", line)
    if match_num:
        return match_num.group(1).strip()
    
    # 匹配无序前缀：- * • ·
    match_bullet = re.match(r"^[-*•·]\s*(.+)$", line)
    if match_bullet:
        return match_bullet.group(1).strip()
    
    return None

def parse_markdown(content: str) -> dict:
    """基于 Markdown Header 提取复盘字段"""
    data = {}
    current_key = None
    lines = content.splitlines()

    # 标题映射字典（忽略大小写和空格）
    header_mapping = {
        "participants": "participants",
        "参与者": "participants",
        "task type": "task_type",
        "tasktype": "task_type",
        "任务类型": "task_type",
        "decisions": "decisions",
        "关键决策": "decisions",
        "success factors": "success_factors",
        "成功因素": "success_factors",
        "failure reasons": "failure_reasons",
        "失败原因": "failure_reasons",
        "best practices": "best_practices",
        "最佳实践": "best_practices",
        "action items": "action_items",
        "行动项": "action_items",
        "status": "status",
        "状态": "status",
    }

    # 哪些字段是数组
    array_keys = {
        "participants",
        "decisions",
        "success_factors",
        "failure_reasons",
        "best_practices",
        "action_items",
    }

    for line in lines:
        line_stripped = line.strip()

        # 匹配 Header (例如 ## Decisions 或 ### 关键决策)
        header_match = re.match(r"^#{2,4}\s+(.+)$", line_stripped)
        if header_match:
            header_text = header_match.group(1).strip().lower().replace("_", " ")
            current_key = None
            for kw, key in header_mapping.items():
                if kw in header_text:
                    current_key = key
                    break
            continue

        if not current_key or not line_stripped:
            continue

        # 提取内容
        if current_key in array_keys:
            val = normalize_bullet(line_stripped)
            if val:
                if current_key not in data:
                    data[current_key] = []
                data[current_key].append(val)
        else:
            # 字符串类型字段（如 task_type, status）
            if current_key not in data:
                data[current_key] = ""
            data[current_key] += line_stripped + " "

    # 清理多余空格
    for k, v in data.items():
        if isinstance(v, str):
            data[k] = v.strip()

    return data


def fill_defaults_and_metadata(data: dict, review_id: str) -> dict:
    """补齐缺失必填字段和元数据，确保满足 schema"""
    now_utc = datetime.now(timezone.utc)
    
    final_data = {
        "review_id": review_id,
        "timestamp": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # 数组默认值
    array_keys = [
        "participants",
        "decisions",
        "success_factors",
        "failure_reasons",
        "best_practices",
        "action_items",
    ]
    
    # Task Type 兜底
    final_data["participants"] = data.get("participants", ["Unknown"])
    final_data["task_type"] = data.get("task_type", "General Review")
    
    for k in array_keys:
        if k != "participants":
            final_data[k] = data.get(k, [])
            
    final_data["status"] = data.get("status", "active")
    
    # 过滤不在 Schema 里的未知字段
    return final_data


def process_single_file(input_path: Path, reviews_dir: Path, id_generator: IDGenerator, verbose: bool = True) -> bool:
    """处理单个文件，成功返回 True，失败返回 False"""
    try:
        # 1. 读取并解析 MD
        md_content = input_path.read_text(encoding="utf-8")
        extracted_data = parse_markdown(md_content)

        # 2. 生成 ID
        review_id = id_generator.next_id()

        # 3. 填充并对齐 Schema
        final_record = fill_defaults_and_metadata(extracted_data, review_id)

        # 4. 写入文件
        out_path = reviews_dir / f"{review_id}.json"
        out_path.write_text(json.dumps(final_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        if verbose:
            print(f"[{input_path.name}] Injected -> {out_path.name}")
        return True
    except Exception as e:
        print(f"[{input_path.name}] Failed: {e}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown review file(s) to memory JSON records.")
    parser.add_argument("input_path", type=Path, help="Path to the input Markdown file or directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search recursively if input_path is a directory")
    args = parser.parse_args()

    input_path: Path = args.input_path
    if not input_path.exists():
        print(f"Error: Path not found -> {input_path}", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parents[1]
    reviews_dir = repo_root / ".storage" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    id_generator = IDGenerator(reviews_dir, date_str)

    files_to_process = []
    if input_path.is_file():
        files_to_process.append(input_path)
    elif input_path.is_dir():
        pattern = "**/*.md" if args.recursive else "*.md"
        files_to_process.extend(input_path.glob(pattern))
    else:
        print(f"Error: Invalid path type -> {input_path}", file=sys.stderr)
        return 1

    if not files_to_process:
        print("No Markdown files found to process.")
        return 0

    print(f"Found {len(files_to_process)} file(s) to process.")
    success_count = 0
    fail_count = 0

    for f in files_to_process:
        if process_single_file(f, reviews_dir, id_generator, verbose=True):
            success_count += 1
        else:
            fail_count += 1

    print(f"Batch import completed: {success_count} succeeded, {fail_count} failed.")
    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
