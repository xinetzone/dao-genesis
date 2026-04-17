from manage_memory import cmd_archive, cmd_update
import sys
import json
from pathlib import Path

scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
sys.path.append(str(scripts_dir))


class MockArgs:
    def __init__(self, review_id, field=None, value=None, append=False):
        self.review_id = review_id
        self.field = field
        self.value = value
        self.append = append


def test_archive_success(tmp_path, capsys):
    # Setup
    review_id = "REV-20260417-001"
    record_file = tmp_path / f"{review_id}.json"
    initial_data = {
        "review_id": review_id,
        "status": "active"
    }
    record_file.write_text(json.dumps(initial_data), encoding="utf-8")

    args = MockArgs(review_id=[review_id])
    cmd_archive(args, tmp_path)

    # Assert output
    captured = capsys.readouterr()
    assert "归档成功" in captured.out

    # Assert file content
    updated_data = json.loads(record_file.read_text(encoding="utf-8"))
    assert updated_data["status"] == "archived"


def test_archive_already_archived(tmp_path, capsys):
    # Setup
    review_id = "REV-20260417-001"
    record_file = tmp_path / f"{review_id}.json"
    initial_data = {
        "review_id": review_id,
        "status": "archived"
    }
    record_file.write_text(json.dumps(initial_data), encoding="utf-8")

    args = MockArgs(review_id=[review_id])
    cmd_archive(args, tmp_path)

    # Assert output
    captured = capsys.readouterr()
    assert "已归档，无需操作" in captured.out

    # Assert file content remains same
    updated_data = json.loads(record_file.read_text(encoding="utf-8"))
    assert updated_data["status"] == "archived"


def test_update_string_field(tmp_path, capsys):
    review_id = "REV-20260417-002"
    record_file = tmp_path / f"{review_id}.json"
    initial_data = {
        "review_id": review_id,
        "task_type": "Old Task"
    }
    record_file.write_text(json.dumps(initial_data), encoding="utf-8")

    args = MockArgs(review_id=[review_id], field="task_type", value="New Task")
    cmd_update(args, tmp_path)

    captured = capsys.readouterr()
    assert "[修改] New Task" in captured.out

    updated_data = json.loads(record_file.read_text(encoding="utf-8"))
    assert updated_data["task_type"] == "New Task"


def test_update_array_field_overwrite(tmp_path, capsys):
    review_id = "REV-20260417-003"
    record_file = tmp_path / f"{review_id}.json"
    initial_data = {
        "review_id": review_id,
        "action_items": ["Old Action 1", "Old Action 2"]
    }
    record_file.write_text(json.dumps(initial_data), encoding="utf-8")

    args = MockArgs(
        review_id=[review_id],
        field="action_items",
        value="New Action",
        append=False)
    cmd_update(args, tmp_path)

    captured = capsys.readouterr()
    assert "[修改] New Action" in captured.out

    updated_data = json.loads(record_file.read_text(encoding="utf-8"))
    assert updated_data["action_items"] == ["New Action"]


def test_update_array_field_append(tmp_path, capsys):
    review_id = "REV-20260417-004"
    record_file = tmp_path / f"{review_id}.json"
    initial_data = {
        "review_id": review_id,
        "action_items": ["Old Action 1"]
    }
    record_file.write_text(json.dumps(initial_data), encoding="utf-8")

    args = MockArgs(
        review_id=[review_id],
        field="action_items",
        value="Appended Action",
        append=True)
    cmd_update(args, tmp_path)

    captured = capsys.readouterr()
    assert "[新增] Appended Action" in captured.out

    updated_data = json.loads(record_file.read_text(encoding="utf-8"))
    assert updated_data["action_items"] == ["Old Action 1", "Appended Action"]
