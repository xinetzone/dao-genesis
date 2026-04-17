import json
import sys
from pathlib import Path

scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
sys.path.append(str(scripts_dir))

from migrate_memory import migrate_v1_0_to_v1_1, is_v1_0

def test_is_v1_0():
    old_data = {
        "review_id": "REV-123",
        "system_meta": {"schema_version": "1.0"},
        "metadata": {"timestamp": "2026-04-17T10:00:00Z"},
        "key_findings": {"decisions": ["D1"]},
        "lessons_learned": {"success_factors": ["S1"]},
        "action_items": ["A1"],
        "status": "active"
    }
    assert is_v1_0(old_data) is True
    
    new_data = {
        "review_id": "REV-123",
        "timestamp": "2026-04-17T10:00:00Z",
        "decisions": ["D1"]
    }
    assert is_v1_0(new_data) is False

def test_migrate_v1_0_to_v1_1():
    old_data = {
        "review_id": "REV-123",
        "system_meta": {"schema_version": "1.0"},
        "metadata": {
            "timestamp": "2026-04-17T10:00:00Z",
            "participants": ["User", "AI Agent"],
            "task_type": "Feature Implementation"
        },
        "key_findings": {
            "decisions": ["D1"]
        },
        "lessons_learned": {
            "success_factors": ["S1"],
            "failure_reasons": ["F1"]
        },
        "action_items": ["A1"],
        "status": "archived"
    }
    
    new_data = migrate_v1_0_to_v1_1(old_data)
    
    assert new_data["review_id"] == "REV-123"
    assert new_data["timestamp"] == "2026-04-17T10:00:00Z"
    assert new_data["participants"] == ["User", "AI Agent"]
    assert new_data["task_type"] == "Feature Implementation"
    assert new_data["decisions"] == ["D1"]
    assert new_data["success_factors"] == ["S1"]
    assert new_data["failure_reasons"] == ["F1"]
    assert new_data["best_practices"] == []
    assert new_data["action_items"] == ["A1"]
    assert new_data["status"] == "archived"
