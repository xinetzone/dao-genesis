from inject_memory import normalize_bullet, parse_markdown, fill_defaults_and_metadata, IDGenerator
import sys
from pathlib import Path

# 将 scripts 目录添加到 sys.path 以便导入被测试的模块
scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
sys.path.append(str(scripts_dir))


def test_id_generator_empty(tmp_path):
    # tmp_path 是 pytest 提供的临时目录 fixture
    generator = IDGenerator(tmp_path, "20260417")
    assert generator.next_id() == "REV-20260417-001"
    assert generator.next_id() == "REV-20260417-002"


def test_id_generator_existing(tmp_path):
    # 模拟已存在的记录
    (tmp_path / "REV-20260417-005.json").touch()
    (tmp_path / "REV-20260417-042.json").touch()
    # 模拟无关文件或其它日期的记录
    (tmp_path / "REV-20260416-099.json").touch()
    (tmp_path / "other.json").touch()

    generator = IDGenerator(tmp_path, "20260417")
    assert generator.next_id() == "REV-20260417-043"
    assert generator.next_id() == "REV-20260417-044"


def test_normalize_bullet_basic():
    assert normalize_bullet("- Item 1") == "Item 1"
    assert normalize_bullet("* Item 2") == "Item 2"


def test_normalize_bullet_numbers():
    assert normalize_bullet("1. First") == "First"
    assert normalize_bullet("2) Second") == "Second"
    assert normalize_bullet("(3) Third") == "Third"
    assert normalize_bullet("① Fourth") == "Fourth"


def test_normalize_bullet_brackets():
    assert normalize_bullet("[Bracket]") == "Bracket"
    assert normalize_bullet("【全角】") == "全角"
    assert normalize_bullet("(圆括)") == "圆括"


def test_normalize_bullet_invalid():
    assert normalize_bullet("Just normal text") is None
    assert normalize_bullet("   ") is None
    assert normalize_bullet("## Not a bullet") is None


def test_parse_markdown_basic():
    md = """
# Review
## 任务类型
Bug Fix
## Action Items
- Fix the issue
- Add tests
"""
    result = parse_markdown(md)
    assert result["task_type"] == "Bug Fix"
    assert result["action_items"] == ["Fix the issue", "Add tests"]


def test_parse_markdown_mixed_bullets():
    md = """
## 关键决策
1. Choose Python
[Use pytest]
"""
    result = parse_markdown(md)
    assert result["decisions"] == ["Choose Python", "Use pytest"]


def test_fill_defaults_and_metadata():
    extracted = {"task_type": "New Feature"}
    review_id = "REV-20260417-999"
    final = fill_defaults_and_metadata(extracted, review_id)

    assert final["review_id"] == review_id
    assert final["task_type"] == "New Feature"
    assert "timestamp" in final
    assert final["participants"] == ["Unknown"]
    assert final["action_items"] == []
    assert final["status"] == "active"
