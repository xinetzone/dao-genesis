import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def generate_review_id(reviews_dir: Path, date_str: str) -> str:
    """生成下一个 review_id (REV-YYYYMMDD-NNN)"""
    prefix = f"REV-{date_str}-"
    max_num = 0
    for f in reviews_dir.glob(f"{prefix}*.json"):
        match = re.match(rf"^{prefix}(\d{{3}})\.json$", f.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"{prefix}{max_num + 1:03d}"


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
            # 匹配列表项 (支持 - 或 *)
            list_match = re.match(r"^[-*]\s+(.+)$", line_stripped)
            if list_match:
                val = list_match.group(1).strip()
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a Markdown review file to a valid memory JSON record.")
    parser.add_argument("input_md", type=Path, help="Path to the input Markdown file")
    args = parser.parse_args()

    input_path: Path = args.input_md
    if not input_path.exists() or not input_path.is_file():
        print(f"Error: File not found -> {input_path}", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parents[1]
    reviews_dir = repo_root / ".storage" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    # 1. 读取并解析 MD
    md_content = input_path.read_text(encoding="utf-8")
    extracted_data = parse_markdown(md_content)

    # 2. 生成 ID
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    review_id = generate_review_id(reviews_dir, date_str)

    # 3. 填充并对齐 Schema
    final_record = fill_defaults_and_metadata(extracted_data, review_id)

    # 4. 写入文件
    out_path = reviews_dir / f"{review_id}.json"
    out_path.write_text(json.dumps(final_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Successfully injected memory record -> {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
